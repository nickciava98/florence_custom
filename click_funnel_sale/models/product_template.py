from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    _sql_constraints = [
        ('click_funnel_id_uniq', 'unique(click_funnel_id)', 'The click funnel id must be unique!'),
    ]

    click_funnel_id = fields.Integer(string='Click Funnel Product ID', index=True, copy=False)