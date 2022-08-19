from odoo import models, fields, api
from datetime import datetime

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
    product_price = fields.Float(
        compute = "_compute_product_price"
    )
    start_date = fields.Date(
        default = datetime.today(),
        required = True
    )
    total_probable_income = fields.Float(
        compute = "_compute_total_probable_income",
        store = True
    )
    revenues_line = fields.One2many(
        "amazon.revenues.line",
        "amazon_revenues_line_id"
    )

    @api.depends("product")
    def _compute_product_price(self):
        if self.product.list_price:
            self.product_price = self.product.list_price
        else:
            self.product_price = self.product.lst_price

    @api.depends("revenues_line")
    def _compute_total_probable_income(self):
        for line in self:
            line.total_probable_income = 0

            for revenues_line in line.revenues_line:
                if revenues_line.probable_income:
                    line.total_probable_income += revenues_line.probable_income
