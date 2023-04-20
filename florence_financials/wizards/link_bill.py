from odoo import models, fields


class LinkBill(models.Model):
    _name = "link.bill"
    _description = "Link Bill"

    purchase_id = fields.Many2one(
        "purchase.order",
        ondelete = "cascade",
        string = "Purchase Order"
    )
    bill_ids = fields.Many2many(
        "account.move",
        "link_bill_account_move_rel",
        domain = "[('move_type', 'in', ['in_invoice', 'in_refund', 'in_receipt'])]",
        string = "Vendor Bill"
    )

    def link_bill_action(self):
        if len(self.bill_ids) > 0:
            original_invoice_ids = self.purchase_id.invoice_ids
            new_invoice_ids = []

            if len(self.bill_ids) > 0 and len(original_invoice_ids) > 0:
                for inv in original_invoice_ids:
                    new_invoice_ids.append(inv.id)

                for bill in self.bill_ids:
                    new_invoice_ids.append(bill.id)
            elif len(self.bill_ids) > 0 and len(original_invoice_ids) == 0:
                new_invoice_ids = [bill.id for bill in self.bill_ids]

            if len(new_invoice_ids) > 0:
                self.purchase_id.sudo().write({
                    "invoice_ids": [(6, 0, new_invoice_ids)],
                    "invoice_count": len(new_invoice_ids)
                })
                self.purchase_id._compute_related_invoice()
