from odoo import models, fields

class AccountMove(models.Model):
    _inherit = "account.move"

    document_type = fields.Char(
        compute = "_compute_document_type"
    )

    def _compute_document_type(self):
        types = []

        for line in self.invoice_line_ids:
            if line.sale_line_ids.order_id.document_type:
                types.append(line.sale_line_ids.order_id.document_type)

        if len(types) > 0:
            self.document_type = ",".join(types)

        else:
            self.document_type = False