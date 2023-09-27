from odoo.exceptions import UserError

from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    related_invoice = fields.Char(
        compute="_compute_related_invoice"
    )
    parent_po_id = fields.Many2one(
        "purchase.order",
        ondelete="restrict",
        string="Parent PO"
    )
    packaging_po_ids = fields.One2many(
        "purchase.order",
        "parent_po_id",
        string="Packaging POs"
    )
    packaging_po_count = fields.Integer(
        compute="_compute_packaging_po_count"
    )

    @api.depends("packaging_po_ids")
    def _compute_packaging_po_count(self):
        for po in self:
            po.packaging_po_count = len(po.packaging_po_ids)

    def view_packaging_po_action(self):
        action = self.env["ir.actions.act_window"]._for_xml_id("purchase.purchase_rfq")

        if len(self.packaging_po_ids) == 1:
            action["res_id"] = self.packaging_po_ids[0].id
        else:
            action["domain"] = [("id", "in", self.packaging_po_ids.ids)]

        return action

    def create_po_packaging_action(self):
        order_line = self.order_line.filtered(lambda ol: ol.product_id.bom_ids).ids

        if not order_line:
            raise UserError("No Products found with associated Boms!")

        return {
            "name": "Create PO for Packaging",
            "type": "ir.actions.act_window",
            "res_model": "create.po.packaging",
            "view_mode": "form",
            "context": {
                "default_order_line_ids": order_line
            },
            "target": "new"
        }

    @api.depends("invoice_ids")
    def _compute_related_invoice(self):
        for line in self:
            invoice_numbers = [invoice.name for invoice in line.invoice_ids] if line.invoice_ids else False
            line.related_invoice = ", ".join(invoice_numbers) if invoice_numbers else False

    def open_link_bill_wizard_action(self):
        po_ids = [po.id for po in self]

        if len(po_ids) == 1:
            return {
                "name": "Link Bill",
                "type": "ir.actions.act_window",
                "res_model": "link.bill",
                "view_mode": "form",
                "view_type": "form",
                "context": {
                    "default_purchase_id": po_ids[0]
                },
                "views": [(False, "form")],
                "target": "new"
            }

        raise UserError(
            "You can only link bill to one Purchase Order!"
        )


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    bom_item_ids = fields.Many2many(
        "product.product",
        "product_product_purchase_order_line_rel",
        string="BoM Items"
    )

    def select_bom_items_action(self):
        bom_id = self.product_id.bom_ids[0] if self.product_id.bom_ids else False
        default_item_ids = self.bom_item_ids.ids \
            if self.bom_item_ids else bom_id.bom_line_ids.ids \
            if bom_id and bom_id.bom_line_ids else False

        return {
            "name": "Select BoM Items",
            "type": "ir.actions.act_window",
            "res_model": "create.po.packaging.items",
            "view_mode": "form",
            "context": {
                "default_order_line_id": self.id,
                "default_item_ids": default_item_ids
            },
            "target": "new"
        }
