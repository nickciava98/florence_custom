from odoo import models, fields, api
from datetime import datetime

class ManufacturingCostsLine(models.Model):
    _name = "manufacturing.costs.line"
    _description = "Manufacturing Costs Line"

    manufacturing_costs_line_id = fields.Many2one(
        "manufacturing.costs",
        ondelete = "cascade"
    )
    product = fields.Many2one(
        "product.product"
    )
    bill = fields.Many2one(
        "account.move"
    )
    bill_date = fields.Date()
    date = fields.Date()
    manufacturer = fields.Char()
    pcs_invoiced = fields.Float(
        digits = (12, 4)
    )
    price_invoiced = fields.Float(
        group_operator = "avg",
        digits = (12, 4)
    )
    price_packaging = fields.Float(
        group_operator = "avg",
        digits = (12, 4)
    )
    price_total = fields.Float(
        compute = "_compute_price_total",
        store = True,
        group_operator = "avg",
        digits = (12, 4)
    )
    price_public = fields.Float(
        group_operator = "avg",
        digits = (12, 4)
    )
    other_costs = fields.Float(
        group_operator = "avg",
        digits = (12, 4)
    )
    currency_id = fields.Many2one(
        "res.currency",
        compute = "_compute_currency_id"
    )

    def _compute_currency_id(self):
        for line in self:
            line.currency_id = self.env.ref('base.main_company').currency_id

    @api.depends("price_invoiced", "price_packaging", "other_costs")
    def _compute_price_total(self):
        for line in self:
            line.price_total = line.price_invoiced + line.price_packaging + line.other_costs
