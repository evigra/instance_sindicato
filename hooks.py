from odoo import SUPERUSER_ID

"""
def pre_load_hook(env):
    load_es_mx_lang(env)

def post_load_hook(env):
    load_es_mx_lang(env)
"""
def post_init_hook(env):
    load_es_mx_lang(env)


def load_es_mx_lang(env):

    lang_code = 'es_MX'

    # ------------------------------------------------------------
    # Buscar idioma
    # ------------------------------------------------------------

    lang = env['res.lang'].sudo().search(
        [('code', '=', lang_code)],
        limit=1
    )

    # ------------------------------------------------------------
    # Si no existe, intentar instalarlo
    # ------------------------------------------------------------

    if not lang:
        try:
            env['res.lang']._activate_lang(lang_code)
        except Exception:
            pass

        lang = env['res.lang'].sudo().search(
            [('code', '=', lang_code)],
            limit=1
        )

    # ------------------------------------------------------------
    # Activar idioma
    # ------------------------------------------------------------

    if lang:
        lang.sudo().write({
            'active': True,
        })

    # ------------------------------------------------------------
    # Configurar Administrador
    # ------------------------------------------------------------

    admin = env['res.users'].sudo().browse(SUPERUSER_ID)

    if admin.exists():
        admin.sudo().write({
            'lang': lang_code,
        })

    # ------------------------------------------------------------
    # Configurar usuario público
    # ------------------------------------------------------------

    public_user = env.ref(
        'base.public_user',
        raise_if_not_found=False
    )

    if public_user:
        public_user.sudo().write({
            'lang': lang_code,
        })