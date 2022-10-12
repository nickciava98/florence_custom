from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = "account.move"

    is_free_sample = fields.Boolean(
        compute = "_compute_is_free_sample"
    )

    is_free_sample_stored = fields.Boolean(
        related = "is_free_sample",
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
    amount_subtotal = fields.Float(
        compute = "_compute_amount_subtotal",
        string = "Subtotal"
    )
    amount_discount = fields.Monetary(
        string = "Discount",
        compute = "_compute_amount_discount",
        store = True
    )

    @api.depends(
        'line_ids.matched_debit_ids.debit_move_id.move_id.line_ids.amount_residual',
        'line_ids.matched_debit_ids.debit_move_id.move_id.line_ids.amount_residual_currency',
        'line_ids.matched_credit_ids.credit_move_id.move_id.line_ids.amount_residual',
        'line_ids.matched_credit_ids.credit_move_id.move_id.line_ids.amount_residual_currency',
        'line_ids.debit',
        'line_ids.credit',
        'line_ids.currency_id',
        'line_ids.amount_currency',
        'line_ids.amount_residual',
        'line_ids.amount_residual_currency',
        'line_ids.payment_id.state',
        'line_ids.full_reconcile_id')
    def _compute_amount_discount(self):
        for move in self:
            if move.payment_state == 'invoicing_legacy':
                move.payment_state = move.payment_state
                continue

            total_untaxed = 0.0
            total_untaxed_currency = 0.0
            total_tax = 0.0
            total_tax_currency = 0.0
            total_to_pay = 0.0
            total_residual = 0.0
            total_residual_currency = 0.0
            total = 0.0
            total_currency = 0.0
            currencies = set()

            for line in move.line_ids:
                if line.currency_id:
                    currencies.add(line.currency_id)

                if move.is_invoice(include_receipts=True):
                    if not line.exclude_from_invoice_tab:
                        total_untaxed += line.balance
                        total_untaxed_currency += line.amount_currency
                        total += line.balance
                        total_currency += line.amount_currency
                    elif line.tax_line_id:
                        total_tax += line.balance
                        total_tax_currency += line.amount_currency
                        total += line.balance
                        total_currency += line.amount_currency
                    elif line.account_id.user_type_id.type in ('receivable', 'payable'):
                        total_to_pay += line.balance
                        total_residual += line.amount_residual
                        total_residual_currency += line.amount_residual_currency
                else:
                    if line.debit:
                        total += line.balance
                        total_currency += line.amount_currency

            if move.move_type == 'entry' or move.is_outbound():
                sign = 1
            else:
                sign = -1

            if move.discount_type == 'percent':
                move.amount_discount = sum(
                    (line.quantity * line.price_unit * line.discount) / 100 for line in move.invoice_line_ids)
            else:
                move.amount_discount = move.discount_rate

            currency = len(currencies) == 1 and currencies.pop() or move.company_id.currency_id

            new_pmt_state = 'not_paid' if move.move_type != 'entry' else False

            if move.is_invoice(include_receipts=True) and move.state == 'posted':
                if currency.is_zero(move.amount_residual):
                    if all(payment.is_matched for payment in move._get_reconciled_payments()):
                        new_pmt_state = 'paid'
                    else:
                        new_pmt_state = move._get_invoice_in_payment_state()
                elif currency.compare_amounts(total_to_pay, total_residual) != 0:
                    new_pmt_state = 'partial'

            if new_pmt_state == 'paid' and move.move_type in ('in_invoice', 'out_invoice', 'entry'):
                reverse_type = move.move_type == 'in_invoice' and 'in_refund' or move.move_type == 'out_invoice' and 'out_refund' or 'entry'
                reverse_moves = self.env['account.move'].search(
                    [('reversed_entry_id', '=', move.id), ('state', '=', 'posted'), ('move_type', '=', reverse_type)])
                reverse_moves_full_recs = reverse_moves.mapped('line_ids.full_reconcile_id')

                if reverse_moves_full_recs.mapped('reconciled_line_ids.move_id').filtered(lambda x: x not in (
                        reverse_moves + reverse_moves_full_recs.mapped('exchange_move_id'))) == move:
                    new_pmt_state = 'reversed'

            move.payment_state = new_pmt_state

    @api.depends("invoice_line_ids")
    def _compute_amount_subtotal(self):
        for line in self:
            line.amount_subtotal = 0

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
