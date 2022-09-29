from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = "product.template"

    property_stock_inventory_stored = fields.Many2one(
        "stock.location",
        string = "Inventory Location",
        compute = "_compute_property_stock_inventory_stored",
        store = True
    )
    qty_available = fields.Float(
        store = True
    )

    @api.depends("property_stock_inventory")
    def _compute_property_stock_inventory_stored(self):
        for line in self:
            line.property_stock_inventory_stored = line.property_stock_inventory
