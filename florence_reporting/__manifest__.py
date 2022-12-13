# -*- coding: utf-8 -*-
{
    'name': "Florence Reporting",
    'summary': "Florence customizations for reporting",
    'license': 'OPL-1',
    'author': "Niccolò Ciavarella",
    'category': 'sales',
    'version': '14.0.4',
    'website': "http://www.nciavarella.me",
    'depends': [
        'base',
        'sale',
        'sale_management',
        'account'
    ],
    'data': [
        'views/sale_order_form.xml',
        'views/sale_order_template_form.xml',
        'views/account_move_form.xml',
        'views/sale_order_tree.xml',
        'reports/sale_order_document.xml',
        'reports/account_invoice_document.xml',
        'reports/external_layout_boxed.xml'
    ],
    'application': False,
    'installable': True,
}