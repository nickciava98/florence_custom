from odoo import models, fields, api

class AmazonRevenuesLine(models.Model):
    _name = "amazon.revenues.line"
    _description = "Amazon Revenues Line"

    #Invisible fields
    amazon_revenues_line_id = fields.Many2one(
        "amazon.revenues"
    )
    parent = fields.Char()
    product = fields.Many2one(
        "product.product"
    )

    #Visible fields
    date = fields.Date()
    price_unit = fields.Float()
    amazon_fees = fields.Float()
    taxes = fields.Float(
        compute = "_compute_taxes"
    )
    sku_cost = fields.Float(
        compute = "_compute_sku_cost"
    )
    gross_revenues = fields.Float(
        compute = "_compute_gross_revenues"
    )
    ads_total_cost = fields.Float()
    ads_cost_per_unit = fields.Float(
        compute = "_compute_ads_cost_per_unit"
    )
    pcs_sold = fields.Float()
    earned_per_pc = fields.Float(
        compute = "_compute_earned_per_pc"
    )
    probable_income = fields.Float(
        compute = "_compute_probable_income"
    )

    @api.depends("price_unit")
    def _compute_taxes(self):
        for line in self:
            if line.parent == "IT":
                line.taxes = 0.22 * line.price_unit
            elif line.parent == "FR" or line.parent == "UK":
                line.taxes = 0.2 * line.price_unit
            elif line.parent == "DE":
                line.taxes = 0.19 * line.price_unit
            elif line.parent == "ES":
                line.taxes = 0.21 * line.price_unit
            else:
                line.taxes = 0

    @api.depends("product")
    def _compute_sku_cost(self):
        for line in self:
            line.sku_cost = 0

            for seller in line.product.seller_ids:
                line.sku_cost += seller.price

    @api.depends("price_unit", "amazon_fees", "taxes", "sku_cost")
    def _compute_gross_revenues(self):
        for line in self:
            line.gross_revenues = line.price_unit - line.amazon_fees - line.taxes - line.sku_cost

    @api.depends("pcs_sold")
    def _compute_ads_cost_per_unit(self):
        for line in self:
            if line.pcs_sold != 0:
                line.ads_cost_per_unit = line.ads_total_cost / line.pcs_sold
            else:
                line.ads_cost_per_unit = 0

    @api.depends("gross_revenues", "ads_cost_per_unit")
    def _compute_earned_per_pc(self):
        for line in self:
            line.earned_per_pc = line.gross_revenues - line.ads_cost_per_unit

    @api.depends("earned_per_pc", "pcs_sold")
    def _compute_probable_income(self):
        for line in self:
            line.probable_income = line.earned_per_pc * line.pcs_sold
