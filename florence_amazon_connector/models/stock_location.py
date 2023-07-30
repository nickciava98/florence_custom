from odoo import models, fields


class StockLocation(models.Model):
    _inherit = "stock.location"

    amazon_mktp_ids = fields.Many2many(
        "amazon.marketplace",
        "amz_mktp_location_rel",
        string="Amazon Marketplaces"
    )
