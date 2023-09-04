import math

from odoo import models, fields, api


class MrpBomLine(models.Model):
    _inherit = "mrp.bom.line"

    cost = fields.Float(
        compute="_compute_bill",
        store=True,
        digits=(12, 4)
    )
    currency_id = fields.Many2one(
        "res.currency",
        related="bill.currency_id",
        store=True
    )
    bill = fields.Many2one(
        "account.move",
        compute="_compute_bill",
        store=True
    )
    bill_date = fields.Date(
        related="bill.invoice_date",
        store=True
    )

    @api.depends("product_id", "product_qty")
    def _compute_bill(self):
        for line in self:
            line.bill = False
            line.cost = .0
            purchase_ids = self.env["purchase.order"].search([], order="id desc")

            if line.product_id:
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
                                    line.cost = invoice_line[0].price_unit * line.product_qty
                                    break
                        else:
                            line.cost = order_line[0].price_unit * line.product_qty

                    break

                if math.isclose(line.cost, .0):
                    bill_ids = self.env["account.move"].search(
                        [("move_type", "=", "in_invoice")], order="id desc"
                    )

                    if bill_ids:
                        for bill_id in bill_ids:
                            invoice_line = bill_id.invoice_line_ids.filtered(
                                lambda inv_line: inv_line.product_id.id == line.product_id.id
                            )

                            if invoice_line:
                                line.cost = invoice_line[0].price_unit * line.product_qty
                                break
