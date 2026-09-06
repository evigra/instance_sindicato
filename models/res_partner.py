from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    matricula = fields.Char(
        string='Matrícula'
    )


    ine_file = fields.Binary(
        string='INE',
        attachment=True
    )

    ine_filename = fields.Char(
        string='Nombre archivo INE'
    )

    tarjeton_file = fields.Binary(
        string='Tarjetón',
        attachment=True
    )

    tarjeton_filename = fields.Char(
        string='Nombre archivo Tarjetón'
    )

    # ============================================================
    # PADRE / MADRE - HIJOS
    # ============================================================

    parent_contact_id = fields.Many2one(
        'res.partner',
        string='Padre / Madre',
        index=True,
        ondelete='cascade'
    )

    child_ids = fields.One2many(
        'res.partner',
        'parent_contact_id',
        string='Hijos'
    )

    # ============================================================
    # DATOS DEL HIJO
    # ============================================================

    child_birthdate = fields.Date(
        string='Fecha de nacimiento'
    )

    child_curp = fields.Char(
        string='CURP'
    )

    child_gender = fields.Selection(
        [
            ('male', 'Masculino'),
            ('female', 'Femenino'),
        ],
        string='Sexo'
    )