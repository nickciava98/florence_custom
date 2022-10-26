from odoo import models, fields, api
import datetime
import itertools
import operator


class AmazonFinancialPlan(models.Model):
    _name = "amazon.financial.plan"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Amazon Financial Plan"

    name = fields.Char(
        required = True
    )
    date = fields.Date(
        default = datetime.datetime.now(),
        required = True
    )
    currency_id = fields.Many2one(
        "res.currency",
        compute = "_compute_currency_id"
    )
    total_value = fields.Float(
        compute = "_compute_total_value",
        store = True
    )
    total_used = fields.Float(
        compute = "_compute_total_used",
        store = True
    )
    total_to_use = fields.Float(
        compute = "_compute_total_to_use",
        store = True
    )
    amazon_financial_plan_values = fields.One2many(
        "amazon.financial.plan.values",
        "name",
        readonly = True,
        ondelete = "cascade"
    )
    amazon_financial_plan_lines = fields.One2many(
        "amazon.financial.plan.line",
        "name",
        ondelete = "cascade"
    )

    def update_fp_values_action(self):
        for line in self:
            line.amazon_financial_plan_values = [(6, 0, 0)]
            products = []

            for fp_line in self.env["amazon.financial.plan.line"].search([]):
                products.append(
                    (fp_line.product_id.id,
                     fp_line.value if fp_line.value_used else 0,
                     fp_line.value if not fp_line.value_used else 0)
                )

            products_grouped = []
            totals_used = []
            totals_to_use = []

            for product in products:
                if product[0] not in products_grouped:
                    products_grouped.append(product[0])

            for pg in products_grouped:
                total_used = 0
                total_to_use = 0

                for p in products:
                    if p[0] == pg:
                        total_used += p[1]
                        total_to_use += p[2]

                totals_used.append(total_used)
                totals_to_use.append(total_to_use)

            res = []

            for product in products_grouped:
                res.append((
                    0, 0, {
                        'name': line.id,
                        'product_id': product,
                        'total_used': totals_used[products_grouped.index(product)],
                        'total_to_use': totals_to_use[products_grouped.index(product)]
                    }
                ))

            self.write({
                'amazon_financial_plan_values': res
            })

    @api.depends("amazon_financial_plan_lines")
    def _compute_total_value(self):
        for line in self:
            line.total_value = 0

            for fp in line.amazon_financial_plan_lines:
                line.total_value += fp.value

    @api.depends("amazon_financial_plan_lines")
    def _compute_total_used(self):
        for line in self:
            line.total_used = 0

            for fp in line.amazon_financial_plan_lines:
                if fp.value_used:
                    line.total_used += fp.value

    @api.depends("amazon_financial_plan_lines")
    def _compute_total_to_use(self):
        for line in self:
            line.total_to_use = 0

            for fp in line.amazon_financial_plan_lines:
                if not fp.value_used:
                    line.total_to_use += fp.value

    def _compute_currency_id(self):
        for line in self:
            line.currency_id = self.env.ref('base.main_company').currency_id
