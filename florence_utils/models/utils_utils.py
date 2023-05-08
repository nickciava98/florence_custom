from odoo import models, fields, api
import datetime


class UtilsUtils(models.Model):
    _name = "utils.utils"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Utils"

    name = fields.Char(
        copy = False,
        string = "Year"
    )
    month_ids = fields.One2many(
        "utils.months",
        "name",
        copy = True,
        string = "Months"
    )
    total_util = fields.Float(
        digits = (11, 2),
        compute = "_compute_total_util",
        store = True
    )
    currency_id = fields.Many2one(
        "res.currency",
        default = lambda self: self.env.ref("base.main_company").currency_id
    )

    @api.depends("month_ids")
    def _compute_total_util(self):
        for line in self:
            line.total_util = 0.0

            if len(line.month_ids) > 0:
                for month in line.month_ids:
                    line.total_util += month.util
