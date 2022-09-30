# -*- coding: utf-8 -*-
{
    'name': "Florence Amazon Reporting",
    'summary': "Florence customization for Amazon Reporting management",
    'license': 'OPL-1',
    'author': "Niccolò Ciavarella",
    'category': 'sales',
    'version': '14.0.1',
    'website': "http://www.nciavarella.me",
    'depends': ['base', 'florence_amazon_revenues'],
    'data': [
        'security/ir.model.access.csv',
        'views/amazon_revenues_reporting_actions.xml',
        'views/amazon_revenues_reporting_form.xml',
        'views/amazon_revenues_reporting_menus.xml',
        'views/amazon_revenues_reporting_search.xml',
        'views/amazon_revenues_reporting_tree.xml'
    ],
    'application': False,
    'installable': True,
}
