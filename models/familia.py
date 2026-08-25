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

class familia(models.Model):
    _name = "familia"
    _description = 'familia'
    #_order="fecha DESC"


    name = fields.Char('Nombre', size = 75 , required=True)
    nacimiento = fields.Datetime(string='Fecha de nacimiento', required=True)
    parentesco = fields.Selection([('Hijos', 'hijos'), ('Padres', 'padres')], copy=False)
    
    archivo = fields.Binary(
        string='Archivo',
        attachment=True
    )
    archivo_nombre = fields.Char(
        string='Nombre del archivo'
    )    
