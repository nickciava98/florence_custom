# -*- coding: utf-8 -*-
{
    'name': "Florence Amazon Statistics",
    'summary': "Florence custom App for Amazon Statistics",
    'license': 'OPL-1',
    'author': "Niccolò Ciavarella",
    'category': 'sales',
    'version': '14.2',
    'website': "http://www.nciavarella.me",
    'depends': ['base', 'mail', 'stock',
                'florence_amazon_revenues', 'board'],
    'data': [
        'security/ir.model.access.csv',
        'views/amazon_statistics_actions.xml',
        'views/amazon_statistics_form.xml',
        'views/amazon_statistics_tree.xml',
        'views/amazon_statistics_line_tree.xml',
        'views/amazon_statistics_line_graph.xml',
        'views/amazon_statistics_line_pivot.xml',
        'views/amazon_statistics_line_dashboard.xml',
        'wizard/help_wizard.xml'
    ],
    'application': False,
    'installable': True,
}