from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange("sale_order_template_id")
    def _onchange_sale_order_template_id(self):
        for line in self:
            if line.sale_order_template_id:
                line.fiscal_position_id = line.sale_order_template_id.fiscal_position_id

            line.order_line._compute_tax_id()
