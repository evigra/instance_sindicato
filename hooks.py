from odoo import api, SUPERUSER_ID

def pre_load_hook(cr):
    env = api.Environment(cr, SUPERUSER_ID, {})

    load_es_mx_lang(env)
    #load_taecel(env)


def post_load_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})

    load_es_mx_lang(env)
    #load_taecel(env)

def load_es_mx_lang(env):    
    lang = env['res.lang'].search([('code', '=', 'es_MX')], limit=1)
    
    if not lang:
        # Instalar idioma si no existe
        env['res.lang'].load_lang('es_MX')        
    else:
        lang.active = True

def load_taecel(env):
    taecel = env['taecel_product']
    taecel.getProducts()
