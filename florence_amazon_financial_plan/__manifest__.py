# -*- coding: utf-8 -*-
{
    'name': "Florence Amazon Financial Plan",
    'summary': "Florence customization for Amazon Financial Plan management",
    'license': 'OPL-1',
    'author': "Niccolò Ciavarella",
    'category': 'sales',
    'version': '14.0.4',
    'website': "http://www.nciavarella.me",
    'depends': ['base', 'florence_amazon_revenues'],
    'data': [
        'security/ir.model.access.csv',
        'views/amazon_financial_plan_actions.xml',
        'views/amazon_financial_plan_form.xml',
        'views/amazon_financial_plan_tree.xml',
        'views/amazon_financial_plan_menus.xml',
        'views/amazon_financial_plan_search.xml',
        'views/amazon_financial_plan_tree.xml',
        'views/amazon_financial_plan_line_form.xml',
        'views/amazon_financial_plan_line_tree.xml',
        'views/amazon_financial_plan_values_form.xml',
        'views/amazon_financial_plan_values_tree.xml',
        'views/florence_financial_plan_form.xml',
        'views/florence_financial_plan_tree.xml',
        'views/florence_financial_plan_graph.xml'
    ],
    'application': False,
    'installable': True,
}
