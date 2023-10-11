import calendar

from odoo import models, fields, api


class UtilsDays(models.Model):
    _name = "utils.days"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Profit Days"

    name = fields.Many2one(
        "utils.utils",
        ondelete="cascade"
    )
    name_filtered = fields.Many2one(
        "utils.utils",
        ondelete="cascade"
    )
    date = fields.Date(
        string="Date (i)"
    )
    probable_income_amz = fields.Float(
        compute="_compute_probable_income_amz",
        string="Probable Income (Amazon) (ii)"
    )
    monthly_total_per_day = fields.Float(
        compute="_compute_monthly_total_per_day",
        string="Monthly Total Per Day (iii)"
    )
    util = fields.Float(
        compute="_compute_util",
        string="Profit (iv)"
    )
    currency_id = fields.Many2one(
        "res.currency",
        compute="_compute_currency_id",
        store=True
    )

    @api.depends("name", "name.currency_id", "name_filtered", "name_filtered.currency_id")
    def _compute_currency_id(self):
        for line in self:
            line.currency_id = False

            if line.name:
                line.currency_id = line.name.currency_id
            elif line.name_filtered:
                line.currency_id = line.name_filtered.currency_id

    @api.depends("date")
    def _compute_probable_income_amz(self):
        for line in self:
            revenues = self.env["amazon.revenues.line"].search([("date", "=", line.date)])
            line.probable_income_amz = sum([
                revenue.probable_income_amz for revenue in revenues
            ]) if line.date and revenues else .0

    @api.depends("name", "name.name", "name.month_ids", "name.month_ids.month",
                 "name_filtered", "name_filtered.name", "name_filtered.month_ids",
                 "name_filtered.month_ids.month", "date")
    def _compute_monthly_total_per_day(self):
        for line in self:
            line.monthly_total_per_day = .0

            if line.name and line.name.month_ids:
                line.monthly_total_per_day = line.name.month_ids.filtered(
                    lambda month: month.month == str(line.date.strftime("%m"))
                ).monthly_total / int(calendar.monthrange(int(line.name.name), int(line.date.strftime("%m")))[1])
            elif line.name_filtered and line.name_filtered.month_ids:
                line.monthly_total_per_day = line.name_filtered.month_ids.filtered(
                    lambda month: month.month == str(line.date.strftime("%m"))
                ).monthly_total / int(calendar.monthrange(int(line.name_filtered.name), int(line.date.strftime("%m")))[1])

    @api.depends("probable_income_amz", "monthly_total_per_day")
    def _compute_util(self):
        for line in self:
            line.util = line.probable_income_amz - line.monthly_total_per_day
