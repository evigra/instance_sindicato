from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal

import base64
import io
import qrcode


class CredencialPortal(CustomerPortal):


    @http.route(
        '/my/credencial',
        type='http',
        auth='user',
        website=True
    )
    def portal_credencial(self, **kw):
        partner = request.env.user.partner_id
        return self.portal_metodo(partner)


    @http.route(
        '/my/credencial/<int:credencia_id>',
        type='http',
        auth='user',
        website=True
    )
    def portal_credencial_detalle(self, credencia_id, **kw):
        partner = request.env['res.partner'].sudo().browse(credencia_id)
        return  self.portal_metodo(partner)


    def portal_metodo(self, partner, **kw):

        company = request.env.company        

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

        return request.render(
            'instance_sindicato.portal_credencial',
            {
                'partner': partner,
                'qr_code': qr_base64,
                'company': company,
            }
        )


        