from odoo import models, fields


class UtilsDays(models.Model):
    _name = "utils.days"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Util Days"

    name = fields.Many2one(
        "utils.utils",
        ondelete = "cascade"
    )
    date = fields.Date(
        string = "Date (i)"
    )
    probable_income_amz = fields.Float(
        string = "Probable Income (Amazon) (ii)"
    )
    monthly_total_per_day = fields.Float(
        string = "Monthly Total Per Day (iii)"
    )
    util = fields.Float(
        string = "Util (iv)"
    )
    currency_id = fields.Many2one(
        "res.currency",
        related = "name.currency_id",
        store = True
    )
