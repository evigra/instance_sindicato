from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo import http, api, fields, models, _
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
        asistencias = request.env['asistencias'].sudo().browse(asistencia_id)

        values = {
            'asistencias': asistencias,
            'page_name': 'eventos',
            'format_date': format_date,
        }

        return request.render(
            'instance_sindicato.portal_asistencias',
            values
        )


    @http.route(
        '/my/asistencias/<int:asistencia_id>/<string:accion>',
        type='http',
        auth='user',
        website=True
    )
    def portal_asistencia_accion(self, asistencia_id,accion, **kw):

        asistencias = request.env['asistencias'].sudo().browse(asistencia_id)


        if accion == 'entrada':
            asistencias.write({
                'fecha_inicio': fields.Datetime.now(),
            })
        elif accion == 'salida':
            asistencias.write({
                'fecha_termino': fields.Datetime.now(),
            })



        values = {
            'asistencias': asistencias,
            'page_name': 'eventos',
            'format_date': format_date,
        }

        return request.render(
            'instance_sindicato.portal_asistencias',
            values
        )
