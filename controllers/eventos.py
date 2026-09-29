from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal
from babel.dates import format_date

import base64
import io
import qrcode


class PortalEventos(CustomerPortal):

    @http.route(
        '/my/eventos',
        type='http',
        auth='user',
        website=True
    )
    def portal_eventos(self, **kw):

        partner = request.env.user.partner_id


        eventos = request.env['eventos'].sudo().search([
            # Aquí pondremos después el filtro correcto
            # para determinar qué eventos corresponden
            # al usuario.
        ])


        values = {
            'eventos': eventos,
            'page_name': 'eventos',
            'format_date': format_date,
        }

        return request.render(
            'instance_sindicato.portal_eventos',
            values
        )

    @http.route(
        '/my/eventos/<int:evento_id>',
        type='http',
        auth='user',
        website=True
    )
    def portal_evento_detalle(self, evento_id, **kw):

        evento = request.env['eventos'].sudo().browse(evento_id)
        if not evento.exists():
            return request.not_found()

        values = {
            'evento': evento,
            'page_name': 'evento',
        }

        return request.render(
            'instance_sindicato.portal_evento_detalle',
            values
        )

    
    @http.route(
        '/my/asistencias/<int:evento_id>',
        type='http',
        auth='user',
        website=True
    )
    def portal_asistencia(self, evento_id, **kw):

        partner = request.env.user.partner_id

        evento = request.env['eventos'].sudo().browse(evento_id)

        if not evento.exists():
            return request.not_found()

        asistencia = request.env['asistencias'].sudo().search([
            ('partner_id', '=', partner.id),
            ('evento_id', '=', evento.id),
        ], limit=1)

        # Si no existe el registro de asistencia, lo creamos
        if not asistencia:
            asistencia = request.env['asistencias'].sudo().create({
                'name': evento.name,
                'partner_id': partner.id,
                'evento_id': evento.id,
            })

        # ==========================================================


        url = request.httprequest.host_url.rstrip(
            '/'
        ) + f'/my/credencial/{partner.id}'

        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=4,
        )

        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image()

        buffer = io.BytesIO()
        img.save(buffer, format='PNG')

        qr_base64 = base64.b64encode(
            buffer.getvalue()
        ).decode()



        # ==========================================================
        # GENERAR PDF
        # ==========================================================

        pdf_content, content_type = request.env[
            'ir.actions.report'
        ].sudo()._render_qweb_pdf(
            'instance_sindicato.action_report_asistencia',
            [asistencia.id],
            data={
                'qr_base64': qr_base64,
            }
        )
        nombre_pdf = 'Constancia de Registro %s.pdf' % partner.matricula

        # ==========================================================
        # CREAR ADJUNTO
        # ==========================================================

        attachment = request.env['ir.attachment'].sudo().create({
            'name': nombre_pdf,
            'type': 'binary',
            'datas': base64.b64encode(pdf_content),
            'mimetype': 'application/pdf',
            'res_model': 'asistencias',
            'res_id': asistencia.id,
        })

        # ==========================================================
        # CREAR CORREO
        # ==========================================================

        email_to = partner.email
        email_from = '%s <%s>' % (
            request.env.company.name,
            request.env.company.email
        )
        if email_to:
            mail_values = {
                'subject': 'Constancia de Registro - %s' % evento.name,
                'body_html': """
                    <p>
                        Apreciable
                        <h3>%s</h3>
                    </p>
                    <p>
                        Se ha generado correctamente tu constancia
                        de registro para el evento <strong>%s</strong>.
                    </p>
                    <img src="data:image/png;base64,%s"   style="width:150px;"/>
                    <p>
                        Encontrarás la constancia adjunta a este correo
                        en formato PDF.
                    </p>

                    <p>Saludos.</p>
                """ % (
                    partner.name,
                    evento.name,
                    qr_base64,
                ),

                'email_to': email_to,
                'email_from': email_from,
                'attachment_ids': [(4, attachment.id)],
            }

            mail = request.env['mail.mail'].sudo().create(mail_values)

            # Enviar inmediatamente
            mail.sudo().send()

        # ==========================================================
        # DEVOLVER PDF AL NAVEGADOR
        # ==========================================================

        pdfhttpheaders = [
            ('Content-Type', 'application/pdf'),
            ('Content-Length', str(len(pdf_content))),
            (
                'Content-Disposition',
                'inline; filename="%s"' % nombre_pdf
            ),
        ]

        return request.make_response(
            pdf_content,
            headers=pdfhttpheaders
        )
