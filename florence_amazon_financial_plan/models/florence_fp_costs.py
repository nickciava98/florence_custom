from odoo import models, fields, api
import datetime


class FlorenceFpCosts(models.Model):
    _name = "florence.fp.costs"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Florence FP Costs"

    name = fields.Many2one(
        "product.template",
        required = True,
        string = "Product"
    )
    date = fields.Date(
        default = datetime.datetime.now(),
        required = True
    )
    currency_id = fields.Many2one(
        "res.currency",
        compute = "_compute_currency_id"
    )
    total = fields.Float(
        compute = "_compute_total"
    )
    pieces = fields.Float(
        default = 0,
        copy = True
    )
    price = fields.Float(
        compute = "_compute_price"
    )
    fp_costs_lines = fields.One2many(
        "florence.fp.costs.line",
        "name",
        copy = True
    )

    @api.depends("fp_costs_lines")
    def _compute_total(self):
        for line in self:
            line.total = 0

            if len(line.fp_costs_lines) > 0:
                for fp_cost in line.fp_costs_lines:
                    line.total += fp_cost.cost

    @api.depends("total", "pieces")
    def _compute_price(self):
        for line in self:
            line.price = line.total * line.pieces

    def _compute_currency_id(self):
        for line in self:
            line.currency_id = self.env.ref("base.main_company").currency_id
