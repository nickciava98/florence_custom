from datetime import timedelta
from odoo import models, fields, api

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

    add_free_sample_rule = fields.Boolean(
        compute = "_compute_add_free_sample_rule"
    )
    amount_subtotal = fields.Float(
        compute = "_compute_amount_subtotal",
        string = "Subtotal",
        store = True
    )
    amount_discount = fields.Monetary(
        compute = "_compute_amount_discount",
        store = True
    )

    @api.depends("order_line.price_total")
    def _compute_amount_discount(self):
        for order in self:
            amount_discount = 0.0

            for line in order.order_line:
                amount_discount += (line.product_uom_qty * line.price_unit * line.discount) / 100

            order.update({
                "amount_discount": amount_discount
            })

    @api.depends("order_line")
    def _compute_amount_subtotal(self):
        for line in self:
            line.amount_subtotal = 0

            for order_line in line.order_line:
                line.amount_subtotal += order_line.price_total

    @api.depends("is_free_sample", "order_line")
    def _compute_amount_untaxed_free_sample(self):
        for line in self:
            line.amount_untaxed_free_sample = 0

            if line.is_free_sample:
                for order_line in line.order_line:
                    if order_line.price_subtotal >= 0:
                        line.amount_untaxed_free_sample += order_line.price_subtotal

    @api.depends("is_free_sample", "order_line")
    def _compute_amount_tax_free_sample(self):
        for line in self:
            line.amount_tax_free_sample = 0

            if line.is_free_sample:
                for order_line in line.order_line:
                    if order_line.price_reduce_taxinc >= 0:
                        line.amount_tax_free_sample += \
                            (order_line.price_reduce_taxinc
                             - order_line.price_unit * (1 - order_line.discount / 100)) * order_line.product_uom_qty

    @api.depends("is_free_sample", "amount_untaxed_free_sample", "amount_tax_free_sample")
    def _compute_free_sample_total(self):
        for line in self:
            line.free_sample_total = 0

            if line.is_free_sample:
                line.free_sample_total = \
                    -(line.amount_untaxed_free_sample + line.amount_tax_free_sample)

    @api.depends("is_free_sample", "order_line", "free_sample_total")
    def _compute_add_free_sample_rule(self):
        for line in self:
            if line.is_free_sample:
                line.add_free_sample_rule = True

                if not self.env["product.product"].search([('default_code','ilike','free sample')]):
                    self.env["product.product"].sudo().create(
                        {
                            "name": "Free Sample",
                            "type": "consu",
                            "default_code": "Free Sample",
                            "categ_id": self.env.ref('product.product_category_all').id,
                            "uom_id": self.env.ref('uom.product_uom_unit').id,
                            "uom_po_id": self.env.ref('uom.product_uom_unit').id,
                            "product_variant_ids": False,
                            "taxes_id": False,
                            "invoice_policy": "order"
                        })

                free_sample = self.env["product.product"].search([('default_code','ilike','free sample')])
                free_sample_present = False

                for order_line in line.order_line:
                    if order_line.product_id.name == free_sample.name:
                        free_sample_present = True
                        break

                if not free_sample_present:
                    self.write({
                        'order_line': [
                            (0, 0, {
                                'order_id': line.order_line.order_id.id,
                                'product_id': free_sample.id,
                                'name': free_sample.name,
                                'product_uom_qty': 1,
                                'product_uom': self.env.ref('uom.product_uom_unit').id,
                                'price_unit': line.free_sample_total if line.free_sample_total < 0 else -line.amount_total,
                                'customer_lead': 0.0,
                                'discount': 0,
                                'company_id': line.order_line.order_id.company_id.id,
                            })
                        ]})

            else:
                line.add_free_sample_rule = False

    @api.onchange('sale_order_template_id')
    def onchange_sale_order_template_id(self):
        if not self.sale_order_template_id:
            self.require_signature = self._get_default_require_signature()
            self.require_payment = self._get_default_require_payment()
            return

        template = self.sale_order_template_id.with_context(lang=self.partner_id.lang)

        # --- first, process the list of products from the template
        order_lines = [(5, 0, 0)]
        for line in template.sale_order_template_line_ids:
            data = self._compute_line_data_for_template_change(line)

            if line.product_id:
                price = line.product_id.lst_price
                discount = line.discount

                if self.pricelist_id:
                    pricelist_price = self.pricelist_id.with_context(uom=line.product_uom_id.id).get_product_price(
                        line.product_id, 1, False)

                    if self.pricelist_id.discount_policy == 'without_discount' and price:
                        discount = max(0, (price - pricelist_price) * 100 / price)
                    else:
                        price = pricelist_price

                data.update({
                    'price_unit': price,
                    'discount': discount,
                    'product_uom_qty': line.product_uom_qty,
                    'product_id': line.product_id.id,
                    'product_uom': line.product_uom_id.id,
                    'customer_lead': self._get_customer_lead(line.product_id.product_tmpl_id),
                })

            order_lines.append((0, 0, data))

        self.order_line = order_lines
        self.order_line._compute_tax_id()

        # then, process the list of optional products from the template
        option_lines = [(5, 0, 0)]
        for option in template.sale_order_template_option_ids:
            data = self._compute_option_data_for_template_change(option)
            option_lines.append((0, 0, data))

        self.sale_order_option_ids = option_lines

        if template.number_of_days > 0:
            self.validity_date = fields.Date.context_today(self) + timedelta(template.number_of_days)

        self.require_signature = template.require_signature
        self.require_payment = template.require_payment

        if template.note:
            self.note = template.note
