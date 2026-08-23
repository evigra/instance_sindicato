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

class eventos(models.Model):
    _name = "eventos"
    _description = 'Eventos'
    _order="fecha DESC"

    _inherit = [
        'mail.thread',
        'mail.activity.mixin',
    ]

    name = fields.Char('Nombre del evento', size = 75 , required=True,  tracking=True,)
    tipo = fields.Selection([('Trabajador', 'trabajador'), ('Familiar', 'Familiar')], default='Trabajador', copy=False)
    fecha = fields.Datetime(string='Fecha', required=True, tracking=True,default=lambda self: fields.Datetime.now() + timedelta(days=3))
    duracion = fields.Datetime(string='Duracion')
    fecha_publicacion = fields.Datetime(string='Fecha Publicacion', required=True, default=lambda self: fields.Datetime.now() + timedelta(days=1))
    fecha_termino = fields.Datetime(string='Fecha Termino', required=True,default=lambda self: fields.Datetime.now() + timedelta(days=2))
    estado = fields.Selection([('Programado', 'programado'), ('Anunciado', 'anunciado'), ('En proceso', 'en proceso'), ('Finalizado', 'Finalizado')], default='Programado', copy=False)

    asistencia_ids = fields.One2many('asistencias','evento_id', string='Asistencias')

    total_asistencias = fields.Integer(string='Total', compute='_compute_asistencias', store=True)
    asistencias_iniciadas = fields.Integer(string='Iniciadas', compute='_compute_asistencias', store=True)
    asistencias_pendientes = fields.Integer(string='Pendientes', compute='_compute_asistencias', store=True)

    @api.depends(
        'asistencia_ids',
        'asistencia_ids.fecha_inicio'
    )
    def _compute_asistencias(self):
        for evento in self:
            asistencias = evento.asistencia_ids
            evento.total_asistencias = len(asistencias)
            evento.asistencias_iniciadas = len(
                asistencias.filtered(
                    lambda a: a.fecha_inicio
                )
            )
            evento.asistencias_pendientes = evento.total_asistencias - evento.asistencias_iniciadas
    
    @api.constrains('fecha_publicacion', 'fecha_termino')
    def _check_fechas(self):
        for record in self:
            if (
                record.fecha_publicacion
                and record.fecha_termino
                and record.fecha_publicacion >= record.fecha_termino
            ):
                raise ValidationError(
                    'En la vigencia, la Fecha de Publicación debe ser menor que la Fecha de Término.'
                )