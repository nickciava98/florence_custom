from odoo import models, fields, api
from datetime import datetime

class AmazonRevenues(models.Model):
    _name = "amazon.revenues"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Amazon Revenues Model"

    name = fields.Selection(
        [("IT", "Amazon IT"),
         ("FR", "Amazon FR"),
         ("DE", "Amazon DE"),
         ("ES", "Amazon ES"),
         ("UK", "Amazon UK")],
        required = True,
        string = "Marketplace",
        tracking = True
    )
    marketplace = fields.Selection(
        [("IT", "Amazon IT"),
         ("FR", "Amazon FR"),
         ("DE", "Amazon DE"),
         ("ES", "Amazon ES"),
         ("UK", "Amazon UK")]
    )
    product = fields.Many2one(
        "product.product",
        required = True,
        tracking = True
    )
    product_updated_price = fields.Float(
        compute = "_compute_product_updated_price"
    )
    start_date = fields.Date(
        compute = "_compute_start_date"
    )
    total_probable_income = fields.Float(
        compute = "_compute_total_probable_income",
        store = True
    )
    revenues_line = fields.One2many(
        "amazon.revenues.line",
        "amazon_revenues_line_id"
    )
    currency_id = fields.Many2one(
        "res.currency",
        compute = "_compute_currency_id"
    )
    product_updated_sku_cost = fields.Float(
        compute = "_compute_product_updated_sku_cost"
    )

    @api.onchange("marketplace")
    def _onchange_marketplace(self):
        for line in self:
            line.name = False
            
            if line.marketplace:
                line.name = line.marketplace

    def _compute_start_date(self):
        for line in self:
            line.start_date = datetime.now()

    def _compute_currency_id(self):
        for line in self:
            line.currency_id = self.env.ref('base.main_company').currency_id

    @api.depends("product")
    def _compute_product_updated_price(self):
        for line in self:
            line.product_updated_price = 0

            if line.product.list_price:
                line.product_updated_price = line.product.list_price
            else:
                line.product_updated_price = line.product.lst_price

    @api.depends("revenues_line")
    def _compute_total_probable_income(self):
        for line in self:
            line.total_probable_income = 0

            for revenues_line in line.revenues_line:
                if revenues_line.probable_income:
                    line.total_probable_income += revenues_line.probable_income

    @api.depends("product")
    def _compute_product_updated_sku_cost(self):
        for line in self:
            line.product_updated_sku_cost = 0

            if line.product.bom_count >= 1:
                for bom_id in line.product.bom_ids:
                    for bom_line_id in bom_id.bom_line_ids:
                        for seller_id in bom_line_id.product_id.seller_ids:
                            line.product_updated_sku_cost += seller_id.price
                            break
            else:
                line.product_updated_sku_cost = 0
