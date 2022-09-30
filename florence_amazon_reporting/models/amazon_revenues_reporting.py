from odoo import models, fields, api


class AmazonRevenuesReporting(models.Model):
    _name = "amazon.revenues.reporting"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Revenues Report"

    name = fields.Char(
        string = "Report"
    )
    date_start = fields.Date()
    date_to = fields.Date()
    group_by = fields.Selection(
        [("day", "Daily"),
         ("monthly", "Monthly"),
         ("yearly", "Yearly")]
    )
    total_revenues = fields.Float(
        compute = "_compute_total_revenues",
        store = True
    )
    financial_plan_value = fields.Float()
    delta = fields.Float(
        compute = "_compute_delta",
        store = True
    )
    delta_hint = fields.Char(
        compute = "_compute_delta_hint",
        string = "Status"
    )

    @api.depends("date_start", "date_to")
    def _compute_total_revenues(self):
        for line in self:
            line.total_revenues = 0

            if line.date_start and line.date_to:
                for marketplace in self.env["amazon.revenues"].search([]):
                    if len(marketplace.revenues_line) > 0:
                        for revenues_line in marketplace.revenues_line:
                            if revenues_line.date >= line.date_start \
                                and revenues_line.date <= line.date_to:
                                line.total_revenues += revenues_line.probable_income

    @api.depends("total_revenues", "financial_plan_value")
    def _compute_delta(self):
        for line in self:
            line.delta = line.total_revenues - line.financial_plan_value

    @api.depends("delta")
    def _compute_delta_hint(self):
        for line in self:
            line.delta_hint = ""

            if float("%.2f" % line.delta) < 0:
                line.delta_hint = "Balance is currently negative"
            elif float("%.2f" % line.delta) > 0:
                line.delta_hint = "Balance is currently positive"
            elif float("%.2f" % line.delta) == 0:
                line.delta_hint = "Balance is currently tie"

