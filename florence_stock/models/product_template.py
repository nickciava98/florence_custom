from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

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
        default=False,
        string="Finished Product?"
    )

    def _compute_location_ids(self):
        for line in self:
            stock_quant_ids = self.env["stock.quant"].search([("product_id", "=", line.id)])
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
