import math
from datetime import timedelta

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_free_sample = fields.Boolean(
        related="sale_order_template_id.is_free_sample",
        store=True
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
    add_free_sample_rule = fields.Boolean(
        compute="_compute_add_free_sample_rule",
        store=True
    )
    amount_subtotal = fields.Float(
        compute="_compute_amount_subtotal",
        store=True,
        string="Subtotal",
        digits=(12, 4)
    )
    amount_discount = fields.Monetary(
        compute="_compute_amount_discount",
        store=True
    )

    @api.depends("order_line", "order_line.product_uom_qty", "order_line.price_unit", "order_line.discount")
    def _compute_amount_discount(self):
        for order in self:
            order.amount_discount = sum([
                line.product_uom_qty * line.price_unit * line.discount / 100 for line in order.order_line
            ])

    @api.depends("order_line", "order_line.price_total")
    def _compute_amount_subtotal(self):
        for line in self:
            line.amount_subtotal = sum([
                order_line.price_total for order_line in line.order_line
            ])

    @api.depends("is_free_sample", "order_line", "order_line.price_subtotal")
    def _compute_amount_untaxed_free_sample(self):
        for line in self:
            line.amount_untaxed_free_sample = sum([
                order_line.price_subtotal for order_line in line.order_line.filtered(
                    lambda ol: ol.price_subtotal > 0 or math.isclose(ol.price_subtotal, .0)
                )
            ]) if line.is_free_sample else .0

    @api.depends("is_free_sample", "order_line", "order_line.price_reduce_taxinc", "order_line.price_unit",
                 "order_line.discount", "order_line.product_uom_qty")
    def _compute_amount_tax_free_sample(self):
        for line in self:
            line.amount_tax_free_sample = sum([
                (order_line.price_reduce_taxinc - order_line.price_unit * (1 - order_line.discount / 100))
                * order_line.product_uom_qty
                for order_line in line.order_line.filtered(
                    lambda ol: ol.price_reduce_taxinc > 0 or math.isclose(ol.price_reduce_taxinc, .0)
                )
            ])

    @api.depends("is_free_sample", "amount_untaxed_free_sample", "amount_tax_free_sample")
    def _compute_free_sample_total(self):
        for line in self:
            line.free_sample_total = -(line.amount_untaxed_free_sample + line.amount_tax_free_sample) \
                if line.is_free_sample else .0

    @api.depends("is_free_sample", "order_line", "free_sample_total")
    def _compute_add_free_sample_rule(self):
        for line in self:
            if line.is_free_sample:
                line.add_free_sample_rule = True
                free_sample_product_id = self.env["product.product"].search(
                    [("default_code", "ilike", "Free Sample")], limit=1
                )

                if not free_sample_product_id:
                    free_sample_product_id = self.env["product.product"].create({
                        "name": "Free Sample",
                        "type": "consu",
                        "default_code": "Free Sample",
                        "categ_id": self.env.ref("product.product_category_all").id,
                        "uom_id": self.env.ref("uom.product_uom_unit").id,
                        "uom_po_id": self.env.ref("uom.product_uom_unit").id,
                        "product_variant_ids": False,
                        "taxes_id": False,
                        "invoice_policy": "order"
                    })

                free_sample_present = True if line.order_line.filtered(
                    lambda ol: ol.product_id.id == free_sample_product_id.id
                ) else False

                if not free_sample_present:
                    price_unit = -line.amount_untaxed_free_sample \
                        if line.amount_untaxed_free_sample > .0 else -line.amount_untaxed
                    line.order_line = [(0, 0, {
                        "product_id": free_sample_product_id.id,
                        "name": free_sample_product_id.name,
                        "product_uom_qty": 1.,
                        "product_uom": free_sample_product_id.uom_id.id,
                        "price_unit": price_unit,
                        "tax_id": line.order_line[0].tax_id.ids,
                        "customer_lead": .0,
                        "discount": .0,
                        "company_id": line.company_id.id,
                    })]

            else:
                line.add_free_sample_rule = False

    @api.onchange("sale_order_template_id")
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
