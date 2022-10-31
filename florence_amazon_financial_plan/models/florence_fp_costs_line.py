from odoo import models, fields, api


class FlorenceFpCostsLine(models.Model):
    _name = "florence.fp.costs.line"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Florence FP Costs Line"

    name = fields.Many2one(
        "florence.fp.costs",
        ondelete = "cascade"
    )
    item = fields.Char()
    cost = fields.Float()
    currency_id = fields.Many2one(
        "res.currency",
        compute = "_compute_currency_id"
    )

    def _compute_currency_id(self):
        for line in self:
            line.currency_id = self.env.ref("base.main_company").currency_id
