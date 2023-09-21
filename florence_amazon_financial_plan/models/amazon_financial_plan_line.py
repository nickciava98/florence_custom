import datetime

from odoo import models, fields


class AmazonFinancialPlanLine(models.Model):
    _name = "amazon.financial.plan.line"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Amazon Financial Plan"

    name = fields.Many2one(
        "amazon.financial.plan",
        ondelete="cascade"
    )
    date = fields.Date(
        default=datetime.datetime.now()
    )
    currency_id = fields.Many2one(
        "res.currency",
        related="name.currency_id",
        store=True
    )
    product_id = fields.Many2one(
        "product.template"
    )
    value = fields.Float(
        digits=(12, 4)
    )
    value_used = fields.Boolean()
    total_used = fields.Float(
        group_operator="avg",
        digits=(12, 4)
    )
    total_to_use = fields.Float(
        group_operator="avg",
        digits=(12, 4)
    )
