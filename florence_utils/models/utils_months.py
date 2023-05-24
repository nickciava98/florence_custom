from odoo import models, fields, api
import calendar


class UtilsMonths(models.Model):
    _name = "utils.months"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Util Months"

    name = fields.Many2one(
        "utils.utils",
        ondelete = "cascade",
        string = "Util Ref."
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
        string = "Inventory (iii)"
    )
    monthly_total = fields.Float(
        compute = "_compute_monthly_total",
        string = "Monthly Total (iv)"
    )
    util = fields.Float(
        compute = "_compute_util",
        string = "Util (v)"
    )
    currency_id = fields.Many2one(
        "res.currency",
        related = "name.currency_id",
        store = True
    )

    @api.depends("month")
    def _compute_monthly_total(self):
        for line in self:
            line.monthly_total = 0.0

            if line.month:
                last_day = str(calendar.monthrange(int(line.name.name), int(line.month))[1])
                domain = [
                    "&",
                    ("date", ">=", str(line.name.name) + "-" + str(line.month) + "-" + "01"),
                    ("date", "<=", str(line.name.name) + "-" + str(line.month) + "-" + str(last_day))
                ]
                florence_fp_id = self.env["florence.financial.plan"].search(domain, limit = 1)

                if florence_fp_id:
                    line.monthly_total = florence_fp_id.monthly_total

    @api.depends("month")
    def _compute_inventory(self):
        for line in self:
            line.inventory = 0.0

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
    def _compute_util(self):
        for line in self:
            line.util = 0.0

            if line.month:
                last_day = str(calendar.monthrange(int(line.name.name), int(line.month))[1])
                domain = [
                    "&",
                    ("date", ">=", str(line.name.name) + "-" + str(line.month) + "-" + "01"),
                    ("date", "<=", str(line.name.name) + "-" + str(line.month) + "-" + str(last_day))
                ]

                for fp in self.env["florence.financial.plan"].search(domain):
                    line.util += fp.surplus
