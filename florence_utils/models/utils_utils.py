from odoo import models, fields, api
import calendar


class UtilsUtils(models.Model):
    _name = "utils.utils"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Util"

    name = fields.Char(
        copy = False,
        string = "Year"
    )
    month_ids = fields.One2many(
        "utils.months",
        "name",
        copy = True,
        string = "Months"
    )
    day_ids = fields.One2many(
        "utils.days",
        "name",
        copy = False,
        string = "Days"
    )
    total_util = fields.Float(
        digits = (11, 2),
        compute = "_compute_total_util",
        store = True
    )
    currency_id = fields.Many2one(
        "res.currency",
        default = lambda self: self.env.ref("base.main_company").currency_id
    )

    @api.depends("month_ids", "day_ids")
    def _compute_total_util(self):
        for line in self:
            line.total_util = 0.0

            if len(line.month_ids) > 0:
                for month in line.month_ids:
                    line.total_util += month.util

            if len(line.day_ids) > 0:
                for day in line.day_ids:
                    line.total_util += day.util

    def update_days_action(self):
        days_present = [day.date for day in self.day_ids] if len(self.day_ids) > 0 else []
        days_total = []
        domain = [
            "&",
            ("date", ">=", self.name + "-01-01"),
            ("date", "<=", self.name + "-12-31")
        ]

        for revenue in self.env["amazon.revenues.line"].search(domain):
            if revenue.date not in days_total:
                days_total.append(revenue.date)

        if len(days_total) > 0:
            for day in days_total:
                if day not in days_present:
                    probable_income = 0.0
                    monthly_total_per_day = 0.0

                    for revenue in self.env["amazon.revenues.line"].search([("date", "=", day)]):
                        probable_income += revenue.probable_income_amz

                    if len(self.month_ids) > 0:
                        month_days = int(calendar.monthrange(int(self.name), int(day.strftime("%m")))[1])

                        for month in self.month_ids:
                            if month.month == str(day.strftime("%m")):
                                monthly_total_per_day = month.monthly_total / month_days

                    self.env["utils.days"].sudo().create({
                        "name": self.id,
                        "date": day,
                        "probable_income_amz": probable_income,
                        "monthly_total_per_day": monthly_total_per_day,
                        "util": probable_income - monthly_total_per_day
                    })
