# -*- coding: utf-8 -*-
{
    'name': "bulk_sms",

    'summary': """
        Ce module permet d'envoyer des SMS de masse""",

    'description': """
        Long description of module's purpose
    """,

    'author': "MT Consulting and Services",
    'website': "http://mtconsultingandservices.com/",
    'Phone': "+237 697 00 56 49 / 678 12 81 20",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        #'views/views.xml',
        #'views/templates.xml',
         'views/bulk_sms_views.xml',
         'views/locataire_views.xml',
         'menu_bulk_sms.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    
    'application': True
    
}
