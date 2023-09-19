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
