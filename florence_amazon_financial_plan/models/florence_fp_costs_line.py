from odoo import models, fields


class FlorenceFpCostsLine(models.Model):
    _name = "florence.fp.costs.line"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Florence FP Costs Line"

    name = fields.Many2one(
        "florence.fp.costs",
        ondelete = "cascade"
    )
    date = fields.Date(
        related = "name.date"
    )
    component = fields.Many2one(
        "product.product"
    )
    cost = fields.Float(
        digits = (12, 4)
    )
    vendor = fields.Many2one(
        "res.partner",
        related = "bill.partner_id",
        store = True
    )
    bill = fields.Many2one(
        "account.move"
    )
    bill_date = fields.Date(
        related = "bill.invoice_date",
        store = True
    )
    currency_id = fields.Many2one(
        "res.currency",
        related = "name.currency_id",
        store = True
    )
