from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import datetime
import calendar
import math


class FlorenceFpCosts(models.Model):
    _name = "florence.fp.costs"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Florence FP Costs"

    name = fields.Many2one(
        "product.product",
        copy = True,
        string = "Product"
    )
    sku_id = fields.Many2one(
        "product.sku",
        copy = True
    )
    date = fields.Date(
        default = datetime.datetime.now(),
        copy = False
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
        digits = (12, 4)
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
                year = line.date.strftime("%Y")
                month = line.date.strftime("%m")
                last_day = str(calendar.monthrange(int(year), int(month))[1])
                bom_id = self.env["mrp.bom"].search(
                    [("product_id", "=", line.name.id)], limit = 1
                ).id

                for bom_line in self.env["mrp.bom.line"].search([("bom_id", "=", bom_id)]):
                    bill_id = 0
                    cost = 0
                    invoice_domain = [
                        "&",
                        ("move_type", "=", "in_invoice"), ("invoice_date", "<=", year + "-" + month + "-" + last_day)
                    ]

                    for bill in self.env["account.move"].search(invoice_domain, order = "name desc"):
                        for invoice_line in bill.invoice_line_ids:
                            if invoice_line.product_id.id == bom_line.product_id.id:
                                bill_id = bill.id
                                cost = invoice_line.price_unit
                                break

                        if bill_id != 0 and cost != 0:
                            break

                    self.sudo().write({
                        "fp_costs_lines": [(
                            0, 0, {
                                "name": line.id,
                                "component": bom_line.product_id.id,
                                "cost": cost,
                                "bill": bill_id
                            }
                        )]
                    })

    @api.depends("price", "pieces")
    def _compute_total(self):
        for line in self:
            line.total = line.price / line.pieces if line.pieces != 0 else .0

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

    @api.constrains("name")
    def _constrains_name(self):
        for line in self:
            if not line.name:
                raise ValidationError(
                    _("Name must be filled!")
                )

    def update_values_action(self):
        for line in self:
            line.fp_costs_lines = [(5, 0, 0)]

            if line.name and line.name.bom_count > 0:
                year = line.date.strftime("%Y")
                month = line.date.strftime("%m")
                last_day = str(calendar.monthrange(int(year), int(month))[1])
                bom_id = self.env["mrp.bom"].search(
                    [("product_id", "=", line.name.id)],
                    limit = 1
                )

                for bom_line in self.env["mrp.bom.line"].search([("bom_id", "=", bom_id.id)]):
                    bill_id = 0
                    cost = .0
                    domain = [
                        "&",
                        ("move_type", "=", "in_invoice"), ("invoice_date", "<=", year + "-" + month + "-" + last_day)
                    ]

                    for bill in self.env["account.move"].search(domain, order = "name desc"):
                        for invoice_line in bill.invoice_line_ids:
                            if invoice_line.product_id.id == bom_line.product_id.id:
                                bill_id = bill.id
                                cost = invoice_line.price_unit
                                break

                        if bill_id != 0 and not math.isclose(cost, 0.0):
                            break

                    self.env["florence.fp.costs.line"].sudo().create({
                        "name": line.id,
                        "component": bom_line.product_id.id,
                        "cost": cost,
                        "bill": bill_id
                    })

                bill_id = 0
                cost = .0
                domain = [
                    "&",
                    ("move_type", "=", "in_invoice"),
                    ("invoice_date", "<=", year + "-" + month + "-" + last_day)
                ]

                for bill in self.env["account.move"].search(domain, order = "name desc"):
                    for invoice_line in bill.invoice_line_ids:
                        if invoice_line.product_id.id == line.name.id:
                            bill_id = bill.id
                            cost = invoice_line.price_unit
                            break

                    if bill_id != 0 and not math.isclose(cost, 0.0):
                        break

                self.env["florence.fp.costs.line"].sudo().create({
                    "name": line.id,
                    "component": line.name.id,
                    "cost": cost,
                    "bill": bill_id
                })
