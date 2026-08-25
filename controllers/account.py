from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomerPortalInherit(CustomerPortal):

    @http.route(
        ['/my/account'],
        type='http',
        auth='user',
        website=True
    )
    def account(self, redirect=None, **post):

        partner = request.env.user.partner_id

        ine_file = request.httprequest.files.get('ine_file')
        tarjeton_file = request.httprequest.files.get('tarjeton_file')

        vals = {}

        if ine_file and ine_file.filename:

            vals['ine_file'] = ine_file.read()
            vals['ine_filename'] = ine_file.filename

        if tarjeton_file and tarjeton_file.filename:

            vals['tarjeton_file'] = tarjeton_file.read()
            vals['tarjeton_filename'] = tarjeton_file.filename

        if vals:
            partner.sudo().write(vals)

        return super().account(
            redirect=redirect,
            **post
        )