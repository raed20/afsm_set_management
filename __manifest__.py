# -*- coding: utf-8 -*-
{
    'name': 'afsm_set_management',
   # Categories can be used to filter modules in modules listing
    'version': '17.0.0.1.0',
    # any module necessary for this one to work correctly
    'depends': ['base','sale'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/product_set_views.xml',
        'wizards/product_set_view.xml',
        'wizards/sale_product_set_wizard_view.xml',
    ],

    'demo': [
        # 'demo/demo.xml',
    ],

    'application': True,
    'installable': True,

}
