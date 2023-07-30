from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = "account.move"

    is_free_sample = fields.Boolean(
        compute="_compute_is_free_sample",
        string="Original Is Free Sample"
    )
    is_free_sample_stored = fields.Boolean(
        related="is_free_sample",
        store=True,
        string="Is Free Sample"
    )
    amount_untaxed_free_sample = fields.Monetary(
        compute="_compute_amount_untaxed_free_sample"
    )
    amount_tax_free_sample = fields.Monetary(
        compute="_compute_amount_tax_free_sample"
    )
    free_sample_total = fields.Monetary(
        compute="_compute_free_sample_total"
    )
    amount_subtotal = fields.Float(
        compute="_compute_amount_subtotal",
        string="Subtotal"
    )
    amount_discount = fields.Monetary(
        compute="_compute_amount_discount",
        string="Discount"
    )

    @api.depends("invoice_line_ids")
    def _compute_amount_discount(self):
        for line in self:
            line.amount_discount = 0

            for invoice_line in line.invoice_line_ids:
                if invoice_line.sale_line_ids.order_id.amount_discount > 0:
                    line.amount_discount = invoice_line.sale_line_ids.order_id.amount_discount
                    break

    @api.depends("invoice_line_ids")
    def _compute_amount_subtotal(self):
        for line in self:
            line.amount_subtotal = .0

            for invoice_line in line.invoice_line_ids:
                line.amount_subtotal += invoice_line.total_price

    @api.depends("invoice_line_ids")
    def _compute_is_free_sample(self):
        for line in self:
            line.is_free_sample = False

            for invoice_line in line.invoice_line_ids:
                if invoice_line.sale_line_ids.order_id.is_free_sample:
                    line.is_free_sample = True
                    break

    @api.depends("is_free_sample")
    def _compute_amount_untaxed_free_sample(self):
        for line in self:
            line.amount_untaxed_free_sample = 0

            if line.is_free_sample:
                for invoice_line in line.invoice_line_ids:
                    if invoice_line.sale_line_ids.order_id.amount_total == 0:
                        line.amount_untaxed_free_sample = invoice_line.sale_line_ids.order_id.amount_untaxed_free_sample
                        line.amount_untaxed_signed = line.amount_untaxed = .0
                        break

    @api.depends("is_free_sample")
    def _compute_amount_tax_free_sample(self):
        for line in self:
            line.amount_tax_free_sample = 0

            if line.is_free_sample:
                for invoice_line in line.invoice_line_ids:
                    if invoice_line.sale_line_ids.order_id.amount_total == 0:
                        line.amount_tax_free_sample = invoice_line.sale_line_ids.order_id.amount_tax_free_sample

    @api.depends("is_free_sample")
    def _compute_free_sample_total(self):
        for line in self:
            line.free_sample_total = 0

            if line.is_free_sample:
                for invoice_line in line.invoice_line_ids:
                    if invoice_line.sale_line_ids.order_id.amount_total == 0:
                        line.free_sample_total = invoice_line.sale_line_ids.order_id.free_sample_total
