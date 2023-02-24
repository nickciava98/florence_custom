from odoo import http, _
from odoo.http import request
from odoo.addons.purchase.controllers.portal import CustomerPortal
from odoo.addons.portal.controllers.portal import pager as portal_pager
from collections import OrderedDict


class PurchasePortal(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        domain = [("state", "in", ["purchase", "done"])]

        if "purchase_count" in counters:
            values["purchase_count"] = len(request.env["purchase.order"].sudo().search(domain))

        return values

    @http.route(["/my/purchase", "/my/purchase/page/<int:page>"], type="http", auth="user", website=True)
    def portal_my_purchase_orders(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw):
        values = self._prepare_portal_layout_values()
        domain = []

        if date_begin and date_end:
            domain += [("create_date", ">", date_begin), ("create_date", "<=", date_end)]

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc, id desc"},
            "name": {"label": _("Name"), "order": "name asc, id asc"},
            "amount_total": {"label": _("Total"), "order": "amount_total desc, id desc"},
        }

        if not sortby:
            sortby = "date"

        order = searchbar_sortings[sortby]["order"]
        searchbar_filters = {
            "all": {"label": _("All"), "domain": [("state", "in", ["purchase", "done"])]},
            "purchase": {"label": _("Purchase Order"), "domain": [("state", "=", "purchase")]},
            "done": {"label": _("Locked"), "domain": [("state", "=", "done")]},
        }

        if not filterby:
            filterby = "all"

        domain += searchbar_filters[filterby]["domain"]
        purchase_count = len(request.env["purchase.order"].sudo().search(domain))
        pager = portal_pager(
            url = "/my/purchase",
            url_args = {"date_begin": date_begin, "date_end": date_end, "sortby": sortby, "filterby": filterby},
            total = purchase_count,
            page = page,
            step = self._items_per_page
        )
        orders = request.env["purchase.order"].sudo().search(
            domain, order = order, limit = self._items_per_page, offset = pager["offset"]
        )
        request.session["my_purchases_history"] = orders.ids[:100]

        values.update({
            "date": date_begin,
            "orders": orders,
            "page_name": "purchase",
            "pager": pager,
            "searchbar_sortings": searchbar_sortings,
            "sortby": sortby,
            "searchbar_filters": OrderedDict(sorted(searchbar_filters.items())),
            "filterby": filterby,
            "default_url": "/my/purchase",
        })

        return request.render("purchase.portal_my_purchase_orders", values)
