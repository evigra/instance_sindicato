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
        '/my/registro/<int:evento_id>',
        type='http',
        auth='user',
        website=True
    )
    def portal_registro(self, evento_id, **kw):

        # ==========================================================
        # DATOS
        # ==========================================================

        partner = request.env.user.partner_id

        evento = request.env['eventos'].sudo().browse(evento_id)

        if not evento.exists():
            return request.not_found()

        # ==========================================================
        # BUSCAR / CREAR ASISTENCIA
        # ==========================================================

        asistencia = request.env['asistencias'].sudo().search([
            ('partner_id', '=', partner.id),
            ('evento_id', '=', evento.id),
        ], limit=1)

        if not asistencia:
            asistencia = request.env['asistencias'].sudo().create({
                'name': evento.name,
                'partner_id': partner.id,
                'evento_id': evento.id,
            })

        # ==========================================================
        # GENERAR URL DEL QR
        # ==========================================================

        url = (
            request.httprequest.host_url.rstrip('/')
            + f'/my/asistencias/{asistencia.id}'
        )

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

        nombre_pdf = (
            'Constancia de Registro %s.pdf'
            % partner.matricula
        )

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
        # ENVIAR CORREO CON MAIL TEMPLATE
        # ==========================================================

        template = request.env.ref(
            'instance_sindicato.mail_template_eventos',
            raise_if_not_found=False
        )

        if template and partner.email:
            template = template.sudo().with_company(
                request.env.company
            ).with_context(
                asistencia=asistencia
            )

            template.send_mail(
                partner.id,
                force_send=True,
                email_values={
                    'attachment_ids': [
                        (4, attachment.id)
                    ],
                }
            )
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