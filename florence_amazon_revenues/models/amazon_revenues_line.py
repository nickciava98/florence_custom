from odoo import models, fields, api


class AmazonRevenuesLine(models.Model):
    _name = "amazon.revenues.line"
    _description = "Amazon Revenues Line"

    # Invisible fields
    amazon_revenues_line_id = fields.Many2one(
        "amazon.revenues",
        ondelete = "cascade"
    )
    amazon_revenues_line_id_test = fields.Many2one(
        "amazon.revenues",
        ondelete = "cascade"
    )
    parent = fields.Char()
    product = fields.Many2one(
        "product.template"
    )

    # Visible fields
    date = fields.Date()
    price_unit = fields.Float(
        group_operator = "avg",
        digits = (12, 4)
    )
    amazon_fees = fields.Float(
        digits = (12, 4)
    )
    taxes = fields.Float(
        compute = "_compute_taxes",
        store = True,
        digits = (12, 4)
    )
    sku_cost = fields.Float(
        group_operator = "avg",
        digits = (12, 4)
    )
    gross_revenues = fields.Float(
        compute = "_compute_gross_revenues",
        store = True,
        digits = (12, 4)
    )
    ads_total_cost = fields.Float(
        digits = (12, 4)
    )
    ads_cost_per_unit = fields.Float(
        compute = "_compute_ads_cost_per_unit",
        store = True,
        group_operator = "avg",
        digits = (12, 4)
    )
    pcs_sold = fields.Float(
        digits = (12, 4)
    )
    earned_per_pc = fields.Float(
        compute = "_compute_earned_per_pc",
        store = True,
        group_operator = "avg",
        digits = (12, 4)
    )
    probable_income = fields.Float(
        compute = "_compute_probable_income",
        store = True,
        string = "Probable Income (Odoo)",
        digits = (12, 4)
    )
    probable_income_amz = fields.Float(
        compute = "_compute_probable_income_amz",
        store = True,
        string = "Probable Income (Amazon)",
        digits = (12, 4)
    )
    currency_id = fields.Many2one(
        "res.currency",
        compute = "_compute_currency_id"
    )

    @api.depends("probable_income", "sku_cost")
    def _compute_probable_income_amz(self):
        for line in self:
            line.probable_income_amz = 0

            if line.probable_income and line.sku_cost:
                line.probable_income_amz = line.probable_income + line.pcs_sold * line.sku_cost

    def _compute_currency_id(self):
        for line in self:
            line.currency_id = self.env.ref('base.main_company').currency_id

    @api.depends("price_unit")
    def _compute_taxes(self):
        for line in self:
            line.taxes = 0

            if line.parent == "IT":
                line.taxes = line.price_unit * 0.180327868852459
            elif line.parent == "FR" or line.parent == "UK":
                line.taxes = line.price_unit * 0.166666666666667
            elif line.parent == "DE":
                line.taxes = line.price_unit * 0.159663865546218
            elif line.parent == "ES":
                line.taxes = line.price_unit * 0.173553719008264

    @api.depends("price_unit", "amazon_fees", "taxes", "sku_cost")
    def _compute_gross_revenues(self):
        for line in self:
            line.gross_revenues = line.price_unit - line.amazon_fees - line.taxes - line.sku_cost

    @api.depends("ads_total_cost", "pcs_sold")
    def _compute_ads_cost_per_unit(self):
        for line in self:
            line.ads_cost_per_unit = 0

            if line.pcs_sold != 0:
                line.ads_cost_per_unit = line.ads_total_cost / line.pcs_sold

    @api.depends("gross_revenues", "ads_cost_per_unit")
    def _compute_earned_per_pc(self):
        for line in self:
            line.earned_per_pc = line.gross_revenues - line.ads_cost_per_unit

    @api.depends("earned_per_pc", "pcs_sold")
    def _compute_probable_income(self):
        for line in self:
            line.probable_income = line.earned_per_pc * line.pcs_sold
