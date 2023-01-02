{
    'name': "Click Funnel Webhooks for Sale",

    'summary': """
        Click Funnel Webhooks for Sale
    """,

    'description': """
        Click Funnel Webhooks for Sale
    """,

    'author': "LevelPrime",
    'website': "https://levelprime.com",

    'category': 'Sale',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'account',
        'account_payment',
        'sale',
        'stock',
        'partner_firstname',    # OCA/partner-contact
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/click_funnel.xml',
        'views/product.xml',
        'views/sale.xml',
    ],
}
