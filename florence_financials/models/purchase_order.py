from odoo.exceptions import UserError

from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    related_invoice = fields.Char(
        compute="_compute_related_invoice"
    )

    @api.depends("invoice_ids")
    def _compute_related_invoice(self):
        for line in self:
            line.related_invoice = ""

            if len(line.invoice_ids) > 0:
                invoice_numbers = []

                for invoice in line.invoice_ids:
                    invoice_numbers.append(invoice.name)

                line.related_invoice = ", ".join(invoice_numbers)

    def open_link_bill_wizard_action(self):
        po_ids = []

        for po in self:
            po_ids.append(po.id)

        if len(po_ids) == 1:
            return {
                "name": "Link Bill",
                "type": "ir.actions.act_window",
                "res_model": "link.bill",
                "view_mode": "form",
                "view_type": "form",
                "context": {
                    "default_purchase_id": self.id
                },
                "views": [(False, "form")],
                "target": "new"
            }

        raise UserError(
            "You can only link bill to one Purchase Order!"
        )
