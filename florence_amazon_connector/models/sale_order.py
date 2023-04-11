from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    amazon_mktp_ids = fields.Many2many(
        "amazon.marketplace",
        "amz_mktp_sale_order_rel",
        compute = "_compute_amazon_marketplaces",
        store = True,
        string = "Amazon Marketplaces"
    )
    amazon_locations = fields.Char(
        compute = "_compute_amazon_marketplaces",
        store = True,
        string = "Amazon Locations"
    )

    @api.depends("warehouse_id")
    def _compute_amazon_marketplaces(self):
        for line in self:
            line.amazon_mktp_ids = False
            line.amazon_locations = "Standard Order"

            if line.warehouse_id:
                if line.warehouse_id.lot_stock_id:
                    if len(line.warehouse_id.lot_stock_id.amazon_mktp_ids) > 0:
                        mktp_ids = []
                        mktps = []

                        for mktp in line.warehouse_id.lot_stock_id.amazon_mktp_ids:
                            mktp_ids.append(mktp.id)
                            mktps.append(mktp.domain)

                        if len(mktp_ids) > 0 and len(mktps) > 0:
                            line.amazon_mktp_ids = [(6, 0, mktp_ids)]
                            line.amazon_locations = ", ".join(mktps)
