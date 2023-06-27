from odoo import models, fields, api
import calendar


class UtilsMonths(models.Model):
    _name = "utils.months"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Profit Months"

    name = fields.Many2one(
        "utils.utils",
        ondelete = "cascade",
        string = "Profit Ref."
    )
    month = fields.Selection(
        [("01", "January"),
         ("02", "February"),
         ("03", "March"),
         ("04", "April"),
         ("05", "May"),
         ("06", "June"),
         ("07", "July"),
         ("08", "August"),
         ("09", "September"),
         ("10", "October"),
         ("11", "November"),
         ("12", "December")],
        string = "Month (i)",
        copy = True
    )
    taxes = fields.Float(
        default = 0.0,
        string = "Taxes (ii)"
    )
    inventory = fields.Float(
        compute = "_compute_inventory",
        string = "Product Real Cost (iii)"
    )
    inventory_value = fields.Float(
        compute = "_compute_inventory_value",
        string = "Inventory Value (iv)"
    )
    div4a_value = fields.Float(
        compute = "_compute_div4a_value",
        string = "DIV4A Value (v)"
    )
    monthly_total = fields.Float(
        compute = "_compute_monthly_total",
        string = "Monthly Total (vi)"
    )
    util = fields.Float(
        compute = "_compute_util",
        string = "Profit (vii)"
    )
    currency_id = fields.Many2one(
        "res.currency",
        related = "name.currency_id",
        store = True
    )

    @api.depends("month")
    def _compute_monthly_total(self):
        for line in self:
            line.monthly_total = .0

            if line.month:
                last_day = str(calendar.monthrange(int(line.name.name), int(line.month))[1])
                domain = [
                    "&",
                    ("date", ">=", str(line.name.name) + "-" + str(line.month) + "-" + "01"),
                    ("date", "<=", str(line.name.name) + "-" + str(line.month) + "-" + str(last_day))
                ]
                florence_fp_id = self.env["florence.financial.plan"].search(domain, order = "date desc", limit = 1)

                if florence_fp_id:
                    line.monthly_total = florence_fp_id.monthly_total

                domain2 = [
                    "&", "&",
                    ("date", ">=", str(line.name.name) + "-" + str(line.month) + "-" + "01"),
                    ("date", "<=", str(line.name.name) + "-" + str(line.month) + "-" + str(last_day)),
                    ("is_single_cost", "=", True)
                ]
                florence_fp_lines_single_cost = self.env["florence.financial.plan.line"].search(domain2)

                if len(florence_fp_lines_single_cost) > 0:
                    for fp_line in florence_fp_lines_single_cost:
                        line.monthly_total += fp_line.approved

    @api.depends("month")
    def _compute_inventory(self):
        for line in self:
            line.inventory = .0

            if line.month:
                last_day = str(calendar.monthrange(int(line.name.name), int(line.month))[1])
                domain = [
                    "&",
                    ("date", ">=", str(line.name.name) + "-" + str(line.month) + "-" + "01"),
                    ("date", "<=", str(line.name.name) + "-" + str(line.month) + "-" + str(last_day))
                ]

                for forecast in self.env["florence.forecasting"].search(domain):
                    line.inventory += forecast.est_value

    @api.depends("month")
    def _compute_inventory_value(self):
        for line in self:
            line.inventory_value = .0

            if line.month:
                last_day = str(calendar.monthrange(int(line.name.name), int(line.month))[1])
                domain = [
                    "&",
                    ("date", ">=", str(line.name.name) + "-" + str(line.month) + "-" + "01"),
                    ("date", "<=", str(line.name.name) + "-" + str(line.month) + "-" + str(last_day))
                ]
                line.inventory_value = self.env["florence.balance.sheet"].search(
                    domain, order = "create_date desc", limit = 1
                ).inventory_value

    @api.depends("month")
    def _compute_div4a_value(self):
        for line in self:
            line.div4a_value = .0

            if line.month:
                last_day = str(calendar.monthrange(int(line.name.name), int(line.month))[1])
                domain = [
                    "&",
                    ("date", ">=", str(line.name.name) + "-" + str(line.month) + "-" + "01"),
                    ("date", "<=", str(line.name.name) + "-" + str(line.month) + "-" + str(last_day))
                ]
                fp_lines = self.env["florence.financial.plan"].search(
                    domain, order = "create_date desc", limit = 1
                ).div4a

                for fp_line in fp_lines:
                    line.div4a_value += fp_line.monthly_computed

    @api.depends("month")
    def _compute_util(self):
        for line in self:
            line.util = .0

            if line.month:
                last_day = str(calendar.monthrange(int(line.name.name), int(line.month))[1])
                domain = [
                    "&",
                    ("date", ">=", str(line.name.name) + "-" + str(line.month) + "-" + "01"),
                    ("date", "<=", str(line.name.name) + "-" + str(line.month) + "-" + str(last_day))
                ]

                for fp in self.env["florence.financial.plan"].search(domain):
                    line.util += fp.surplus
