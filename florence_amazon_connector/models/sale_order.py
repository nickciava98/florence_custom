from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    amazon_mktp_ids = fields.Many2many(
        "amazon.marketplace",
        "amz_mktp_sale_order_rel",
        compute="_compute_amazon_marketplaces",
        store=True,
        string="Amazon Marketplaces"
    )
    amazon_locations = fields.Char(
        compute="_compute_amazon_marketplaces",
        store=True,
        string="Amazon Locations"
    )

    @api.depends("warehouse_id")
    def _compute_amazon_marketplaces(self):
        for line in self:
            line.amazon_mktp_ids = False
            line.amazon_locations = "Standard Order"

            if line.warehouse_id and line.warehouse_id.lot_stock_id and line.warehouse_id.lot_stock_id.amazon_mktp_ids:
                mktp_ids = [mktp.id for mktp in line.warehouse_id.lot_stock_id.amazon_mktp_ids]
                mktps = [mktp.domain for mktp in line.warehouse_id.lot_stock_id.amazon_mktp_ids]
                line.amazon_mktp_ids = [(6, 0, mktp_ids)] if mktp_ids else False
                line.amazon_locations = ", ".join(mktps) if mktps else False
