import base64

from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomerPortalInherit(CustomerPortal):

    @http.route(
        ['/my/account'],
        type='http',
        auth='user',
        website=True,
    )
    def account(self, redirect=None, **post):

        partner = request.env.user.partner_id

        files = request.httprequest.files

        image_file = files.get('image_1920')
        ine_file = files.get('ine_file')
        tarjeton_file = files.get('tarjeton_file')

        vals = {}

        # FOTO
        if image_file and image_file.filename:
            vals['image_1920'] = base64.b64encode(
                image_file.read()
            )

        # INE
        if ine_file and ine_file.filename:
            vals['ine_file'] = base64.b64encode(
                ine_file.read()
            )
            vals['ine_filename'] = ine_file.filename

        # TARJETÓN
        if tarjeton_file and tarjeton_file.filename:
            vals['tarjeton_file'] = base64.b64encode(
                tarjeton_file.read()
            )
            vals['tarjeton_filename'] = tarjeton_file.filename

        if vals:
            partner.sudo().write(vals)

        post.pop('image_1920', None)
        post.pop('ine_file', None)
        post.pop('tarjeton_file', None)

        return super().account(
            redirect=redirect,
            **post
        )