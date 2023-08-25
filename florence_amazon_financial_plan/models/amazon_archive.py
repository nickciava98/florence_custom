import datetime

from odoo import models, fields, api
from odoo.osv import expression


class AmazonArchive(models.Model):
    _name = "amazon.archive"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Amazon Archive"
    _rec_name = "amazon_order_id"

    amazon_order_id = fields.Char(
        string="Amazon Order Id"
    )
    merchant_order_id = fields.Char(
        string="Merchant Order ID"
    )
    shipment_id = fields.Char(
        string="Shipment ID"
    )
    shipment_item_id = fields.Char(
        string="Shipment Item ID"
    )
    amazon_order_item_id = fields.Char(
        string="Amazon Order Item ID"
    )
    merchant_order_item_id = fields.Char(
        string="Merchant Order Item ID"
    )
    purchase_date = fields.Char(
        string="Purchase Date Text"
    )
    purchase_datetime = fields.Datetime(
        compute="_compute_purchase_datetime",
        store=True,
        string="Purchase Date"
    )
    payments_date = fields.Char(
        string="Payments Date Text"
    )
    payments_datetime = fields.Datetime(
        compute="_compute_payments_datetime",
        store=True,
        string="Payments Date"
    )
    shipment_date = fields.Char(
        string="Shipment Date Text"
    )
    shipment_datetime = fields.Datetime(
        compute="_compute_shipment_datetime",
        store=True,
        string="Shipment Date"
    )
    reporting_date = fields.Char(
        string="Reporting Date Text"
    )
    reporting_datetime = fields.Datetime(
        compute="_compute_reporting_datetime",
        store=True,
        string="Reporting Date"
    )
    buyer_email = fields.Char(
        string="Buyer E-mail"
    )
    buyer_name = fields.Char(
        string="Buyer Name"
    )
    buyer_phone_number = fields.Char(
        string="Buyer Phone Number"
    )
    merchant_sku = fields.Char(
        string="Merchant SKU"
    )
    product_id = fields.Many2one(
        "product.product",
        compute="_compute_product_id",
        store=True,
        string="Product"
    )
    title = fields.Char(
        string="Title"
    )
    dispatched_quantity = fields.Integer(
        string="Dispatched Quantity"
    )
    currency = fields.Char(
        string="Currency Name"
    )
    currency_id = fields.Char(
        compute="_compute_currency_id",
        store=True,
        string="Currency"
    )
    item_price = fields.Float(
        string="Item Price"
    )
    item_tax = fields.Float(
        string="Item Tax"
    )
    delivery_price = fields.Float(
        string="Delivery Price"
    )
    delivery_tax = fields.Float(
        string="Delivery Tax"
    )
    gift_wrap_price = fields.Float(
        string="Gift Wrap Price"
    )
    gift_wrapping_tax = fields.Float(
        string="Gift Wrapping Tax"
    )
    delivery_service_level = fields.Char(
        string="Delivery Service Level"
    )
    recipient_name = fields.Char(
        string="Recipient Name"
    )
    delivery_address_one = fields.Char(
        string="Delivery Address 1"
    )
    delivery_address_two = fields.Char(
        string="Delivery Address 2"
    )
    delivery_address_three = fields.Char(
        string="Delivery Address 3"
    )
    delivery_city_town = fields.Char(
        string="Delivery City/Town"
    )
    delivery_county = fields.Char(
        string="Delivery County"
    )
    delivery_postcode = fields.Char(
        string="Delivery Postcode"
    )
    delivery_country_code = fields.Char(
        string="Delivery Country Code"
    )
    delivery_phone_number = fields.Char(
        string="Delivery Phone Number"
    )
    billing_address_one = fields.Char(
        string="Billing Address 1"
    )
    billing_address_two = fields.Char(
        string="Billing Address 2"
    )
    billing_address_three = fields.Char(
        string="Billing Address 3"
    )
    billing_city_town = fields.Char(
        string="Billing City/Town"
    )
    billing_county = fields.Char(
        string="Billing County"
    )
    bill_postal_code = fields.Char(
        string="bill-postal-code"
    )
    bill_country = fields.Char(
        string="bill-country"
    )
    item_promo_discount = fields.Float(
        string="Item Promo Discount"
    )
    shipment_promo_discount = fields.Float(
        string="Shipment Promo Discount"
    )
    carrier = fields.Char(
        string="Carrier"
    )
    tracking_number = fields.Char(
        string="Tracking Number"
    )
    estimated_arrival_date = fields.Char(
        string="Estimated Arrival Date Text"
    )
    estimated_arrival_datetime = fields.Datetime(
        compute="_compute_estimated_arrival_datetime",
        store=True,
        string="Estimated Arrival Date"
    )
    fc = fields.Char(
        string="FC"
    )
    fulfilment_channel = fields.Char(
        string="Fulfilment Channel"
    )
    sales_channel = fields.Char(
        string="Sales Channel"
    )

    @api.depends("purchase_date")
    def _compute_purchase_datetime(self):
        for line in self:
            line.purchase_datetime = datetime.datetime.strptime(
                line.purchase_date[:-6], "%Y-%m-%dT%H:%M:%S"
            ) if line.purchase_date else False

    @api.depends("payments_date")
    def _compute_payments_datetime(self):
        for line in self:
            line.payments_datetime = datetime.datetime.strptime(
                line.payments_date[:-6], "%Y-%m-%dT%H:%M:%S"
            ) if line.payments_date else False

    @api.depends("shipment_date")
    def _compute_shipment_datetime(self):
        for line in self:
            line.shipment_datetime = datetime.datetime.strptime(
                line.shipment_date[:-6], "%Y-%m-%dT%H:%M:%S"
            ) if line.shipment_date else False

    @api.depends("reporting_date")
    def _compute_reporting_datetime(self):
        for line in self:
            line.reporting_datetime = datetime.datetime.strptime(
                line.reporting_date[:-6], "%Y-%m-%dT%H:%M:%S"
            ) if line.reporting_date else False

    @api.depends("merchant_sku", "delivery_country_code")
    def _compute_product_id(self):
        for line in self:
            sku_ids = self.env["product.sku"].search([("name", "ilike", line.merchant_sku)], order="id asc")

            if sku_ids:
                line.product_id = sku_ids[0].product_id

                for sku_id in sku_ids[1:]:
                    if line.delivery_country_code and line.delivery_country_code in sku_id.product_id.display_name:
                        line.product_id = sku_id.product_id

    @api.depends("currency")
    def _compute_currency_id(self):
        for line in self:
            line.currency_id = self.env["res.currency"].search(
                [("name", "ilike", line.currency)], limit=1
            ) if line.currency else False

    @api.depends("estimated_arrival_date")
    def _compute_estimated_arrival_datetime(self):
        for line in self:
            line.estimated_arrival_datetime = datetime.datetime.strptime(
                line.estimated_arrival_date[:-6], "%Y-%m-%dT%H:%M:%S"
            ) if line.estimated_arrival_date else False


class AmazonArchiveOpen(models.TransientModel):
    _name = "amazon.archive.open"
    _description = "Amazon Archive Open"

    date_from = fields.Date(
        string="From"
    )
    date_to = fields.Date(
        string="To"
    )
    sales_channel = fields.Selection(
        [("Amazon.it", "Amazon IT"),
         ("Amazon.fr", "Amazon FR"),
         ("Amazon.de", "Amazon DE"),
         ("Amazon.es", "Amazon ES"),
         ("Amazon.co.uk", "Amazon UK"),
         ("Amazon.pl", "Amazon PL"),
         ("Amazon.se", "Amazon SE")],
        string="Sales Channel"
    )
    product_id = fields.Many2one(
        "product.product",
        domain="['&', '&', ('active', '=', True), ('sale_ok', '=', True), ('is_finished_product', '=', True)]",
        string="Product"
    )

    def confirm_action(self):
        domain = [
            "&", ("purchase_datetime", ">=", self.date_from.strftime("%Y-%m-%d") + " 00:00:00"),
            ("purchase_datetime", "<=", self.date_to.strftime("%Y-%m-%d") + " 23:59:59")
        ]

        if self.sales_channel:
            domain = expression.AND([domain, [("sales_channel", "=", self.sales_channel)]])

        if self.product_id:
            domain = expression.AND([domain, [("product_id", "=", self.product_id.id)]])

        return {
            "name": "Amazon Archive",
            "type": "ir.actions.act_window",
            "res_model": "amazon.archive",
            "view_mode": "tree,form",
            "view_type": "form",
            "view_id": False,
            "domain": domain,
            "context": {
                "group_by": ["sales_channel", "buyer_name", "purchase_date:day", "product_id"]
            },
            "target": "current"
        }
