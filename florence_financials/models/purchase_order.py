from odoo import models, fields


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    related_invoice = fields.Char(
        compute = "_compute_related_invoice"
    )

    def _compute_related_invoice(self):
        for line in self:
            line.related_invoice = ""

            if len(line.invoice_ids) > 0:
                invoice_numbers = []

                for invoice in line.invoice_ids:
                    invoice_numbers.append(invoice.name)

                line.related_invoice = ", ".join(invoice_numbers)
