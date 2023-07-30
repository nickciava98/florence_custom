from odoo import models, fields, api


class MrpBomLine(models.Model):
    _inherit = "mrp.bom.line"

    cost = fields.Float(
        compute="_compute_bill",
        digits=(12, 4)
    )
    currency_id = fields.Many2one(
        "res.currency",
        compute="_compute_currency_id"
    )
    bill = fields.Many2one(
        "account.move",
        compute="_compute_bill"
    )
    bill_date = fields.Date(
        related="bill.invoice_date"
    )

    @api.depends("product_id", "product_qty")
    def _compute_bill(self):
        for line in self:
            line.bill = False
            line.cost = 0.0

            if line.product_id:
                for bill in self.env["account.move"].search(
                        [("move_type", "=", "in_invoice")], order="name desc"):
                    for invoice_line in bill.invoice_line_ids:
                        if invoice_line.product_id.id == line.product_id.id:
                            line.bill = bill
                            line.cost = invoice_line.price_unit * line.product_qty
                            break
                    if line.bill and line.cost > 0.0:
                        break

    def _compute_currency_id(self):
        for line in self:
            line.currency_id = self.env.ref('base.main_company').currency_id
