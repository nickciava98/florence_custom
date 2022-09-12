# -*- coding: utf-8 -*-
{
    'name': "Florence Amazon Statistics",
    'summary': "Florence custom App for Amazon Statistics",
    'license': 'OPL-1',
    'author': "Niccolò Ciavarella",
    'category': 'sales',
    'version': '14.1.1',
    'website': "http://www.nciavarella.me",
    'depends': ['florence_amazon_revenues'],
    'data': [
        'security/ir.model.access.csv',
        'views/amazon_statistics_actions.xml',
        'views/amazon_statistics_form.xml',
        'views/amazon_statistics_tree.xml',
        'views/amazon_statistics_line_tree.xml',
        'views/amazon_statistics_line_graph.xml'
    ],
    'application': False,
    'installable': True,
}