from odoo import models, fields


class UtilsDays(models.Model):
    _name = "utils.days"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Utils Days"

    name = fields.Many2one(
        "utils.utils",
        ondelete = "cascade"
    )
    date = fields.Date()
    probable_income_amz = fields.Float()
    monthly_total_per_day = fields.Float()
    util = fields.Float()
    currency_id = fields.Many2one(
        "res.currency",
        related = "name.currency_id",
        store = True
    )
