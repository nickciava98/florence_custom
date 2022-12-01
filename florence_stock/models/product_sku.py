from odoo import models, fields


class ProductSku(models.Model):
    _name = "product.sku"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Product SKU"

    name = fields.Char(
        required = True
    )
    product_id = fields.Many2one(
        "product.product",
        required = True
    )
