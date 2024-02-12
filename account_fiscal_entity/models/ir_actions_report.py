from odoo import models


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    def _get_rendering_context(self, docids, data):
        data['fiscal_partner_id'] = False

        if self.model in ('sale.order', 'account.move', 'purchase.order', 'stock.delivery.note'):
            ids = self.env[self.model].sudo().browse(docids)

            if ids and ids[0].fiscal_position_id and ids[0].fiscal_position_id.fiscal_partner_id:
                data['fiscal_partner_id'] = ids[0].fiscal_position_id.fiscal_partner_id

        return super(IrActionsReport, self)._get_rendering_context(docids, data)
