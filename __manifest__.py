# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Sindicato',
    'price' : '0.0',
    'currency' : 'EUR',
    'license' : 'LGPL-3',
    'images': ['static/description/logo.png'],    
    'author': "SolesGPS :: Eduardo Vizcaino",
    'category': 'fleet, GPS, Geolocation',
    "version": "18.0.0.0.1",
    'website' : 'https://solesgps.com',
    'summary' : 'Locate the satellite coordinates that your GPS devices throw. Save that information here and see it on the map.',
    'description' : """
Vehicle, leasing, insurances, cost
==================================
With this module, Odoo helps you managing all your vehicles, the
contracts associated to those vehicle as well as services, fuel log
entries, costs and many other features necessary to the management 
of your fleet of vehicle(s)

Main Features
-------------
* Add vehicles to your fleet
* Manage contracts for vehicles
* Reminder when a contract reach its expiration date
* Add services, fuel log entry, odometer values for all vehicles
* Show all costs associated to a vehicle or to a type of service
* Analysis graph for costs
""",
    'depends': [
        'mail',
        'portal',
        #'website',
        #'gpsmap',        
    ],
    #"pre_init_hook": "pre_load_hook",
    #"post_init_hook": "post_load_hook",
    'data': [
        #'data/ir_config_parameter.xml',
        #'data/ir_attachment.xml',
        
        #'data/fetchmail_server.xml',
        'data/eventos.xml',
        'data/res_company_data.xml',
        #'data/res_config_settings.xml',
        #"data/lang.xml",
        
        #'data/res_partner.xml',
        #'data/res_users.xml',
        
        'security/security.xml',
        'security/ir.model.access.csv',

        'views/asistencias.xml',
        'views/eventos.xml',
        'views/menuitem.xml',
        #'views/portal_menu_templates.xml',
        #'views/portal_layout.xml',
        'views/portal_credencial.xml',
        'views/portal_eventos.xml',
        'views/portal_familia.xml',
        #'views/views.xml',
        #'views/website_aboutus.xml',
        #'views/website_contactus_thanks.xml',
        #'views/website_contactus.xml',
        #'views/website_footer_custom.xml',
        #'views/homepage.xml',
    ],

    'installable': True,
    'application': True,
}
