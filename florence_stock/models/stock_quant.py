import math

from odoo import models, fields, api


class StockQuant(models.Model):
    _inherit = "stock.quant"

    value = fields.Monetary(
        string="Value",
        compute="_compute_value",
        groups="stock.group_stock_manager"
    )
    currency_id = fields.Many2one(
        "res.currency",
        related="company_id.currency_id",
        groups="stock.group_stock_manager"
    )
    sale_ok = fields.Boolean(
        related="product_id.sale_ok",
        store=True
    )
    can_be_used = fields.Boolean(
        related="product_id.can_be_used",
        store=True
    )

    @api.depends("product_id", "available_quantity")
    def _compute_value(self):
        for line in self:
            line.value = .0
            purchase_ids = self.env["purchase.order"].search([], order="id desc")

            if line.product_id:
                for purchase_id in purchase_ids:
                    order_line = purchase_id.order_line.filtered(
                        lambda ol: ol.product_id.id == line.product_id.id
                    )

                    if order_line and purchase_id.invoice_ids:
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
                    bill_ids = self.env["account.move"].search(
                        [("move_type", "=", "in_invoice")], order="id desc"
                    )

                    if bill_ids:
                        for bill_id in bill_ids:
                            invoice_line = bill_id.invoice_line_ids.filtered(
                                lambda inv_line: inv_line.product_id.id == line.product_id.id
                            )

                            if invoice_line:
                                line.value = invoice_line[0].price_unit * line.available_quantity
                                break
