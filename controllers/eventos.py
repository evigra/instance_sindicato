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
        #evento = request.env['eventos'].sudo().search([])
        if not evento.exists():
            return request.not_found()

        values = {
            'evento': evento,
            'page_name': 'evento',
        }

        return request.render(
            #'instance_sindicato.portal_eventos',
            'instance_sindicato.portal_evento_detalle',
            values
        )

