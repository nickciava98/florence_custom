from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_free_sample = fields.Boolean(
        related = "sale_order_template_id.is_free_sample",
        store = True
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

    def _compute_amount_untaxed_free_sample(self):
        if self.is_free_sample:
            for line in self.order_line:
                if line.price_subtotal > 0:
                    self.amount_untaxed_free_sample += line.price_subtotal
        else:
            self.amount_untaxed_free_sample = False

    def _compute_amount_tax_free_sample(self):
        if self.is_free_sample:
            for line in self.order_line:
                if line.price_reduce_taxinc > 0:
                    self.amount_tax_free_sample += (line.price_reduce_taxinc - line.price_unit) * line.product_uom_qty
        else:
            self.amount_tax_free_sample = False

    def _compute_free_sample_total(self):
        if self.is_free_sample:
            self.free_sample_total = -(self.amount_untaxed_free_sample + self.amount_tax_free_sample)
        else:
            self.free_sample_total = False