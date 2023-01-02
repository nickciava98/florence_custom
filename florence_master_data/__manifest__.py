{
    'name': 'Florence Master Data',
    'summary': 'Florence Master Data',
    'description': 'Florence Master Data',
    'category': 'Account',
    'version': '14.0.1.0.0',
    'author': "LevelPrime",
    'website': "https://levelprime.com",
    'data': [
        'views/account_journal.xml',
        'views/account_template.xml',
        'views/sale_order_template.xml',
        'views/sale_view.xml',
        'views/account_move.xml',
        'views/delivery_note.xml',
    ],
    'depends': [
        'account','sale','l10n_it_delivery_note'
    ],
    'images': ['static/description/signature.png'],

    'installable': True,
    'application': True,
    'auto_install': False,
}
