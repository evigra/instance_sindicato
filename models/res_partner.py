from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    ine_file = fields.Binary(string='INE',attachment=True)
    ine_filename = fields.Char(string='Nombre archivo INE')

    tarjeton_file = fields.Binary(string='Tarjetón', attachment=True)
    tarjeton_filename = fields.Char(string='Nombre archivo Tarjetón')


    