from odoo import models, fields, api
import calendar
import math


class FlorenceFpCostsLine(models.Model):
    _name = "florence.fp.costs.line"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Florence FP Costs Line"

    name = fields.Many2one(
        "florence.fp.costs",
        ondelete = "cascade"
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
        compute = "_compute_currency_id"
    )

    def _compute_currency_id(self):
        for line in self:
            line.currency_id = self.env.ref("base.main_company").currency_id
