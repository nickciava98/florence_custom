from odoo import models, fields, api

class AmazonRevenues(models.Model):
    _name = "amazon.revenues"
    _description = "Amazon Revenues Model"

    name = fields.Selection(
        [("IT", "Amazon IT"),
         ("FR", "Amazon FR"),
         ("DE", "Amazon DE"),
         ("ES", "Amazon ES"),
         ("UK", "Amazon UK")],
        required = True,
        string = "Marketplace"
    )
    product = fields.Many2one(
        "product.product",
        required = True
    )
    revenues_line = fields.One2many(
        "amazon.revenues.line",
        "amazon_revenues_line_id"
    )

