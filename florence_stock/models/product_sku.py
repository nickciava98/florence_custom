from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ProductSku(models.Model):
    _name = "product.sku"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Product SKU"

    name = fields.Char(
        copy = False
    )
    product_id = fields.Many2one(
        "product.product",
        required = True
    )

    @api.constrains("name")
    def _constrains_name(self):
        for line in self:
            if not line.name:
                raise ValidationError(
                    _("Name must be filled!")
                )

    _sql_constraint = [
        ("unique_name", "unique(name)", _("Name must be unique!"))
    ]
