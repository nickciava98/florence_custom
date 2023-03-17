from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    order_type = fields.Char(
        compute = "_compute_order_type",
        store = True
    )
    amazon_order_country = fields.Many2one(
        "res.country",
        ondelete = "cascade",
        compute = "_compute_amazon_order_country",
        store = True
    )
    amazon_products = fields.Char(
        compute = "_compute_amazon_products",
        store = True
    )

    @api.depends("amazon_order_ref", "order_line")
    def _compute_amazon_products(self):
        for line in self:
            line.amazon_products = ""

            if line.amazon_order_ref and len(line.order_line) > 0:
                amazon_products = []

                for order_line in line.order_line:
                    if order_line.product_template_id and order_line.product_template_id.name != "Amazon Shipping":
                        if order_line.product_template_id.name == "Amazon Sale":
                            sku = order_line.name.split()[0][1:-1]
                            product = self.env["product.sku"].search(
                                [("name", "=", sku)], limit = 1
                            ).product_id.product_tmpl_id.name
                            amazon_products.append(product)
                        else:
                            amazon_products.append(order_line.product_template_id.name)

                if len(amazon_products) > 0:
                    line.amazon_products = "Amazon Products: " + ", ".join(map(str, amazon_products))

    @api.depends("amazon_order_ref")
    def _compute_amazon_order_country(self):
        for line in self:
            line.amazon_order_country = False

            if line.amazon_order_ref:
                line.amazon_order_country = line.partner_id.country_id

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
