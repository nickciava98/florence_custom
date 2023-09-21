from odoo.osv import expression

from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = "product.product"

    display_value = fields.Char(
        compute="_compute_display_value",
        store=True
    )
    is_decommissioned = fields.Boolean(
        default=False
    )
    can_be_used = fields.Boolean(
        default=True
    )
    location_ids = fields.Many2many(
        "stock.location",
        string="Locations",
        compute="_compute_location_ids",
        store=True
    )
    locations_count = fields.Float(
        compute="_compute_locations_count",
        store=True
    )
    locations = fields.Char(
        compute="_compute_locations",
        store=True,
        string="Locations String"
    )
    qty_available = fields.Float(
        store=True,
        digits=(12, 4)
    )
    is_finished_product = fields.Boolean(
        related="product_tmpl_id.is_finished_product",
        store=True,
        string="Finished Product?"
    )

    @api.depends("name", "product_template_attribute_value_ids")
    def _compute_display_value(self):
        for line in self:
            values = [value.name for value in line.product_template_attribute_value_ids] \
                if line.product_template_attribute_value_ids else []
            line.display_value = line.name + f"{line.name} ({', '.join(values)})" \
                if line.name and values else line.name \
                if line.name and not values else False

    def _compute_location_ids(self):
        for line in self:
            stock_quant_ids = self.env["stock.quant"].search(
                [("product_id", "=", line.id)]
            )
            locations = [stock_quant.location_id.id for stock_quant in stock_quant_ids] if stock_quant_ids else []
            line.location_ids = [(6, 0, locations)] if locations else False

    @api.depends("location_ids")
    def _compute_locations_count(self):
        for line in self:
            line.locations_count = len(line.location_ids)

    @api.depends("location_ids")
    def _compute_locations(self):
        for line in self:
            line.locations = ""

            if line.location_ids:
                location_names = [
                    f"{location.location_id.name}/{location.name}"
                    for location in line.location_ids.filtered(
                        lambda l: l != line.property_stock_production and l != line.property_stock_inventory
                    )
                ]

                if location_names:
                    line.locations = ", ".join(location_names)

    @api.model
    def _name_search(self, name, args=None, operator="ilike", limit=100, name_get_uid=None):
        args = args or []
        domain = ["|", ("name", operator, name), ("display_value", operator, name)] if name else []

        return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
