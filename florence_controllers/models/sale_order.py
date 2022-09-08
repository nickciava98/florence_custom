from odoo import models, api, exceptions

class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.constrains("order_line")
    def constrains_order_line(self):
        for line in self:
            for order_line in line.order_line:
                if not order_line.tax_id:
                    raise exceptions.ValidationError(
                        "VAT must be present in sale order line!"
                    )
