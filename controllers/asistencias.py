from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal
from babel.dates import format_date

import base64
import io
import qrcode

class PortalAsistencias(CustomerPortal):

        
    @http.route(
        '/my/asistencias/<int:asistencia_id>',
        type='http',
        auth='user',
        website=True
    )
    def portal_asistencia(self, asistencia_id, **kw):

        print("#######################") 
         
        asistencias = request.env['asistencias'].sudo().browse(asistencia_id)
        


        #partner_id = fields.Many2one('res.partner', string='Usuario', required=True)
        #evento_id = fields.Many2one('eventos', string='Evento', required=True)

        vals = {
            'partner_id': request.env.user.partner_id,
            'id': asistencia_id,
        }
        #request.env['asistencias'].sudo().create(vals)


        values = {
            'asistencias': asistencias,
            'page_name': 'eventos',
            'format_date': format_date,
        }

        return request.render(
            'instance_sindicato.portal_asistencias',
            values
        )

