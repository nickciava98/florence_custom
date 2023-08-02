import math

from odoo import models, fields, api
import calendar


class FlorenceBalanceSheetInventory(models.Model):
    _name = "florence.balance.sheet.inventory"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Florence Balance Sheet Inventory"

    name = fields.Many2one(
        "florence.balance.sheet"
    )
    product_id = fields.Many2one(
        "product.product"
    )
    location_id = fields.Many2one(
        "stock.location"
    )
    lot_id = fields.Many2one(
        "stock.production.lot"
    )
    available_quantity = fields.Float()
    value = fields.Float()
    currency_id = fields.Many2one(
        "res.currency",
        related="name.currency_id",
        store=True
    )
    sale_ok = fields.Boolean(
        string="Can Be Sold"
    )
    can_be_used = fields.Boolean()

    @api.onchange("available_quantity")
    def _onchange_available_quantity(self):
        for line in self:
            if line.name.date:
                year = str(line.name.date.year)
                month = str(line.name.date.month)
                last_day = str(calendar.monthrange(int(year), int(month))[1])
                purchase_ids = self.env["purchase.order"].search(
                    [("date_order", "<=", "%s-%s-%s" % (year, month, last_day))], order="id desc"
                )

                if line.product_id and purchase_ids:
                    for purchase_id in purchase_ids:
                        order_line = purchase_id.order_line.filtered(
                            lambda ol: ol.product_id.id == line.product_id.id
                        )

                        if order_line:
                            if purchase_id.invoice_ids:
                                for invoice_id in purchase_id.invoice_ids:
                                    invoice_line = invoice_id.invoice_line_ids.filtered(
                                        lambda inv_line: inv_line.product_id.id == line.product_id.id
                                    )

                                    if invoice_line:
                                        line.value = invoice_line[0].price_unit * line.available_quantity
                                        break
                            else:
                                line.value = order_line[0].price_unit * line.available_quantity

                            break

                    if math.isclose(line.value, .0):
                        bills = self.env["account.move"].search(
                            ["&", ("move_type", "=", "in_invoice"),
                             ("invoice_date", "<=", "%s-%s-%s" % (year, month, last_day))], order="id desc"
                        )

                        if bills:
                            for bill in bills:
                                invoice_line = bill.invoice_line_ids.filtered(
                                    lambda inv_line: inv_line.product_id.id == line.product_id.id
                                )

                                if invoice_line:
                                    line.value = invoice_line[0].price_unit * line.available_quantity
                                    break


class FlorenceBalanceSheetInventoryMore(models.Model):
    _name = "florence.balance.sheet.inventory.more"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Florence Balance Sheet Inventory More"

    name = fields.Many2one(
        "florence.balance.sheet"
    )
    product_id = fields.Many2one(
        "product.product"
    )
    location = fields.Char()
    lot = fields.Char()
    available_quantity = fields.Float()
    value = fields.Float()
    currency_id = fields.Many2one(
        "res.currency",
        related="name.currency_id",
        store=True
    )
    sale_ok = fields.Boolean(
        string="Can Be Sold"
    )
    can_be_used = fields.Boolean()

    @api.onchange("available_quantity")
    def _onchange_available_quantity(self):
        for line in self:
            if line.name.date:
                year = str(line.name.date.year)
                month = str(line.name.date.month)
                last_day = str(calendar.monthrange(int(year), int(month))[1])
                purchase_ids = self.env["purchase.order"].search(
                    [("date_order", "<=", "%s-%s-%s" % (year, month, last_day))], order="id desc"
                )

                if line.product_id and purchase_ids:
                    for purchase_id in purchase_ids:
                        order_line = purchase_id.order_line.filtered(
                            lambda ol: ol.product_id.id == line.product_id.id
                        )

                        if order_line:
                            if purchase_id.invoice_ids:
                                for invoice_id in purchase_id.invoice_ids:
                                    invoice_line = invoice_id.invoice_line_ids.filtered(
                                        lambda inv_line: inv_line.product_id.id == line.product_id.id
                                    )

                                    if invoice_line:
                                        line.value = invoice_line[0].price_unit * line.available_quantity
                                        break
                            else:
                                line.value = order_line[0].price_unit * line.available_quantity

                            break

                    if math.isclose(line.value, .0):
                        bills = self.env["account.move"].search(
                            ["&", ("move_type", "=", "in_invoice"),
                             ("invoice_date", "<=", "%s-%s-%s" % (year, month, last_day))], order="id desc"
                        )

                        if bills:
                            for bill in bills:
                                invoice_line = bill.invoice_line_ids.filtered(
                                    lambda inv_line: inv_line.product_id.id == line.product_id.id
                                )

                                if invoice_line:
                                    line.value = invoice_line[0].price_unit * line.available_quantity
                                    break
