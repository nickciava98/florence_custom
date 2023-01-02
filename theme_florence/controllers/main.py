import json

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class ThemePages(http.Controller):

    @http.route(['/gyik/'], type='http', auth='public', website=True, csrf=False)
    def faq_page(self, **post):
        return request.render("theme_florence.faq_page_template",{})

    @http.route(['/bio-minosites/'], type='http', auth='public', website=True, csrf=False)
    def bio_minosites(self, **post):
        return request.render("theme_florence.bio_minosites",{})
    #
    # @http.route(['/tt'], type='http', auth='public', website=True, csrf=False)
    # def bio_minosites(self, **post):
    #     return request.render("theme_florence.tt_template",{})
