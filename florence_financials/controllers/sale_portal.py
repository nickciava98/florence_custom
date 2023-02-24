from odoo import http, _
from odoo.http import request
from odoo.addons.sale.controllers.portal import CustomerPortal
from odoo.addons.portal.controllers.portal import pager as portal_pager


class SalePortal(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        domain_quotation = [("state", "in", ["draft", "sent"])]
        domain_order = [("state", "in", ["sale", "done"])]

        if "quotation_count" in counters:
            values["quotation_count"] = len(request.env["sale.order"].sudo().search(domain_quotation))
        if "order_count" in counters:
            values["order_count"] = len(request.env["sale.order"].sudo().search(domain_order))

        return values

    @http.route(["/my/quotes", "/my/quotes/page/<int:page>"], type="http", auth="user", website=True)
    def portal_my_quotes(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        domain = [("state", "in", ["draft", "sent"])]
        searchbar_sortings = self._get_sale_searchbar_sortings()

        if not sortby:
            sortby = "date"
            
        sort_order = searchbar_sortings[sortby]["order"]

        if date_begin and date_end:
            domain += [("create_date", ">", date_begin), ("create_date", "<=", date_end)]

        quotation_count = len(request.env["sale.order"].sudo().search(domain))
        pager = portal_pager(
            url = "/my/quotes",
            url_args = {"date_begin": date_begin, "date_end": date_end, "sortby": sortby},
            total = quotation_count,
            page = page,
            step = self._items_per_page
        )
        quotations = request.env["sale.order"].sudo().search(
            domain, order = sort_order, limit = self._items_per_page, offset = pager["offset"]
        )
        request.session["my_quotations_history"] = quotations.ids[:100]

        values.update({
            "date": date_begin,
            "quotations": quotations.sudo(),
            "page_name": "quote",
            "pager": pager,
            "default_url": "/my/quotes",
            "searchbar_sortings": searchbar_sortings,
            "sortby": sortby,
        })
        
        return request.render("sale.portal_my_quotations", values)

    @http.route(["/my/orders", "/my/orders/page/<int:page>"], type="http", auth="user", website=True)
    def portal_my_orders(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        domain = [("state", "in", ["sale", "done"])]
        searchbar_sortings = self._get_sale_searchbar_sortings()

        if not sortby:
            sortby = "date"

        sort_order = searchbar_sortings[sortby]["order"]

        if date_begin and date_end:
            domain += [("create_date", ">", date_begin), ("create_date", "<=", date_end)]

        order_count = len(request.env["sale.order"].sudo().search(domain))
        pager = portal_pager(
            url = "/my/orders",
            url_args = {"date_begin": date_begin, "date_end": date_end, "sortby": sortby},
            total = order_count,
            page = page,
            step = self._items_per_page
        )
        orders = request.env["sale.order"].sudo().search(
            domain, order = sort_order, limit = self._items_per_page, offset = pager["offset"]
        )
        request.session["my_orders_history"] = orders.ids[:100]

        values.update({
            "date": date_begin,
            "orders": orders,
            "page_name": "order",
            "pager": pager,
            "default_url": "/my/orders",
            "searchbar_sortings": searchbar_sortings,
            "sortby": sortby,
        })

        return request.render("sale.portal_my_orders", values)
    