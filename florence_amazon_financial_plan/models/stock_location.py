from odoo import models, fields


class StockLocation(models.Model):
    _inherit = "stock.location"

    is_valuable_stock = fields.Boolean(
        default=False
    )
