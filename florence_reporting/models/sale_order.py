from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = "sale.order"

    document_type = fields.Char(
        related = "sale_order_template_id.document_type",
        store = True
    )
