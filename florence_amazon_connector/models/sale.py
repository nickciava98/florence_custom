from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    order_type = fields.Char(
        compute = "_compute_order_type",
        store = True
    )

    @api.depends("amazon_order_ref")
    def _compute_order_type(self):
        for line in self:
            line.order_type = "Standard Order"

            if line.amazon_order_ref != False:
                line.order_type = "Amazon Order"

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    amazon_order_country = fields.Many2one(
        "res.country",
        ondelete = "cascade",
        compute = "_compute_amazon_order_country",
        store = True
    )

    @api.depends("order_id.amazon_order_ref")
    def _compute_amazon_order_country(self):
        for line in self:
            line.amazon_order_country = False

            if line.order_id.amazon_order_ref:
                line.amazon_order_country = line.order_id.partner_id.country_id
