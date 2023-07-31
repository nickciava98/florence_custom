# -*- coding: utf-8 -*-
{
    'name': "Florence Amazon Financial Plan",
    'summary': "Florence customization for Amazon Financial Plan management",
    'license': 'OPL-1',
    'author': "Niccolò Ciavarella",
    'category': 'sales',
    'version': '14.1.2',
    'website': "https://www.nciavarella.me",
    'depends': [
        'base',
        'florence_manufacturing_costs',
        'florence_stock'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron.xml',
        'views/amazon_financial_plan_form.xml',
        'views/amazon_financial_plan_tree.xml',
        'views/amazon_financial_plan_search.xml',
        'views/amazon_financial_plan_tree.xml',
        'views/amazon_financial_plan_line_form.xml',
        'views/amazon_financial_plan_line_tree.xml',
        'views/amazon_financial_plan_values_form.xml',
        'views/amazon_financial_plan_values_tree.xml',
        'views/florence_financial_plan_form.xml',
        'views/florence_financial_plan_tree.xml',
        'views/florence_financial_plan_graph.xml',
        'views/florence_financial_plan_line_form.xml',
        'views/florence_fp_costs_form.xml',
        'views/florence_fp_costs_tree.xml',
        'views/florence_balance_sheet_form.xml',
        'views/florence_balance_sheet_tree.xml',
        'views/stock_location_form.xml',
        'views/florence_forecasting_views.xml',
        'views/amazon_financial_plan_actions.xml',
        'views/amazon_financial_plan_menus.xml',
        'views/amazon_archive_views.xml',
        'wizard/fp_costs_update_form.xml',
        'wizard/export_xlsx_views.xml',
        'data/server_action.xml'
    ],
    'application': False,
    'installable': True,
}
