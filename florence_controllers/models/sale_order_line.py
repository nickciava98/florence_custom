from odoo import models, api, exceptions


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _check_line_vat(self):
        if (not self.display_type and "Free Sample" not in self.product_id.display_name != "Free Sample"
                and not self.tax_id):
            return f"VAT not present for {self.product_id.name} in Order nr. {self.order_id.name}"

        return ""

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)

        if "force_create" in self.env.context:
            return lines

        vat_errors = [line._check_line_vat() for line in lines]

        if vat_errors:
            raise exceptions.ValidationError("\n".join(vat_errors))

        return lines

    def write(self, values):
        res = super().write(values)

        if "force_create" in self.env.context:
            return res

        if "display_type" in values or "product_id" in values or "tax_id" in values:
            vat_errors = [line._check_line_vat() for line in self]

            if vat_errors:
                raise exceptions.ValidationError("\n".join(vat_errors))

        return res
