from odoo import models, fields

class SaleOrderTemplateLine(models.Model):
    _inherit = "sale.order.template.line"

    discount = fields.Float(
        string = "Disc.%"
    )