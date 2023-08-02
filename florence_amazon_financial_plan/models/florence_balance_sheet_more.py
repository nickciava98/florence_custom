from odoo import models, fields


class FlorenceBalanceSheetMore(models.Model):
    _name = "florence.balance.sheet.more"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Florence Balance Sheet More"

    name = fields.Many2one(
        "florence.balance.sheet"
    )
    item = fields.Char()
    value = fields.Float()
    currency_id = fields.Many2one(
        "res.currency",
        related="name.currency_id",
        store=True
    )
