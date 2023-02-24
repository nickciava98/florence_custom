from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.addons.account.controllers.portal import PortalAccount
from collections import OrderedDict


class AccountPortal(PortalAccount):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)

        if "invoice_count" in counters:
            domain = self._get_invoices_domain() + [("state", "!=", "cancel")]
            invoice_count = len(request.env["account.move"].sudo().search(domain))
            values["invoice_count"] = invoice_count

        return values

    @http.route(["/my/invoices", "/my/invoices/page/<int:page>"], type="http", auth="user", website=True)
    def portal_my_invoices(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw):
        values = self._prepare_portal_layout_values()
        domain = self._get_invoices_domain() + [("state", "!=", "cancel")]
        searchbar_sortings = {
            "date": {"label": _("Date"), "order": "invoice_date desc"},
            "duedate": {"label": _("Due Date"), "order": "invoice_date_due desc"},
            "name": {"label": _("Reference"), "order": "name desc"},
            "state": {"label": _("Status"), "order": "state"},
        }

        if not sortby:
            sortby = "date"

        order = searchbar_sortings[sortby]["order"]
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
            "invoices": {"label": _("Invoices"), "domain": [("move_type", "=", ("out_invoice", "out_refund"))]},
            "bills": {"label": _("Bills"), "domain": [("move_type", "=", ("in_invoice", "in_refund"))]},
        }

        if not filterby:
            filterby = "all"

        domain += searchbar_filters[filterby]["domain"]
        
        if date_begin and date_end:
            domain += [("create_date", ">", date_begin), ("create_date", "<=", date_end)]

        invoice_count = len(request.env["account.move"].sudo().search(domain))
        pager = portal_pager(
            url = "/my/invoices",
            url_args = {"date_begin": date_begin, "date_end": date_end, "sortby": sortby},
            total = invoice_count,
            page = page,
            step = self._items_per_page
        )
        invoices = request.env["account.move"].sudo().search(
            domain, order = order, limit = self._items_per_page, offset = pager["offset"]
        )
        request.session["my_invoices_history"] = invoices.ids[:100]
        
        values.update({
            "date": date_begin,
            "invoices": invoices,
            "page_name": "invoice",
            "pager": pager,
            "default_url": "/my/invoices",
            "searchbar_sortings": searchbar_sortings,
            "sortby": sortby,
            "searchbar_filters": OrderedDict(sorted(searchbar_filters.items())),
            "filterby": filterby,
        })

        return request.render("account.portal_my_invoices", values)
