# -*- coding: utf-8 -*-
{
    'name': "Florence Controllers",
    'summary': "Florence customizations for quick creates and quick edits",
    'license': 'OPL-1',
    'author': "Niccolò Ciavarella",
    'category': '',
    'version': '14.1.3',
    'website': "http://www.nciavarella.me",
    'depends': [
        'base',
        'sale',
        'sale_management',
        'account',
        'florence_free_sample'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_form.xml',
        'views/account_move_form.xml',
        'views/purchase_order_form.xml',
        'wizard/help_wizard_sale_order.xml'
    ],
    'application': False,
    'installable': True,
}
