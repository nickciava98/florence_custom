from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = "account.move"

    is_free_sample = fields.Boolean(
        compute="_compute_is_free_sample",
        store=True,
        string="Free Sample?"
    )
    amount_untaxed_free_sample = fields.Monetary(
        compute="_compute_amount_untaxed_free_sample",
        store=True
    )
    amount_tax_free_sample = fields.Monetary(
        compute="_compute_amount_tax_free_sample",
        store=True
    )
    free_sample_total = fields.Monetary(
        compute="_compute_free_sample_total",
        store=True
    )
    amount_subtotal = fields.Float(
        compute="_compute_amount_subtotal",
        store=True,
        string="Subtotal"
    )
    amount_discount = fields.Monetary(
        compute="_compute_amount_discount",
        store=True,
        string="Discount"
    )

    @api.depends("invoice_line_ids", "invoice_line_ids.sale_line_ids", "invoice_line_ids.sale_line_ids.order_id",
                 "invoice_line_ids.sale_line_ids.order_id.amount_discount")
    def _compute_amount_discount(self):
        for line in self:
            sale_order_id = line.invoice_line_ids.filtered(
                lambda inv_line: inv_line.sale_line_ids.order_id
                                 and inv_line.sale_line_ids.order_id.amount_discount > .0
            )
            line.amount_discount = sale_order_id[0].sale_line_ids.order_id.amount_discount if sale_order_id else .0

    @api.depends("invoice_line_ids", "invoice_line_ids.total_price")
    def _compute_amount_subtotal(self):
        for line in self:
            line.amount_subtotal = sum([
                invoice_line.total_price for invoice_line in line.invoice_line_ids
            ])

    @api.depends("invoice_line_ids", "invoice_line_ids.sale_line_ids", "invoice_line_ids.sale_line_ids.order_id",
                 "invoice_line_ids.sale_line_ids.order_id.is_free_sample")
    def _compute_is_free_sample(self):
        for line in self:
            sale_order_id = line.invoice_line_ids.filtered(
                lambda inv_line: inv_line.sale_line_ids.order_id
                                 and inv_line.sale_line_ids.order_id.is_free_sample
            )
            line.is_free_sample = True if sale_order_id else False

    @api.depends("invoice_line_ids", "invoice_line_ids.sale_line_ids", "invoice_line_ids.sale_line_ids.order_id",
                 "invoice_line_ids.sale_line_ids.order_id.is_free_sample",
                 "invoice_line_ids.sale_line_ids.order_id.amount_untaxed_free_sample", "is_free_sample")
    def _compute_amount_untaxed_free_sample(self):
        for line in self:
            line.amount_untaxed_free_sample = .0

            if line.is_free_sample:
                sale_order_id = line.invoice_line_ids.filtered(
                    lambda inv_line: inv_line.sale_line_ids.order_id
                                     and inv_line.sale_line_ids.order_id.is_free_sample
                )

                if sale_order_id:
                    line.amount_untaxed_free_sample = sale_order_id[0].sale_line_ids.order_id.amount_untaxed_free_sample

                line.amount_untaxed_signed = line.amount_untaxed = .0

    @api.depends("invoice_line_ids", "invoice_line_ids.sale_line_ids", "invoice_line_ids.sale_line_ids.order_id",
                 "invoice_line_ids.sale_line_ids.order_id.is_free_sample",
                 "invoice_line_ids.sale_line_ids.order_id.amount_tax_free_sample", "is_free_sample")
    def _compute_amount_tax_free_sample(self):
        for line in self:
            line.amount_tax_free_sample = .0

            if line.is_free_sample:
                sale_order_id = line.invoice_line_ids.filtered(
                    lambda inv_line: inv_line.sale_line_ids.order_id
                                     and inv_line.sale_line_ids.order_id.is_free_sample
                )

                if sale_order_id:
                    line.amount_tax_free_sample = sale_order_id[0].sale_line_ids.order_id.amount_tax_free_sample

    @api.depends("invoice_line_ids", "invoice_line_ids.sale_line_ids", "invoice_line_ids.sale_line_ids.order_id",
                 "invoice_line_ids.sale_line_ids.order_id.is_free_sample",
                 "invoice_line_ids.sale_line_ids.order_id.free_sample_total", "is_free_sample")
    def _compute_free_sample_total(self):
        for line in self:
            line.free_sample_total = .0

            if line.is_free_sample:
                sale_order_id = line.invoice_line_ids.filtered(
                    lambda inv_line: inv_line.sale_line_ids.order_id
                                     and inv_line.sale_line_ids.order_id.is_free_sample
                )

                if sale_order_id:
                    line.free_sample_total = sale_order_id[0].sale_line_ids.order_id.free_sample_total
