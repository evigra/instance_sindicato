from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal

import base64
import io
import qrcode


class FamiliaPortal(CustomerPortal):

    @http.route(
        '/my/familia',
        type='http',
        auth='user',
        website=True
    )
    def portal_familia(self, **kw):

        partner = request.env.user.partner_id

        familiares = request.env['familia'].sudo().search([
            # Aquí pondremos después el filtro correcto
            # para determinar qué eventos corresponden
            # al usuario.
        ])
        
        values = {
            'familiares': familiares,
            'page_name': 'familiares',
        }

        return request.render(
            'instance_sindicato.portal_familia',
            values
        )

