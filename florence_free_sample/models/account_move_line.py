from odoo import models, fields, api

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    discount = fields.Float(
        string = "Discount (%)",
        digits = (16, 20),
        default = 0.0
    )
    total_price = fields.Float(
        compute = "_compute_total_price",
        string = "Total"
    )

    @api.depends("price_unit", "tax_ids", "quantity")
    def _compute_total_price(self):
        for line in self:
            total_tax = 0

            for tax in line.tax_ids:
                total_tax += line.price_unit * line.quantity * tax.amount / 100

            line.total_price = (line.price_unit * line.quantity) + total_tax
