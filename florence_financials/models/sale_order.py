from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    related_invoice = fields.Char(
        compute="_compute_related_invoice"
    )

    def _compute_related_invoice(self):
        for line in self:
            line.related_invoice = ", ".join([invoice.name for invoice in line.invoice_ids]) \
                if line.invoice_ids else False

    @api.onchange("sale_order_template_id")
    def _onchange_sale_order_template_id(self):
        for line in self:
            if line.sale_order_template_id:
                line.fiscal_position_id = line.sale_order_template_id.fiscal_position_id

            line.order_line._compute_tax_id()
