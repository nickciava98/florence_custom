from odoo import models, fields, api
import calendar


class UtilsDays(models.Model):
    _name = "utils.days"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Profit Days"

    name = fields.Many2one(
        "utils.utils",
        ondelete = "cascade"
    )
    date = fields.Date(
        string = "Date (i)"
    )
    probable_income_amz = fields.Float(
        compute = "_compute_probable_income_amz",
        string = "Probable Income (Amazon) (ii)"
    )
    monthly_total_per_day = fields.Float(
        compute = "_compute_monthly_total_per_day",
        string = "Monthly Total Per Day (iii)"
    )
    util = fields.Float(
        compute = "_compute_util",
        string = "Profit (iv)"
    )
    currency_id = fields.Many2one(
        "res.currency",
        related = "name.currency_id",
        store = True
    )

    @api.depends("date")
    def _compute_probable_income_amz(self):
        for line in self:
            revenues = self.env["amazon.revenues.line"].search(
                [("date", "=", line.date)]
            )
            line.probable_income_amz = sum([
                revenue.probable_income_amz for revenue in revenues
            ]) if line.date and len(revenues) > 0 else .0

    @api.depends("name", "date")
    def _compute_monthly_total_per_day(self):
        for line in self:
            line.monthly_total_per_day = line.name.month_ids.filtered(
                lambda month: month.month == str(line.date.strftime("%m"))
            ).monthly_total / int(calendar.monthrange(int(line.name.name), int(line.date.strftime("%m")))[1]) \
            if len(line.name.month_ids) > 0 else .0

    @api.depends("probable_income_amz", "monthly_total_per_day")
    def _compute_util(self):
        for line in self:
            line.util = line.probable_income_amz - line.monthly_total_per_day
