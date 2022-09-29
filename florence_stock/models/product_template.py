from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

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
        store = True
    )
    qty_available = fields.Float(
        store = True
    )

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
