# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import datetime
import requests
import random
from dateutil.relativedelta import relativedelta
from odoo import http, api, fields, models, _
from odoo.http import request
from odoo.addons.portal.controllers.web import Home

"""
class WebsiteSort(Home):
   @http.route()
   def index(self, **kw):
       super(WebsiteSort, self).index()
       return request.render('website.homepage', {})
"""
class vehicle(models.Model):
    _inherit = "fleet.vehicle"
    
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id)    
    
class company(models.Model):
    _inherit = "res.company"


