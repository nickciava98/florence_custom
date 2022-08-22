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
    pcs = fields.Float()
    price_agreed = fields.Float()
    price_unit = fields.Float()
    price_finished = fields.Float()
    currency_id = fields.Many2one(
        "res.currency"
    )
