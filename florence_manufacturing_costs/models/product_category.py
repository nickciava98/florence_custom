from odoo import models, fields

class ProductCategory(models.Model):
    _inherit = "product.category"

    is_manufacturing_product_category = fields.Boolean()
