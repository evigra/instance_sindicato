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



