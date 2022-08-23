# -*- coding: utf-8 -*-
{
    'name': "Florence Manufacturing Costs",
    'summary': "Florence customizations for manufacturing costs tracking",
    'license': 'OPL-1',
    'author': "Niccolò Ciavarella",
    'category': 'inventory',
    'version': '14.0.2',
    'website': "http://www.nciavarella.me",
    'depends': ['mail', 'sale', 'sale_management',
                'purchase', 'stock', 'mrp', 'account'],
    'data': ['security/ir.model.access.csv',
             'views/account_move_form.xml',
             'views/manufacturing_costs_actions.xml',
             'views/manufacturing_costs_form.xml',
             'views/manufacturing_costs_menus.xml',
             'views/manufacturing_costs_pivot.xml',
             'views/manufacturing_costs_search.xml',
             'views/manufacturing_costs_tree.xml'],
    'application': True,
    'installable': True,
}
