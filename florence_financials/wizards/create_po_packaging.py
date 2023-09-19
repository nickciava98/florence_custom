from odoo import models, fields, exceptions


class CreatePoPackaging(models.TransientModel):
    _name = "create.po.packaging"
    _description = "Create PO for Packaging"

    order_line_ids = fields.Many2many(
        "purchase.order.line",
        "purchase_order_line_create_po_packaging_rel",
        string="Order Line"
    )

    def confirm_action(self):
        if not self.order_line_ids:
            raise exceptions.UserError("No Products found to create PO!")

        po_ids = []

        for order_line_id in self.order_line_ids:
            for bom_id in order_line_id.product_id.bom_ids.filtered(lambda bom: bom.bom_line_ids):
                for bom_line_id in bom_id.bom_line_ids.filtered(lambda bom_line: bom_line.bill):
                    po_id = self.env["purchase.order"].create({
                        "partner_id": bom_line_id.bill.partner_id.id,
                        "partner_ref": f"{order_line_id.product_qty} pz {bom_line_id.product_id.display_name}",
                        "parent_po_id": order_line_id.order_id.id,
                        "order_line": [(
                            0, 0, {
                                "product_id": bom_line_id.product_id.id,
                                "name": bom_line_id.product_id.display_name,
                                "product_uom_qty": order_line_id.product_qty,
                                "product_uom": bom_line_id.product_id.uom_po_id.id,
                                "price_unit": bom_line_id.bill.invoice_line_ids.filtered(
                                    lambda inv_line_id: inv_line_id.product_id.id == bom_line_id.product_id.id
                                )[0].price_unit,
                                "taxes_id": [(6, 0, [self.env.ref("l10n_uk.PT0").id])],
                                "company_id": self.env.company.id
                            }
                        )]
                    })

                    po_ids.append(po_id.id)

        action = self.env["ir.actions.act_window"]._for_xml_id("purchase.purchase_rfq")

        if len(po_ids) == 1:
            action["res_id"] = po_ids[0]
        elif len(po_ids) > 1:
            action["domain"] = [("id", "in", po_ids)]
        else:
            raise exceptions.UserError("No PO has been created!")

        return action
