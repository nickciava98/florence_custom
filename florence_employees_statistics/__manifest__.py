# -*- coding: utf-8 -*-
{
    'name': "Florence Employees Statistics",
    'summary': "Florence customizations for employees statistics tracking",
    'license': 'OPL-1',
    'author': "Niccolò Ciavarella",
    'category': 'Human Resources/Employees',
    'version': '14.0.4',
    'website': "http://www.nciavarella.me",
    'depends': [
        'base',
        'mail',
        'hr'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/employees_statistics_actions.xml',
        'views/employees_statistics_form.xml',
        'views/employees_statistics_menus.xml',
        'views/employees_statistics_search.xml',
        'views/employees_statistics_tree.xml',
        'views/employees_statistics_benchmark_form.xml',
        'views/employees_statistics_benchmark_tree.xml',
        'views/employees_statistics_line_graph.xml',
        'views/employees_statistics_line_tree.xml',
        'wizard/help_wizard.xml'
    ],
    'application': True,
    'installable': True,
}
