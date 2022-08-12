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

    def _compute_add_free_sample_rule(self):
        if self.is_free_sample:
            self.add_free_sample_rule = True

            if not self.env["product.product"].search([('name','ilike','free sample')]):
                self.env["product.product"].sudo().create(
                    {
                        "name": "Free Sample",
                        "type": "consu",
                        "default_code": "Free Sample",
                        "categ_id": self.env.ref('product.product_category_all').id,
                        "uom_id": self.env.ref('uom.product_uom_unit').id,
                        "uom_po_id": self.env.ref('uom.product_uom_unit').id,
                        "product_variant_ids": False,
                    })

            free_sample = self.env["product.product"].search(
                ['&',('default_code','ilike','free sample'),('name','ilike','free sample')])

            if self.amount_total != 0 or self.free_sample_total >= 0:
                self.write({
                    'order_line': [
                        (0, 0, {
                            'order_id': self.order_line.order_id.id,
                            'product_id': free_sample.id,
                            'name': free_sample.name,
                            'product_uom_qty': 1,
                            'product_uom': self.env.ref('uom.product_uom_unit').id,
                            'price_unit': self.free_sample_total if self.free_sample_total < 0 else -self.amount_total,
                            'customer_lead': 0.0,
                            'discount': 0,
                            'company_id': self.order_line.order_id.company_id.id,
                        })
                    ]})

        else:
            self.add_free_sample_rule = False