import datetime

from odoo import models, fields


class AmazonFinancialPlanMore(models.Model):
    _name = "amazon.financial.plan.more"
    _description = "Amazon Financial Plan More"

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
    vendor = fields.Many2one(
        "res.partner",
        domain="[('supplier_rank','>',0)]"
    )
    notes = fields.Char()
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
