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

    add_free_sample_rule = fields.Boolean(
        compute = "_compute_add_free_sample_rule"
    )

    def _compute_amount_untaxed_free_sample(self):
        for line in self:
            line.amount_untaxed_free_sample = 0

            if line.is_free_sample:
                for order_line in line.order_line:
                    if order_line.price_subtotal >= 0:
                        line.amount_untaxed_free_sample += order_line.price_subtotal

    def _compute_amount_tax_free_sample(self):
        for line in self:
            line.amount_tax_free_sample = 0

            if line.is_free_sample:
                for order_line in line.order_line:
                    if order_line.price_reduce_taxinc >= 0:
                        line.amount_tax_free_sample += \
                            (order_line.price_reduce_taxinc
                             - order_line.price_unit * (1 - order_line.discount / 100)) * order_line.product_uom_qty

    def _compute_free_sample_total(self):
        for line in self:
            line.free_sample_total = 0

            if line.is_free_sample:
                line.free_sample_total = \
                    -(line.amount_untaxed_free_sample + line.amount_tax_free_sample)

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
