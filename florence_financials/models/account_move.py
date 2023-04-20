from odoo import models, fields


class AccountMove(models.Model):
    _inherit = "account.move"

    def unlink_action(self):
        po_id = int(self.env.context.get("po_id"))
        bill_id = int(self.env.context.get("bill_id"))

        self.env["purchase.order"].search(
            [("id", "=", po_id)]
        ).invoice_ids = [(3, bill_id)]
        self.env["purchase.order"].search(
            [("id", "=", po_id)]
        ).invoice_count -= 1

        self.env["purchase.order"].search(
            [("id", "=", po_id)]
        )._compute_related_invoice()
