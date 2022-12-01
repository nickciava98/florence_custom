from odoo import models, fields, api
from odoo.exceptions import ValidationError
import datetime


class FlorenceFpCosts(models.Model):
    _name = "florence.fp.costs"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Florence FP Costs"

    name = fields.Many2one(
        "product.product",
        required = True,
        string = "Product"
    )
    sku = fields.Many2one(
        "stock.production.lot",
        copy = True
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
        compute = "_compute_total",
        digits = (12, 4),
        store = True
    )
    pieces = fields.Float(
        default = 1,
        copy = True,
        digits = (12, 4),
        required = True
    )
    price = fields.Float(
        compute = "_compute_price",
        digits = (12, 4),
        store = True
    )
    fp_costs_lines = fields.One2many(
        "florence.fp.costs.line",
        "name",
        copy = True
    )

    @api.constrains("pieces")
    def _constrains_pieces(self):
        for line in self:
            if line.pieces <= 0:
                raise ValidationError(
                    "Pieces must be greater than zero!"
                )

    @api.onchange("name")
    def _onchange_name(self):
        for line in self:
            if line.name and line.name.bom_count > 0:
                for bom_line in self.env["mrp.bom.line"].search(
                    [("bom_id", "=", self.env["mrp.bom"].search(
                        [("product_id", "=", line.name.id)]
                    )[0].id)]):
                    self.write({
                        "fp_costs_lines": [(
                            0, 0, {
                                "name": line.id,
                                "component": bom_line.product_id
                            }
                        )]
                    })

    @api.depends("price", "pieces")
    def _compute_total(self):
        for line in self:
            line.total = 0

            if line.pieces != 0:
                line.total = line.price / line.pieces

    @api.depends("fp_costs_lines", "pieces")
    def _compute_price(self):
        for line in self:
            line.price = 0

            if len(line.fp_costs_lines) > 0:
                for fp_cost in line.fp_costs_lines:
                    line.price += fp_cost.cost

            line.price *= line.pieces

    def _compute_currency_id(self):
        for line in self:
            line.currency_id = self.env.ref("base.main_company").currency_id
