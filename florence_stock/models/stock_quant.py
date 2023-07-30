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
        compute="_compute_currency_id",
        groups="stock.group_stock_manager"
    )
    sale_ok = fields.Boolean(
        related="product_id.sale_ok"
    )
    can_be_used = fields.Boolean(
        related="product_id.can_be_used"
    )

    @api.depends("company_id")
    def _compute_currency_id(self):
        for line in self:
            line.currency_id = line.company_id.currency_id

    @api.depends("product_id", "available_quantity")
    def _compute_value(self):
        for line in self:
            line.value = 0

            if line.product_id:
                cost = 0

                for bill in self.env["account.move"].search(
                        [("move_type", "=", "in_invoice")], order="name desc"):
                    for invoice_line in bill.invoice_line_ids:
                        if invoice_line.product_id == line.product_id:
                            cost = invoice_line.price_unit
                            break
                    if cost > 0:
                        break
                if cost > 0:
                    line.value = cost * line.available_quantity
