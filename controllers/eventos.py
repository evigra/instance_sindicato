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

        print("====================================")
        print("EVENTO ID:", evento.id)
        print("NOMBRE:", evento.name)
        print("PUBLICACION FILE:", bool(evento.publicacion_file))
        print("PUBLICACION FILE LENGTH:", len(evento.publicacion_file or b''))
        print("FILENAME:", evento.publicacion_filename)
        print("====================================")



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
        print("*************** PORTAL ASISTENCIA CARGADO ***************")

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

        # Generar PDF usando el registro de ASISTENCIA
        pdf_content, content_type = request.env['ir.actions.report'].sudo()._render_qweb_pdf(
            'instance_sindicato.action_report_asistencia',
            [asistencia.id]
        )
        pdfhttpheaders = [
            ('Content-Type', 'application/pdf'),
            ('Content-Length', str(len(pdf_content))),
            (
                'Content-Disposition',
                'inline; filename="Constancia de Registro %s.pdf"'
                % partner.matricula
            ),
        ]

        return request.make_response(
            pdf_content,
            headers=pdfhttpheaders
        )