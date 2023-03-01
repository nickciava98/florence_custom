# -*- coding: utf-8 -*-
{
    'name': "Florence Financials",
    'summary': "Florence customizations for fiscal positions",
    'license': 'OPL-1',
    'author': "Niccolò Ciavarella",
    'category': 'sales',
    'version': '14.0.4',
    'website': "http://www.nciavarella.me",
    'depends': [
        'sale_management',
        'account_accountant',
        'stock'
    ],
    'data': [
        'views/sale_order_template_form.xml',
        'views/sale_order_form.xml',
        'views/sale_order_tree.xml',
        'views/purchase_order_tree.xml',
        'views/purchase_order_form.xml',
        'views/product_portal_template.xml'
    ],
    'application': False,
    'installable': True,
}