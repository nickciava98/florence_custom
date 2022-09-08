from odoo import models, fields
from datetime import datetime

class AmazonStatistics(models.Model):
    _name = "amazon.statistics"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Amazon Statistics"

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
    statistics_lines = fields.One2many(
        "amazon.statistics.line",
        "name"
    )
    start_date = fields.Date(
        compute = "_compute_start_date"
    )

    def _compute_start_date(self):
        for line in self:
            line.start_date = datetime.now()

    def graph_view_action(self):
        return {
            'name': 'Statistics Analysis',
            'view_type': 'graph',
            'view_mode': 'graph',
            'res_model': 'amazon.statistics.line',
            'type': 'ir.actions.act_window',
            'domain': [
                '&',
                ('product', '=', self.product.id),
                ('parent', '=', self.name)
            ],
            'context': {
                'graph_measure': 'main_stat',
                'graph_mode': 'line',
                'graph_groupbys': ['date:day']
            }
        }

    def tree_view_action(self):
        return {
            'name': 'Statistics List',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'view_id': False,
            'res_model': 'amazon.statistics.line',
            'type': 'ir.actions.act_window',
            'context': {
                'group_by': ['date:year', 'date:month']
            },
            'domain': [
                '&',
                ('product', '=', self.product.id),
                ('parent', '=', self.name)
            ],
            'target': 'current'
        }
