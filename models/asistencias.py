# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import datetime
import requests
import random
from dateutil.relativedelta import relativedelta
from odoo import http, api, fields, models, _
from odoo.http import request
from odoo.addons.portal.controllers.web import Home

class asistencias(models.Model):
    _name = "asistencias"
    _description = 'asistencias'
    

    name = fields.Char('Nombre del evento', size = 75  )

    partner_id = fields.Many2one('res.partner', string='Usuario', required=True)
    evento_id = fields.Many2one('eventos', string='Evento', required=True)

    fecha = fields.Datetime(string='Solicitado', default=lambda self: fields.Datetime.now())
    fecha_inicio = fields.Datetime(string='Llegada')
    fecha_termino = fields.Datetime(string='Salida')



class ReportAsistencia(models.AbstractModel):
    _name = 'report.instance_sindicato.report_asistencia_document'
    _description = 'Reporte de Asistencia'

    @api.model
    def _get_report_values(self, docids, data=None):
        asistencias = self.env['asistencias'].browse(docids)

        return {
            'doc_ids': docids,
            'doc_model': 'asistencias',
            'docs': asistencias,
            'qr_base64': data.get('qr_base64') if data else False,
        }
