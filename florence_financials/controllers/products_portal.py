from collections import OrderedDict

from odoo.http import request

from odoo import http, _
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


class ProductsPortal(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)

        if "product_count" in counters:
            domain = [("location_id", "in", request.env["stock.location"].sudo().search(
                [("is_valuable_stock", "=", True)]
            ).ids)]
            product_count = len(request.env["stock.quant"].sudo().search(domain))
            values["product_count"] = product_count

        return values

    @http.route(["/my/products", "/my/products/page/<int:page>"], type="http", auth="user", website=True)
    def portal_products(self, page=1, sortby=None, filterby=None, **kw):
        values = self._prepare_portal_layout_values()
        domain = [("location_id", "in", request.env["stock.location"].sudo().search(
            [("is_valuable_stock", "=", True)]
        ).ids)]
        searchbar_sortings = {
            "product": {"label": _("Product"), "order": "product_id asc"},
            "location": {"label": _("Location"), "order": "location_id asc"}
        }

        if not sortby:
            sortby = "product"

        order = searchbar_sortings[sortby]["order"]
        lfa_i_stock = request.env["stock.location"].sudo().search([("complete_name", "=", "LFA I/Stock")])
        lfa_i_stock_nv = request.env["stock.location"].sudo().search(
            [("complete_name", "=", "LFA I/Stock-NonVendibile")])
        offli_stock = request.env["stock.location"].sudo().search([("complete_name", "=", "OFFLI/Stock")])
        biona_stock = request.env["stock.location"].sudo().search([("complete_name", "=", "BIONA/Stock")])
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
            "lfa_i_stock": {"label": _("LFA I/Stock"), "domain": [("location_id", "=", lfa_i_stock.id)]},
            "lfa_i_stock_nv": {"label": _("LFA I/Stock-NonVendibile"),
                               "domain": [("location_id", "=", lfa_i_stock_nv.id)]},
            "offli_stock": {"label": _("OFFLI/Stock"), "domain": [("location_id", "=", offli_stock.id)]},
            "biona_stock": {"label": _("BIONA/Stock"), "domain": [("location_id", "=", biona_stock.id)]}
        }

        if not filterby:
            filterby = "all"

        domain += searchbar_filters[filterby]["domain"]
        product_count = len(request.env["stock.quant"].sudo().search(domain))
        pager = portal_pager(
            url="/my/products",
            url_args={"sortby": sortby},
            total=product_count,
            page=page,
            step=self._items_per_page
        )
        products = request.env["stock.quant"].sudo().search(
            domain, order=order, limit=self._items_per_page, offset=pager["offset"]
        )
        request.session["my_products_history"] = products.ids[:100]

        values.update({
            "products": products,
            "page_name": "product",
            "pager": pager,
            "default_url": "/my/products",
            "searchbar_sortings": searchbar_sortings,
            "sortby": sortby,
            "searchbar_filters": OrderedDict(sorted(searchbar_filters.items())),
            "filterby": filterby,
        })

        return request.render("florence_financials.portal_my_products", values)
