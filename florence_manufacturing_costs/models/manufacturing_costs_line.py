from odoo import models, fields, api

class ManufacturingCostsLine(models.Model):
    _name = "manufacturing.costs.line"
    _description = "Manufacturing Costs Line"

    manufacturing_costs_line_id = fields.Many2one(
        "manufacturing.costs"
    )
    product = fields.Many2one(
        "product.product"
    )
    date = fields.Date()
    manufacturer = fields.Char()
    pcs_invoiced = fields.Float()
    price_invoiced = fields.Float()
    price_packaging = fields.Float()
    price_total = fields.Float()
    price_public = fields.Float()
    other_costs = fields.Float()
    currency_id = fields.Many2one(
        "res.currency",
        compute = "_compute_currency_id"
    )

    def _compute_currency_id(self):
        for line in self:
            line.currency_id = self.env.ref('base.main_company').currency_id
