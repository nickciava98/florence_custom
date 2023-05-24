# -*- coding: utf-8 -*-
{
    'name': "Florence Util",
    'summary': "Florence customizations for utils tracking",
    'license': 'OPL-1',
    'author': "Niccolò Ciavarella",
    'category': 'inventory',
    'version': '14.0.1',
    'website': "http://www.nciavarella.me",
    'depends': [
        'florence_amazon_financial_plan',
        'florence_stock'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/utils_utils_form.xml',
        'views/utils_utils_tree.xml',
        'views/utils_utils_actions.xml'
    ],
    'application': True,
    'installable': True,
}
