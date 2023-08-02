import calendar
import datetime
import math

from odoo.exceptions import ValidationError

from odoo import models, fields, api, _


class FlorenceFpCosts(models.Model):
    _name = "florence.fp.costs"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Florence FP Costs"

    name = fields.Many2one(
        "product.product",
        copy=True,
        string="Product"
    )
    sku_id = fields.Many2one(
        "product.sku",
        copy=True
    )
    date = fields.Date(
        default=datetime.datetime.today(),
        copy=False
    )
    currency_id = fields.Many2one(
        "res.currency",
        default=lambda self: self.env.ref("base.main_company").currency_id
    )
    total = fields.Float(
        compute="_compute_total",
        digits=(12, 4),
        store=True
    )
    pieces = fields.Float(
        default=1,
        copy=True,
        digits=(12, 4)
    )
    price = fields.Float(
        compute="_compute_price",
        digits=(12, 4),
        store=True
    )
    fp_costs_lines = fields.One2many(
        "florence.fp.costs.line",
        "name",
        copy=True
    )

    @api.constrains("pieces")
    def _constrains_pieces(self):
        for line in self:
            if line.pieces <= 0:
                raise ValidationError(
                    "Pieces must be greater than zero!"
                )

    @api.depends("price", "pieces")
    def _compute_total(self):
        for line in self:
            line.total = line.price / line.pieces if line.pieces != 0 else .0

    @api.depends("fp_costs_lines", "pieces")
    def _compute_price(self):
        for line in self:
            line.price = sum([fp_cost.cost for fp_cost in line.fp_costs_lines]) * line.pieces \
                if line.fp_costs_lines else .0

    def update_values_action(self):
        for line in self:
            line.fp_costs_lines = [(5, 0, 0)]

            if line.name and line.name.bom_count > 0:
                year = line.date.strftime("%Y")
                month = line.date.strftime("%m")
                last_day = str(calendar.monthrange(int(year), int(month))[1])
                bom_id = self.env["mrp.bom"].search(
                    [("product_id", "=", line.name.id)], limit=1
                )

                for bom_line in self.env["mrp.bom.line"].search([("bom_id", "=", bom_id.id)]):
                    bill_id = 0
                    cost = .0
                    purchase_ids = self.env["purchase.order"].search(
                        [("date_order", "<=", "%s-%s-%s" % (year, month, last_day))], order="id desc"
                    )

                    if line.product_id and purchase_ids:
                        for purchase_id in purchase_ids:
                            order_line = purchase_id.order_line.filtered(
                                lambda ol: ol.product_id.id == bom_line.product_id.id
                            )

                            if order_line:
                                if purchase_id.invoice_ids:
                                    for invoice_id in purchase_id.invoice_ids:
                                        invoice_line = invoice_id.invoice_line_ids.filtered(
                                            lambda inv_line: inv_line.product_id.id == bom_line.product_id.id
                                        )

                                        if invoice_line:
                                            bill_id = invoice_id.id
                                            cost = invoice_line[0].price_unit
                                            break
                                else:
                                    cost = order_line[0].price_unit

                                break

                        if math.isclose(cost, .0):
                            bills = self.env["account.move"].search(
                                ["&", ("move_type", "=", "in_invoice"),
                                 ("invoice_date", "<=", "%s-%s-%s" % (year, month, last_day))], order="id desc"
                            )

                            if bills:
                                for bill in bills:
                                    invoice_line = bill.invoice_line_ids.filtered(
                                        lambda inv_line: inv_line.product_id.id == bom_line.product_id.id
                                    )

                                    if invoice_line:
                                        bill_id = bill.id
                                        cost = invoice_line[0].price_unit
                                        break

                    self.env["florence.fp.costs.line"].sudo().create({
                        "name": line.id,
                        "component": bom_line.product_id.id,
                        "cost": cost,
                        "bill": bill_id
                    })

                bill_id = 0
                cost = .0
                purchase_ids = self.env["purchase.order"].search(
                    [("date_order", "<=", "%s-%s-%s" % (year, month, last_day))], order="id desc"
                )

                if purchase_ids:
                    for purchase_id in purchase_ids:
                        order_line = purchase_id.order_line.filtered(
                            lambda ol: ol.product_id.id == line.name.id
                        )

                        if order_line:
                            if purchase_id.invoice_ids:
                                for invoice_id in purchase_id.invoice_ids:
                                    invoice_line = invoice_id.invoice_line_ids.filtered(
                                        lambda inv_line: inv_line.product_id.id == line.name.id
                                    )

                                    if invoice_line:
                                        bill_id = invoice_id.id
                                        cost = invoice_line[0].price_unit
                                        break
                            else:
                                cost = order_line[0].price_unit

                            break

                    if math.isclose(cost, .0):
                        bills = self.env["account.move"].search(
                            ["&", ("move_type", "=", "in_invoice"),
                             ("invoice_date", "<=", "%s-%s-%s" % (year, month, last_day))], order="id desc"
                        )

                        if bills:
                            for bill in bills:
                                invoice_line = bill.invoice_line_ids.filtered(
                                    lambda inv_line: inv_line.product_id.id == line.name.id
                                )

                                if invoice_line:
                                    bill_id = bill.id
                                    cost = invoice_line[0].price_unit
                                    break

                self.env["florence.fp.costs.line"].sudo().create({
                    "name": line.id,
                    "component": line.name.id,
                    "cost": cost,
                    "bill": bill_id
                })
