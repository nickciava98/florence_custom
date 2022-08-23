from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = "account.move"

    is_vendor_bill = fields.Boolean(
        compute = "_compute_is_vendor_bill"
    )

    is_manufacturing_bill = fields.Boolean()

    @api.depends("move_type")
    def _compute_is_vendor_bill(self):
        for line in self:
            line.is_vendor_bill = False

            if "in_" in line.move_type:
                line.is_vendor_bill = True
