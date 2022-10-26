from odoo import models, fields, api
import datetime


class AmazonFinancialPlanLine(models.Model):
    _name = "amazon.financial.plan.line"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Amazon Financial Plan"

    name = fields.Many2one(
        "amazon.financial.plan",
        ondelete = "cascade"
    )
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
    total_used = fields.Float(
        group_operator = "avg"
    )
    total_to_use = fields.Float(
        group_operator = "avg"
    )

    def _compute_currency_id(self):
        for line in self:
            line.currency_id = self.env.ref('base.main_company').currency_id
