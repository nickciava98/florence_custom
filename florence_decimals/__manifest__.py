# -*- coding: utf-8 -*-
{
    'name': "Florence Decimals",
    'summary': "Florence customizations for decimal accuracy",
    'license': 'OPL-1',
    'author': "Niccolò Ciavarella",
    'category': 'sales',
    'version': '14.1',
    'website': "http://www.nciavarella.me",
    'depends': ['base', 'sale', 'sale_management', 'account'],
    'data': ['views/sale_order_form.xml',
             'views/account_move_form.xml',
             'reports/sale_order_document.xml',
             'reports/report_invoice_document.xml'],
    'application': False,
    'installable': True,
}