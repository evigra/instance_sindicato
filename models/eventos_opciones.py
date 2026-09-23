# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import datetime
import requests
import random
from dateutil.relativedelta import relativedelta
from odoo import http, api, fields, models, _
from odoo.http import request
from odoo.addons.portal.controllers.web import Home

class eventos_opciones(models.Model):
    _name = "eventos_opciones"
    _description = 'Opciones de eventos'
    

    name = fields.Char('Nombre de la opcion', size = 75  )

    partner_id = fields.Many2one('res.partner', string='Usuario', required=True)
    evento_id = fields.Many2one('eventos', string='Evento', required=True)

    opcion_file = fields.Binary(
        string='Foto',
        attachment=True
    )





