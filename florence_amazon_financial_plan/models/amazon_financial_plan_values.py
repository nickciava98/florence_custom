from odoo import models, fields


class AmazonFinancialPlanValues(models.Model):
    _name = "amazon.financial.plan.values"
    _description = "Amazon Financial Plan Values"

    name = fields.Many2one(
        "amazon.financial.plan",
        ondelete="cascade"
    )
    current_name = fields.Many2one(
        "amazon.financial.plan",
        ondelete="cascade"
    )
    product_id = fields.Many2one(
        "product.template"
    )
    total_used = fields.Float(
        digits=(12, 4)
    )
    total_to_use = fields.Float(
        digits=(12, 4)
    )
    currency_id = fields.Many2one(
        "res.currency",
        related="name.currency_id",
        store=True
    )


class AmazonFinancialPlanMoreValues(models.Model):
    _name = "amazon.financial.plan.more.values"
    _description = "Amazon Financial Plan Values"

    name = fields.Many2one(
        "amazon.financial.plan",
        ondelete="cascade"
    )
    current_name = fields.Many2one(
        "amazon.financial.plan",
        ondelete="cascade"
    )
    vendor = fields.Many2one(
        "res.partner",
        domain="[('supplier_rank','>',0)]"
    )
    total_used = fields.Float(
        digits=(12, 4)
    )
    total_to_use = fields.Float(
        digits=(12, 4)
    )
    currency_id = fields.Many2one(
        "res.currency",
        related="name.currency_id",
        store=True
    )
