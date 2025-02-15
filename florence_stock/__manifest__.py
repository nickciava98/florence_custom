# -*- coding: utf-8 -*-
{
    'name': "Florence Stock",
    'summary': "Florence customizations for stock",
    'license': 'OPL-1',
    'author': "Niccolò Ciavarella",
    'category': 'stock',
    'version': '14.0.10',
    'website': "http://www.nciavarella.me",
    'depends': [
        'base',
        'stock',
        'stock_account',
        'purchase_stock'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_form.xml',
        'views/product_template_search.xml',
        'views/product_product_form.xml',
        'views/product_variant_form.xml',
        'views/stock_quant_history.xml',
        'views/account_move_form.xml',
        'views/stock_quant_tree.xml',
        'views/product_sku_form.xml',
        'views/product_sku_tree.xml',
        'views/stock_actions.xml',
        'views/stock_move_tree.xml',
        'views/stock_picking_form.xml',
        'views/purchase_order_form.xml'
    ],
    'application': False,
    'installable': True,
}
