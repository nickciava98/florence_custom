from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = "account.move"

    is_manufacturing_bill = fields.Boolean(
        compute = "_compute_is_manufacturing_bill",
        store = True
    )

    def _compute_is_manufacturing_bill(self):
        for line in self:
            line.is_manufacturing_bill = False

            if len(line.invoice_line_ids) > 0:
                for invoice_line in line.invoice_line_ids:
                    line.is_manufacturing_bill = invoice_line.product_id.categ_id.is_manufacturing_product_category

                    if line.is_manufacturing_bill:
                        break
