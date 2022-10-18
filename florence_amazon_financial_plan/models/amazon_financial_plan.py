from odoo import models, fields, api
import datetime


class AmazonFinancialPlan(models.Model):
    _name = "amazon.financial.plan"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Amazon Financial Plan"

    name = fields.Char()
    date = fields.Date(
        default = datetime.datetime.now()
    )
    currency_id = fields.Many2one(
        "res.currency",
        compute = "_compute_currency_id"
    )
    product_id = fields.Many2one(
        "product.template"
    )
    value = fields.Float()
    value_used = fields.Boolean()
    total_used = fields.Float()
    total_to_use = fields.Float()

    @api.onchange("value_used")
    def _onchange_value_used(self):
        for line in self:
            line.total_used = 0

            if line.value_used:
                line.total_to_use = 0
                line.total_used = line.value
            else:
                line.total_used = 0
                line.total_to_use = line.value

    def _compute_currency_id(self):
        for line in self:
            line.currency_id = self.env.ref('base.main_company').currency_id
