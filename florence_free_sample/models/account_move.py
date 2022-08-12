from odoo import models, fields

class AccountMove(models.Model):
    _inherit = "account.move"

    is_free_sample = fields.Boolean(
        compute = "_compute_is_free_sample"
    )

    amount_untaxed_free_sample = fields.Monetary(
        compute = "_compute_amount_untaxed_free_sample"
    )

    amount_tax_free_sample = fields.Monetary(
        compute = "_compute_amount_tax_free_sample"
    )

    free_sample_total = fields.Monetary(
        compute = "_compute_free_sample_total"
    )

    def _compute_is_free_sample(self):
        for line in self.invoice_line_ids:
            if line.sale_line_ids.order_id.is_free_sample:
                self.is_free_sample = True
            else:
                self.is_free_sample = False

    def _compute_amount_untaxed_free_sample(self):
        if self.is_free_sample:
            for line in self.invoice_line_ids:
                if line.sale_line_ids.order_id.amount_total == 0:
                    self.amount_untaxed_free_sample += line.sale_line_ids.order_id.amount_untaxed_free_sample
        else:
            self.amount_untaxed_free_sample = False

    def _compute_amount_tax_free_sample(self):
        if self.is_free_sample:
            for line in self.invoice_line_ids:
                if line.sale_line_ids.order_id.amount_total == 0:
                    self.amount_tax_free_sample += line.sale_line_ids.order_id.amount_tax_free_sample
        else:
            self.amount_tax_free_sample = False

    def _compute_free_sample_total(self):
        if self.is_free_sample:
            for line in self.invoice_line_ids:
                if line.sale_line_ids.order_id.amount_total == 0:
                    self.free_sample_total += line.sale_line_ids.order_id.free_sample_total
        else:
            self.free_sample_total = False
