from odoo import models, fields

class SaleOrderTemplate(models.Model):
    _inherit = "sale.order.template"

    is_free_sample = fields.Boolean(
        store = True
    )