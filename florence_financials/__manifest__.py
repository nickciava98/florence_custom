# -*- coding: utf-8 -*-
{
    "name": "Florence Financials",
    "summary": "Florence customizations for fiscal positions",
    "license": "OPL-1",
    "author": "Niccolò Ciavarella",
    "category": "sales",
    "version": "14.0.4",
    "website": "http://www.nciavarella.me",
    "depends": [
        "sale_management",
        "account_accountant",
        "stock",
        "florence_manufacturing_costs",
        "l10n_uk"
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/sale_order_template_form.xml",
        "views/sale_order_form.xml",
        "views/sale_order_tree.xml",
        "views/purchase_order_tree.xml",
        "views/purchase_order_form.xml",
        "views/product_portal_template.xml",
        "views/purchase_actions.xml",
        "wizards/link_bill_form.xml",
        "wizards/create_po_packaging_form.xml"
    ],
    "application": False,
    "installable": True,
}
