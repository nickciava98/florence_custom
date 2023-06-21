from odoo import models, fields, api
from odoo.osv import expression


class ProductProduct(models.Model):
    _inherit = "product.product"

    display_value = fields.Char(
        compute = "_compute_display_value",
        store = True
    )
    is_decommissioned = fields.Boolean(
        default = False
    )
    can_be_used = fields.Boolean(
        default = True
    )
    location_ids = fields.Many2many(
        "stock.location",
        string = "Locations",
        compute = "_compute_location_ids",
        store = True
    )
    locations_count = fields.Float(
        compute = "_compute_locations_count",
        store = True
    )
    locations = fields.Char(
        compute = "_compute_locations",
        store = True,
        string = "Locations String"
    )
    qty_available = fields.Float(
        store = True,
        digits = (12, 4)
    )

    @api.depends("name", "product_template_attribute_value_ids")
    def _compute_display_value(self):
        for line in self:
            values = [value.name for value in line.product_template_attribute_value_ids] \
                if len(line.product_template_attribute_value_ids) > 0 else []
            line.display_value = line.name + " (" + ", ".join(values) + ")" \
                if line.name and len(values) > 0 else line.name \
                if line.name and len(values) == 0 else ""

    def _compute_location_ids(self):
        for line in self:
            line.location_ids = False

            stock_quant_ids = self.env["stock.quant"].search(
                [("product_id", "=", line.id)]
            )

            if len(stock_quant_ids) > 0:
                locations = []

                for stock_quant in stock_quant_ids:
                    locations.append(stock_quant.location_id.id)

                line.location_ids = [(6, 0, locations)]

    @api.depends("location_ids")
    def _compute_locations_count(self):
        for line in self:
            line.locations_count = len(line.location_ids)

    @api.depends("location_ids")
    def _compute_locations(self):
        for line in self:
            line.locations = ""

            if len(line.location_ids) > 0:
                location_names = []

                for location in line.location_ids:
                    if location != line.property_stock_production \
                            and location != line.property_stock_inventory:
                        location_names.append(location.location_id.name + "/" + location.name)

                if len(location_names) > 0:
                    line.locations = ", ".join(location_names)

    @api.model
    def _name_search(self, name, args = None, operator = "ilike", limit = 100, name_get_uid = None):
        args = args or []
        domain = ["|", ("name", operator, name), ("display_value", operator, name)] if name else []

        return self._search(expression.AND([domain, args]), limit = limit, access_rights_uid = name_get_uid)
