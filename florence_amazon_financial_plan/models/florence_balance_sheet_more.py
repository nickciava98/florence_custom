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
        compute="_compute_currency_id"
    )

    def _compute_currency_id(self):
        for line in self:
            line.currency_id = self.env.ref('base.main_company').currency_id
