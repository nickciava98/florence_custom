from odoo import fields, models


class StockDeliveryNote(models.Model):
    _inherit = "stock.delivery.note"

    fiscal_position_id = fields.Many2one(
        'account.fiscal.position', string='Fiscal Position', check_company=True)
