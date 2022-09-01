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
        "product.template",
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
    revenues_line_test = fields.One2many(
        "amazon.revenues.line",
        "amazon_revenues_line_id_test"
    )
    currency_id = fields.Many2one(
        "res.currency",
        compute = "_compute_currency_id"
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

    def graph_view_action(self):
        return {
            'name': 'Revenues Analysis',
            'view_type': 'graph',
            'view_mode': 'graph',
            'res_model': 'amazon.revenues.line',
            'type': 'ir.actions.act_window',
            'domain': [
                '&',
                ('product', '=', self.product.id),
                ('amazon_revenues_line_id_test', '=', False)
            ],
            'context': {
                'graph_measure': 'probable_income',
                'graph_mode': 'line',
                'graph_groupbys': ['date:day']
            }
        }

    def tree_view_action(self):
        return {
            'name': 'Revenues List',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'view_id': False,
            'res_model': 'amazon.revenues.line',
            'type': 'ir.actions.act_window',
            'context': {
                'group_by': ['date:year', 'date:month']
            },
            'domain': [
                '&',
                ('product', '=', self.product.id),
                ('amazon_revenues_line_id_test', '=', False)
            ],
            'target': 'current'
        }
