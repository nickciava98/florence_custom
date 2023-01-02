from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    partner_bank_id = fields.Many2one('res.partner.bank', string='Partner Bank')

    def _prepare_invoice(self):
        vals = super()._prepare_invoice()
        if self.warehouse_id:
            vals["warehouse_id"] = self.warehouse_id.id
        return vals



