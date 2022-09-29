from odoo import models, fields

class ProductProduct(models.Model):
    _inherit = "product.product"

    qty_available = fields.Float(
        store = True
    )
