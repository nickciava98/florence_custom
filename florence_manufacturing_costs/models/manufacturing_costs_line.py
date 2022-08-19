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
    price_finished = fields.Float(
        compute = "_compute_price_finished"
    )
    currency_id = fields.Many2one(
        "res.currency"
    )

    @api.depends("product")
    def _compute_price_finished(self):
        for line in self:
            line.price_finished = 1.22 * line.price_unit

    #
    # @api.depends("product")
    # def _compute_manufacturer(self):
    #     for line in self:
    #         line.manufacturer = False
    #
    #         for seller in line.product.seller_ids:
    #             if seller.name:
    #                 line.manufacturer = seller.name.name
    #
    # @api.depends("product")
    # def _compute_pcs(self):
    #     for line in self:
    #         line.pcs = 0
    #
    #         for seller in line.product.seller_ids:
    #             if seller.min_qty:
    #                 line.pcs += seller.min_qty
    #
    # @api.depends("product")
    # def _compute_price_unit(self):
    #     for line in self:
    #         line.price_unit = 0
    #
    #         for seller in line.product.seller_ids:
    #             if seller.price:
    #                 line.price_unit = seller.price