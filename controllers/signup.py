# -*- coding: utf-8 -*-

from odoo import http, _
from odoo.http import request
from odoo.addons.auth_signup.controllers.main import AuthSignupHome


class SindicatoSignup(AuthSignupHome):

    # ============================================================
    # CONTEXTO DEL SIGNUP
    # ============================================================

    def get_auth_signup_qcontext(self):
        qcontext = super().get_auth_signup_qcontext()

        # Obtener matrícula enviada desde el formulario
        matricula = (
            request.params.get('matricula') or ''
        ).strip()

        qcontext['matricula'] = matricula

        return qcontext

    # ============================================================
    # BUSCAR MATRÍCULA
    # ============================================================

    @http.route(
        '/sindicato/buscar_matricula',
        type='json',
        auth='public',
        methods=['POST'],
        csrf=False,
    )
    def buscar_matricula(self, matricula=None, **kwargs):

        matricula = (matricula or '').strip()

        if not matricula:
            return {
                'encontrado': False,
            }

        plantilla = request.env['plantilla'].sudo().search(
            [
                ('matricula_ocupante', '=', matricula)
            ],
            limit=1,
        )

        if not plantilla:
            return {
                'encontrado': False,
            }

        return {
            'encontrado': True,
            'matricula': plantilla.matricula_ocupante or '',
            'name': plantilla.nombre_del_titular or '',
            'function': plantilla.categoria or '',
        }

    # ============================================================
    # CREACIÓN DEL USUARIO
    # ============================================================

    def do_signup(self, qcontext):

        # --------------------------------------------------------
        # Valores originales
        # --------------------------------------------------------

        values = {
            'login': qcontext.get('login'),
            'name': qcontext.get('name'),
            'password': qcontext.get('password'),
        }

        # --------------------------------------------------------
        # Validaciones
        # --------------------------------------------------------

        assert values.get('login'), _(
            "El correo electrónico es obligatorio."
        )

        assert values.get('password'), _(
            "La contraseña es obligatoria."
        )

        assert (
            values.get('password')
            == qcontext.get('confirm_password')
        ), _(
            "Las contraseñas no coinciden."
        )

        # --------------------------------------------------------
        # MATRÍCULA
        # --------------------------------------------------------

        matricula = (
            qcontext.get('matricula') or ''
        ).strip()

        if matricula:

            plantilla = request.env['plantilla'].sudo().search(
                [
                    (
                        'matricula_ocupante',
                        '=',
                        matricula,
                    )
                ],
                limit=1,
            )

            # Guardar matrícula
            values['matricula'] = matricula

            # Datos provenientes de plantilla
            if plantilla:

                if plantilla.nombre_del_titular:
                    values['name'] = (
                        plantilla.nombre_del_titular
                    )

                if plantilla.categoria:
                    values['function'] = (
                        plantilla.categoria
                    )

        # --------------------------------------------------------
        # CREAR USUARIO + PARTNER
        # --------------------------------------------------------

        self._signup_with_values(
            qcontext.get('token'),
            values,
        )