from odoo import models, fields, api


class MrpBomLine(models.Model):
    _inherit = "mrp.bom.line"

    cost = fields.Float(
        compute = "_compute_cost",
        digits = (12, 4)
    )
    currency_id = fields.Many2one(
        "res.currency",
        compute = "_compute_currency_id"
    )

    def _compute_currency_id(self):
        for line in self:
            line.currency_id = self.env.ref('base.main_company').currency_id

    @api.depends("product_id", "product_qty")
    def _compute_cost(self):
        for line in self:
            line.cost = 0

            if line.product_id:
                for bill in self.env["account.move"].search(
                    [("move_type", "=", "in_invoice")], order = "name desc"):
                    for invoice_line in bill.invoice_line_ids:
                        if invoice_line.product_id == line.product_id:
                            line.cost = line.product_qty * \
                                        (invoice_line.price_unit
                                         + ((invoice_line.price_total
                                             - invoice_line.price_subtotal) / invoice_line.quantity))
                            break

                    if line.cost > 0:
                        break
