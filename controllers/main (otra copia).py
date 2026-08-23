from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal

import base64
import io
import qrcode


class SindicatoPortal(CustomerPortal):

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

        evento = request.env['eventos'].browse(evento_id)

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
        '/my/credencial',
        type='http',
        auth='user',
        website=True
    )
    def portal_credencial(self, **kw):
        partner = request.env.user.partner_id
        

        url = request.httprequest.host_url.rstrip(
            '/'
        ) + f'/credencial/validar/{partner.id}'

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

        return request.render(
            'instance_sindicato.portal_credencial',
            {
                'partner': partner,
                'qr_code': qr_base64,
            }
        )