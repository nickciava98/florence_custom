from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class AmazonRevenuesReporting(models.Model):
    _name = "amazon.revenues.reporting"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Revenues Report"

    name = fields.Char(
        string = "Report",
        copy = False
    )
    date_start = fields.Date()
    date_to = fields.Date()
    currency_id = fields.Many2one(
        "res.currency",
        compute = "_compute_currency_id"
    )
    total_revenues = fields.Float(
        compute = "_compute_total_revenues",
        store = True,
        digits = (12, 4)
    )
    financial_plan_value = fields.Float(
        digits = (12, 4)
    )
    delta = fields.Float(
        compute = "_compute_delta",
        store = True,
        digits = (12, 4)
    )
    delta_hint = fields.Char(
        compute = "_compute_delta_hint",
        string = "Status"
    )

    def _compute_currency_id(self):
        for line in self:
            line.currency_id = self.env.ref('base.main_company').currency_id

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

    @api.constrains("name")
    def _constrains_name(self):
        for line in self:
            if not line.name:
                raise ValidationError(
                    _("Name must be filled!")
                )

    _sql_constraint = [
        ("unique_name", "unique(name)", _("Name must be unique!"))
    ]
