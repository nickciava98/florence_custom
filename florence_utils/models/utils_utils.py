from odoo import models, fields, api


class UtilsUtils(models.Model):
    _name = "utils.utils"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Profit"

    name = fields.Char(
        copy=False,
        string="Year"
    )
    month_ids = fields.One2many(
        "utils.months",
        "name",
        copy=True,
        string="Months"
    )
    day_ids = fields.One2many(
        "utils.days",
        "name",
        copy=False,
        string="Days"
    )
    date_start = fields.Date()
    date_end = fields.Date()
    day_filtered_ids = fields.One2many(
        "utils.days",
        "name_filtered",
        copy=False,
        string="Days Filtered"
    )
    total_util = fields.Float(
        digits=(11, 2),
        compute="_compute_total_util",
        string="Total Profit",
        store=True
    )
    currency_id = fields.Many2one(
        "res.currency",
        default=lambda self: self.env.ref("base.main_company").currency_id
    )

    @api.depends("month_ids", "day_ids")
    def _compute_total_util(self):
        for line in self:
            line.total_util = .0

            if len(line.month_ids) > 0:
                for month in line.month_ids:
                    line.total_util += month.util

            if len(line.day_ids) > 0:
                for day in line.day_ids:
                    line.total_util += day.util

    def update_days_action(self):
        days_present = [day.date for day in self.day_ids] if len(self.day_ids) > 0 else []
        revenues = self.env["amazon.revenues.line"].search(
            ["&", ("date", ">=", self.name + "-01-01"), ("date", "<=", self.name + "-12-31")]
        )
        days_total = [revenue.date for revenue in revenues]
        days_total = list(dict.fromkeys(days_total))

        if days_total:
            for day in filter(lambda d: d not in days_present, days_total):
                self.env["utils.days"].create({
                    "name": self.id,
                    "date": day
                })

    def filter_by_date_action(self):
        self.day_filtered_ids = [(5, 0, 0)]

        for day_id in self.day_ids.filtered(lambda d: d.date >= self.date_start and d.date <= self.date_end):
            self.day_filtered_ids = [(0, 0, {
                "name_filtered": self.id,
                "date": day_id.date
            })]
