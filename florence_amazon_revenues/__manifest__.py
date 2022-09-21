# -*- coding: utf-8 -*-
{
    'name': "Florence Amazon Revenues",
    'summary': "Florence custom App for Amazon Revenues computation",
    'license': 'OPL-1',
    'author': "Niccolò Ciavarella",
    'category': 'sales',
    'version': '14.2.3',
    'website': "http://www.nciavarella.me",
    'depends': ['mail', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/amazon_revenues_actions.xml',
        'views/amazon_revenues_form.xml',
        'views/amazon_revenues_menus.xml',
        'views/amazon_revenues_pivot.xml',
        'views/amazon_revenues_search.xml',
        'views/amazon_revenues_tree.xml',
        'views/amazon_revenues_line_graph.xml',
        'views/amazon_revenues_line_tree.xml',
        'wizard/help_wizard_amazon_revenues.xml'
    ],
    'application': True,
    'installable': True,
}