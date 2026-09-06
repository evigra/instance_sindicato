import base64

from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class Portalchildren(CustomerPortal):

    # ============================================================
    # MI CUENTA
    # ============================================================


    # ============================================================
    # LISTA DE HIJOS
    # ============================================================

    @http.route(
        ['/my/children'],
        type='http',
        auth='user',
        website=True,
    )
    def children(self, **kwargs):

        partner = request.env.user.partner_id

        children = request.env['res.partner'].sudo().search([
            ('parent_contact_id', '=', partner.id)
        ])

        values = {
            'partner': partner,
            'children': children,
            'page_name': 'children',
        }

        return request.render(
            'instance_sindicato.portal_my_children',
            values
        )

    # ============================================================
    # AGREGAR HIJO
    # ============================================================

    @http.route(
        ['/my/children/new'],
        type='http',
        auth='user',
        website=True,
        methods=['GET', 'POST'],
    )
    def children_new(self, **post):

        partner = request.env.user.partner_id

        # --------------------------------------------------------
        # GUARDAR NUEVO HIJO
        # --------------------------------------------------------

        if request.httprequest.method == 'POST':

            vals = {
                'name': post.get('name'),
                'child_birthdate': ( post.get('child_birthdate') or False     ),
                'child_curp': ( post.get('child_curp') or False   ),
                'child_gender': ( post.get('child_gender') or False    ),
                'parent_contact_id': partner.id,
            }

            # ----------------------------------------------------
            # FOTO DEL HIJO
            # ----------------------------------------------------

            image_file = request.httprequest.files.get(
                'image_1920'
            )

            if image_file and image_file.filename:
                vals['image_1920'] = base64.b64encode(
                    image_file.read()
                )




            request.env['res.partner'].sudo().create(vals)

            return request.redirect('/my/children')

        # --------------------------------------------------------
        # MOSTRAR FORMULARIO
        # --------------------------------------------------------

        values = {
            'partner': partner,
            'page_name': 'children_new',
        }

        return request.render(
            'instance_sindicato.portal_my_child_form',
            values
        )

    # ============================================================
    # EDITAR HIJO
    # ============================================================

    @http.route(
        ['/my/children/<int:child_id>/edit'],
        type='http',
        auth='user',
        website=True,
        methods=['GET', 'POST'],
    )
    def children_edit(self, child_id, **post):

        partner = request.env.user.partner_id

        # --------------------------------------------------------
        # BUSCAR HIJO
        # --------------------------------------------------------

        child = request.env['res.partner'].sudo().search([
            ('id', '=', child_id),
            ('parent_contact_id', '=', partner.id),
        ], limit=1)

        if not child:
            return request.redirect('/my/children')

        # --------------------------------------------------------
        # GUARDAR CAMBIOS
        # --------------------------------------------------------

        if request.httprequest.method == 'POST':

            vals = {
                'name': post.get('name'),
                'child_birthdate': (
                    post.get('child_birthdate') or False
                ),
                'child_curp': (
                    post.get('child_curp') or False
                ),
                'child_gender': (
                    post.get('child_gender') or False
                ),
            }

            # ----------------------------------------------------
            # FOTO DEL HIJO
            # ----------------------------------------------------

            image_file = request.httprequest.files.get(
                'image_1920'
            )

            if image_file and image_file.filename:
                vals['image_1920'] = base64.b64encode(
                    image_file.read()
                )

            child.sudo().write(vals)

            return request.redirect('/my/children')

        # --------------------------------------------------------
        # MOSTRAR FORMULARIO
        # --------------------------------------------------------

        values = {
            'partner': partner,
            'child': child,
            'page_name': 'children_edit',
        }

        return request.render(
            'instance_sindicato.portal_my_child_form',
            values
        )