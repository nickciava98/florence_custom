# -*- coding: utf-8 -*-
{
    'name': "Florence Free Sample",
    'summary': "Florence customizations for free samples management",
    'license': 'OPL-1',
    'author': "Niccolò Ciavarella",
    'category': 'sales',
    'version': '14.1',
    'website': "http://www.nciavarella.me",
    'depends': ['base', 'sale', 'sale_management', 'account'],
    'data': ['views/sale_order_form.xml',
             'views/sale_order_template_form.xml',
             'views/account_move_form.xml',
             'reports/sale_order_document.xml',
             'reports/account_invoice_document.xml'],
    'application': False,
    'installable': True,
}