from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    discount = fields.Float(
        string="Discount (%)",
        digits=(12, 4),
        default=.0
    )
    price_total = fields.Float(
        compute="_compute_price_total",
        string="Total",
        digits=(12, 4)
    )

    @api.depends("price_unit", "product_uom_qty", "tax_id")
    def _compute_price_total(self):
        for line in self:
            tax_amount = sum([
                line.price_unit * line.product_uom_qty * tax.amount / 100 for tax in line.tax_id
            ]) if line.tax_id else .0
            line.price_total = (line.price_unit * line.product_uom_qty) + tax_amount
