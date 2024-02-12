from odoo import fields, models


class AccountFiscalPosition(models.Model):
    _inherit = "account.fiscal.position"

    fiscal_partner_id = fields.Many2one(
        'res.partner',
        string='Fiscal Entity'
    )
