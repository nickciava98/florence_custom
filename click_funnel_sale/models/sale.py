from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    click_funnel_charge_id = fields.Char(string='Click Funnel Charge ID', index=True)
    click_funnel_id = fields.Many2one('click.funnel', string='Click Funnel', check_company=True)