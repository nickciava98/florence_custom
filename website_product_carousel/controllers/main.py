from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_sale.controllers import main
from odoo import fields, http


def splits(length, numbers):
    for i in range(0, len(length), numbers):
        yield length[i:i + numbers]


class CarouselSnippet(http.Controller):

    def split_product_rows(self, product_row, objects):
        res = list(splits(objects, product_row))
        return res

    @http.route(['/render_product_carousel_slider/product_slider/'], type='json',
                auth='public', website=True, csrf=False, cache=600)
    def render_product_carousel_slider(self, product_view=False, filter_id=False, product_row=1, objects_in_slide=4,
                                       limit=10):

        res = request.env['product.template'].get_product_carousel_slider(filter_id=filter_id, limit=limit)
        pricelist_context = dict(request.env.context)
        pricelist = False
        if not pricelist_context.get('pricelist'):
            pricelist = request.website.get_current_pricelist()
            pricelist_context['pricelist'] = pricelist.id
        else:
            pricelist = request.env['product.pricelist'].browse(pricelist_context['pricelist'])

        from_currency = (res['all_products'][:1] or request.env.user.company_id).currency_id
        to_currency = pricelist.currency_id
        compute_currency = lambda price: from_currency._convert(price, to_currency, (
                res['all_products'][:1] or request.env.user).company_id,
                                                                fields.Date.today())

        request.context = dict(request.context, pricelist=pricelist.id, partner=request.env.user.partner_id)

        values = {
            'product_obj': self.split_product_rows(product_row, res['all_products']),
            'product_headline': res['name'],
            'compute_currency': compute_currency,
            'pricelist': pricelist,
        }
        return request.env['ir.ui.view']._render_template(product_view, values)
