# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import datetime
import requests
import random
from dateutil.relativedelta import relativedelta
from odoo import http, api, fields, models, _
from odoo.http import request
from odoo.addons.portal.controllers.web import Home
from datetime import timedelta
from odoo.exceptions import ValidationError

class plantilla(models.Model):
    _name = "plantilla"
    _description = 'plantilla'
    #_order="fecha DESC"

    _inherit = [
        'mail.thread',
        'mail.activity.mixin',
    ]

    name = fields.Char('Nombre')
    matricula_ocupante = fields.Char('Matricula Ocupante',size = 12,required=True)
    departamento = fields.Char('Departamento', size = 75, tracking=True,)
    adscripcion = fields.Char('Ascripcion', size = 75, tracking=True,)
    tipo_contratacion = fields.Char('Tipo Contratacion', tracking=True)
    puesto = fields.Char('Puesto', size = 10)
    categoria = fields.Char('Categoria', size = 75, tracking=True,)
    clasificacion = fields.Char('Clasificacion')
    especialidad = fields.Char('Especialidad', size = 75 )
    turno_descr = fields.Char(string='Turno', size = 25 )
    horario = fields.Char(string='Horario', size = 75 )
    nombre_del_titular = fields.Char('Nombre del titular', size = 75)
    #fecha_de_ocupacion = fields.Datetime(string='Fecha de ocupacion')

@api.model_create_multi
def create(self, vals_list):
    records = self.env[self._name]

    for vals in vals_list:
        puesto                  = vals.get('puesto') or False
        matricula_ocupante      = vals.get('matricula_ocupante') or False

        existente = self.search([
            ('matricula_ocupante', '=', matricula_ocupante),
            ('puesto', '=', puesto)
        ], limit=1)

        vals['name'] = vals.get('nombre_del_titular')
        if existente:
            existente.write(vals)
            records |= existente
        else:
            records |= super().create(vals)

    return records