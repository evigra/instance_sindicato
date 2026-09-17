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
    vacante_c_c_ppto= fields.Char('Vacante c c ppto',size = 20)
    depto = fields.Char('Depto', size = 30, tracking=True,)
    departamento = fields.Char('Departamento', size = 75, tracking=True,)
    adscripcion = fields.Char('Ascripcion', size = 75, tracking=True,)
    tipo_contratacion = fields.Char('Tipo Contratacion', tracking=True)
    puesto = fields.Char('Puesto', size = 10, tracking=True,)
    categoria = fields.Char('Categoria', size = 75, tracking=True,)
    clasificacion = fields.Char('Clasificacion', tracking=True,)
    especialidad = fields.Char('Especialidad', size = 75 , tracking=True,)
    turno_descr = fields.Char(string='Turno Descr', size = 25 , tracking=True,)
    horario = fields.Char(string='Horario', size = 75 , tracking=True,)
    tipo_Plaza_Descripcion = fields.Char(string='Tipo Plaza Descripcion', size = 40 , tracking=True,)
    titular_de_plz = fields.Char('Titular de plz', size = 12)
    nombre_del_titular = fields.Char('Nombre del titular', size = 75)
    nombre_del_ocupante = fields.Char('Nombre del Ocupante', size = 75)
    #fecha_de_ocupacion = fields.Datetime(string='Fecha de ocupacion')

@api.model_create_multi
def create(self, vals_list):
    records = self.env[self._name]

    for vals in vals_list:
        vals['matricula_ocupante']      = vals['matricula_ocupante'] or vals.get('titular_de_plz')
        vals['nombre_del_ocupante']     = vals['nombre_del_ocupante'] or vals.get('nombre_del_titular')
        vals['name']                    =vals['nombre_del_ocupante']
        matricula_ocupante              = vals['matricula_ocupante']

        existente = self.search([
            ('matricula_ocupante', '=', matricula_ocupante),
        ], limit=1)

        vals['name'] = vals['nombre_del_ocupante']
        if existente:
            existente.write(vals)
            records |= existente
        else:
            records |= super().create(vals)

    return records