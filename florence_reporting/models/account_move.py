from odoo import models, fields


class AccountMove(models.Model):
    _inherit = "account.move"

    document_type = fields.Char(
        compute="_compute_document_type"
    )

    def _compute_document_type(self):
        for line in self:
            inv_line_ids = line.invoice_line_ids.filtered(
                lambda l: l.sale_line_ids and l.sale_line_ids.order_id and l.sale_line_ids.order_id.document_type
            )
            line.document_type = ", ".join(
                list(dict.fromkeys([
                    inv_line.sale_line_ids.order_id.document_type for inv_line in inv_line_ids
                ]))
            ) if inv_line_ids else False
