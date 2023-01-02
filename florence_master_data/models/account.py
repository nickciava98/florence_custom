from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse')