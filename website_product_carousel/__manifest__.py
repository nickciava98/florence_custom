{
    'name': 'Website Product Carousel Slider',
    'summary': 'Easily drag and drop Website Product Carousel and Quickly Configure our Product Carousel',
    'description': 'Easily drag and drop Website Product Carousel and Quickly Configure our Product Carousel',
    'category': 'Website/eCommerce',
    'version': '13.0.1.0.0',
    'author': 'Tecspek',
    'data': [
        'security/ir.model.access.csv',
        'data/product_filter_data.xml',
        'views/assets.xml',
        'views/carousel_snippet_options.xml',
        'views/website_filter_view.xml',
        'views/product_carousel.xml',
        'views/product_view.xml',
        'views/small_product_carousel.xml',
    ],
    'depends': [
        'website_sale',
        'rating',
        'website_sale_wishlist',
        'website_sale_comparison',
    ],
    'images': [
        'static/description/banner.png'
    ],
    'support': 'help.tecspek@gmail.com',
    'installable': True,
    'application': True,
    'auto_install': False,
    'price': 66,
    'license': 'OPL-1',
    'currency': 'EUR',
}
