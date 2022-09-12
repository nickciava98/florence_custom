from odoo import models, fields

class SaleOrderTemplate(models.Model):
    _inherit = "sale.order.template"

    document_type = fields.Char(
        store = True
    )
