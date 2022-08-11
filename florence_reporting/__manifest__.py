# -*- coding: utf-8 -*-
{
    'name': "Florence Reporting",
    'summary': "Florence customizations for reporting",
    'license': 'OPL-1',
    'author': "Niccolò Ciavarella",
    'category': 'sales',
    'version': '14.0.3',
    'website': "http://www.nciavarella.me",
    'depends': ['sale', 'sale_management'],
    'data': ['views/sale_order_form.xml',
             'views/sale_order_template_form.xml',
             'reports/sale_order_document.xml'],
    'application': False,
    'installable': True,
}