from odoo import models, api, exceptions


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.constrains("tax_id")
    def constrains_tax_id(self):
        for line in self:
            if not line.display_type and line.product_id.default_code != "Free Sample" and not line.tax_id:
                raise exceptions.ValidationError(
                    "VAT must be present in sale order line!"
                )
