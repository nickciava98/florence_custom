from odoo import models, fields, api
from datetime import datetime, timedelta
import locale


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
    week = fields.Char(
        compute = "_compute_week",
        store = True
    )
    price_unit = fields.Float(
        group_operator = "avg"
    )
    amazon_fees = fields.Float()
    taxes = fields.Float(
        compute = "_compute_taxes",
        store = True
    )
    sku_cost = fields.Float(
        group_operator = "avg"
    )
    gross_revenues = fields.Float(
        compute = "_compute_gross_revenues",
        store = True
    )
    ads_total_cost = fields.Float()
    ads_cost_per_unit = fields.Float(
        compute = "_compute_ads_cost_per_unit",
        store = True,
        group_operator = "avg"
    )
    pcs_sold = fields.Float()
    earned_per_pc = fields.Float(
        compute = "_compute_earned_per_pc",
        store = True,
        group_operator = "avg"
    )
    probable_income = fields.Float(
        compute = "_compute_probable_income",
        store = True,
        string = "Probable Income (Odoo)"
    )
    probable_income_amz = fields.Float(
        compute = "_compute_probable_income_amz",
        store = True,
        string = "Probable Income (Amazon)"
    )
    currency_id = fields.Many2one(
        "res.currency",
        compute = "_compute_currency_id"
    )

    @api.depends("date")
    def _compute_week(self):
        locale.setlocale(locale.LC_TIME, "en_US.UTF-8")

        for line in self:
            line.week = ""

            if line.date:
                dt = datetime.strptime(str(line.date), "%Y-%m-%d")
                start = dt - timedelta(days = dt.weekday())
                end = start + timedelta(days = 6)

                line.week = start.strftime("%d") + "-" + end.strftime("%d") + " " \
                            + datetime.strptime(str(line.date), "%Y-%m-%d").strftime("%B") \
                            + " " + str(datetime.strptime(str(line.date), "%Y-%m-%d").year)

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
