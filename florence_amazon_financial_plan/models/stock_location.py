from odoo import models, fields


class StockLocation(models.Model):
    _inherit = "stock.location"

    is_valuable_stock = fields.Boolean(
        default=False
    )

    def name_get(self):
        return [
            (name[0], name[1] + " €€") if self.browse(name[0]).is_valuable_stock else name
            for name in super().name_get()
        ]
