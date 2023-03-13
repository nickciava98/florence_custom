# -*- coding: utf-8 -*-
{
    'name': "Florence Amazon Connector",
    'summary': "Florence customization for Amazon Connector",
    'license': 'OPL-1',
    'author': "Niccolò Ciavarella",
    'category': 'sales',
    'version': '14.0.1',
    'website': "http://www.nciavarella.me",
    'depends': [
        'sale_amazon'
    ],
    'data': [
        'views/amazon_connector_views.xml',
        'views/sale_order_views.xml'
    ],
    'application': False,
    'installable': True,
}
