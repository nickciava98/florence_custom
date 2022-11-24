from odoo import models, fields, api
import datetime


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
        store = True,
        digits = (12, 4)
    )
    total_used = fields.Float(
        compute = "_compute_total_used",
        store = True,
        digits = (12, 4)
    )
    total_to_use = fields.Float(
        compute = "_compute_total_to_use",
        store = True,
        digits = (12, 4)
    )
    amazon_financial_plan_values = fields.One2many(
        "amazon.financial.plan.values",
        "name",
        readonly = True
    )
    updated_fp_values = fields.Boolean(
        default = False
    )
    amazon_current_fp_values = fields.One2many(
        "amazon.financial.plan.values",
        "current_name",
        readonly = True
    )
    amazon_financial_plan_more_values = fields.One2many(
        "amazon.financial.plan.more.values",
        "name",
        readonly = True
    )
    amazon_current_fp_more_values = fields.One2many(
        "amazon.financial.plan.more.values",
        "current_name",
        readonly = True
    )
    amazon_financial_plan_lines = fields.One2many(
        "amazon.financial.plan.line",
        "name",
        copy = True
    )
    amazon_financial_plan_more_lines = fields.One2many(
        "amazon.financial.plan.more",
        "name",
        copy = True
    )

    @api.onchange("date")
    def _onchange_date(self):
        for line in self:
            if line.date:
                for fp_line in line.amazon_financial_plan_lines:
                    fp_line.date = line.date

    def update_fp_values_action(self):
        for line in self:
            ### UPDATE AMZ FP VALUES ###

            line.amazon_financial_plan_values = [(5, 0, 0)]
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

            for product in products_grouped:
                self.write({
                    'amazon_financial_plan_values': [(
                        0, 0, {
                            'name': line.id,
                            'product_id': product,
                            'total_used': totals_used[products_grouped.index(product)],
                            'total_to_use': totals_to_use[products_grouped.index(product)]
                        }
                    )]
                })

            ### UPDATE AMZ CURRENT FP VALUES ###

            line.amazon_current_fp_values = [(5, 0, 0)]
            products = []
            totals_to_use = []
            totals_used = []

            for fp_line in line.amazon_financial_plan_lines:
                products.append(fp_line.product_id.id)

                if fp_line.value_used:
                    totals_used.append(fp_line.value)
                    totals_to_use.append(0)
                else:
                    totals_used.append(0)
                    totals_to_use.append(fp_line.value)

            products_grouped = []

            for product in products:
                if product not in products_grouped:
                    products_grouped.append(product)

            for product in products_grouped:
                self.write({
                    'amazon_current_fp_values': [(
                        0, 0, {
                            'name': line.id,
                            'product_id': product,
                            'total_used': totals_used[products_grouped.index(product)],
                            'total_to_use': totals_to_use[products_grouped.index(product)]
                        }
                    )]
                })

            ### UPDATE AMZ FP MORE VALUES (VENDORS) ###

            line.amazon_financial_plan_more_values = [(5, 0, 0)]
            vendors = []

            for fp_line in self.env["amazon.financial.plan.more"].search([]):
                vendors.append(
                    (fp_line.vendor.id,
                     fp_line.value if fp_line.value_used else 0,
                     fp_line.value if not fp_line.value_used else 0)
                )

            vendors_grouped = []
            totals_used = []
            totals_to_use = []

            for vendor in vendors:
                if vendor[0] not in vendors_grouped:
                    vendors_grouped.append(vendor[0])

            for vg in vendors_grouped:
                total_used = 0
                total_to_use = 0

                for v in vendors:
                    if v[0] == vg:
                        total_used += v[1]
                        total_to_use += v[2]

                totals_used.append(total_used)
                totals_to_use.append(total_to_use)

            for vendor in vendors_grouped:
                self.write({
                    "amazon_financial_plan_more_values": [(
                        0, 0, {
                            'name': line.id,
                            'vendor': vendor,
                            'total_used': totals_used[vendors_grouped.index(vendor)],
                            'total_to_use': totals_to_use[vendors_grouped.index(vendor)]
                        }
                    )]
                })

            ### UPDATE AMZ CURRENT FP MORE VALUES (VENDORS) ###

            line.amazon_current_fp_more_values = [(5, 0, 0)]
            vendors = []
            totals_to_use = []
            totals_used = []

            for fp_line in line.amazon_financial_plan_more_lines:
                vendors.append(fp_line.vendor.id)

                if fp_line.value_used:
                    totals_used.append(fp_line.value)
                    totals_to_use.append(0)
                else:
                    totals_used.append(0)
                    totals_to_use.append(fp_line.value)

            vendors_grouped = []

            for vendor in vendors:
                if vendor not in vendors_grouped:
                    vendors_grouped.append(vendor)

            for vendor in vendors_grouped:
                self.write({
                    'amazon_current_fp_more_values': [(
                        0, 0, {
                            'name': line.id,
                            'vendor': vendor,
                            'total_used': totals_used[vendors_grouped.index(vendor)],
                            'total_to_use': totals_to_use[vendors_grouped.index(vendor)]
                        }
                    )]
                })

        ### CLEAN DUPLICATES OF FP LINES ###

        for line in self:
            for fp_value in line.amazon_financial_plan_values[-len(line.amazon_financial_plan_lines):]:
                fp_value.unlink()

            for fp_more_values in line.amazon_financial_plan_more_values[-len(line.amazon_financial_plan_more_lines):]:
                fp_more_values.unlink()

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
