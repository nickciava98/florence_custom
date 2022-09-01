from odoo import models, fields, api


class AmazonRevenuesLine(models.Model):
    _name = "amazon.revenues.line"
    _description = "Amazon Revenues Line"

    # Invisible fields
    amazon_revenues_line_id = fields.Many2one(
        "amazon.revenues"
    )
    parent = fields.Char()
    product = fields.Many2one(
        "product.template"
    )

    # Visible fields
    date = fields.Date()
    price_unit = fields.Float()
    amazon_fees = fields.Float()
    taxes = fields.Float(
        compute="_compute_taxes",
        store=True
    )
    sku_cost = fields.Float(
        compute="_compute_sku_cost",
        store=True
    )
    gross_revenues = fields.Float(
        compute="_compute_gross_revenues",
        store=True
    )
    ads_total_cost = fields.Float()
    ads_cost_per_unit = fields.Float(
        compute="_compute_ads_cost_per_unit",
        store=True
    )
    pcs_sold = fields.Float()
    earned_per_pc = fields.Float(
        compute="_compute_earned_per_pc",
        store=True
    )
    probable_income = fields.Float(
        compute="_compute_probable_income",
        store=True
    )
    currency_id = fields.Many2one(
        "res.currency",
        compute="_compute_currency_id"
    )

    def _compute_currency_id(self):
        for line in self:
            line.currency_id = self.env.ref('base.main_company').currency_id

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
            for product in self.env["manufacturing.costs"].search(
                    [("super_product", "=", line.product.id)]):
                line.sku_cost = product.price_total_avg

                if line.sku_cost != 0:
                    break

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
