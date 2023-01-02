from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    fiscal_entity_vat = fields.Char(string='Fiscal Entity')
    type = fields.Selection(selection_add=[('fiscal_entity', 'Fiscal Entity')])
