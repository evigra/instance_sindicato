from odoo import SUPERUSER_ID


def pre_load_hook(env):
    load_es_mx_lang(env)

def post_load_hook(env):
    load_es_mx_lang(env)


def load_es_mx_lang(env):
    lang = env['res.lang'].search([
        ('code', '=', 'es_MX')
    ], limit=1)

    if not lang:
        return

    # Activar Español / México
    lang.write({
        'active': True,
    })

    # Cambiar idioma de TODOS los usuarios existentes
    env['res.users'].search([]).write({
        'lang': 'es_MX',
    })