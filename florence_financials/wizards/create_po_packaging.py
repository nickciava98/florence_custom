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
                bom_line_ids = bom_id.bom_line_ids.filtered(
                    lambda bom_line: bom_line.product_id.id in order_line_id.bom_item_ids.ids
                )
                for bom_line_id in bom_line_ids:
                    po_id = self.env["purchase.order"].create({
                        "partner_id": bom_line_id.vendor_id.id,
                        "partner_ref": f"{int(order_line_id.product_qty)} pz {bom_line_id.product_id.display_name}",
                        "parent_po_id": order_line_id.order_id.id,
                        "order_line": [(
                            0, 0, {
                                "product_id": bom_line_id.product_id.id,
                                "name": bom_line_id.product_id.display_name,
                                "product_qty": order_line_id.product_qty,
                                "product_uom": bom_line_id.product_id.uom_po_id.id,
                                "price_unit": bom_line_id.cost,
                                "taxes_id": [(6, 0, [self.env.ref("l10n_uk.PT0").id])],
                                "company_id": self.env.company.id
                            }
                        )]
                    })

                    po_ids.append(po_id.id)

        for order_line_id in self.order_line_ids:
            order_line_id.write({"bom_item_ids": False})

        if not po_ids:
            raise exceptions.UserError("No PO has been created!")

        action = self.env["ir.actions.act_window"]._for_xml_id("purchase.purchase_rfq")
        action["domain"] = [("id", "in", po_ids)]

        return action


class CreatePoPackagingItems(models.TransientModel):
    _name = "create.po.packaging.items"
    _description = "Create PO for Packaging - Items"

    order_line_id = fields.Many2one(
        "purchase.order.line",
        string="Order Line"
    )
    item_ids = fields.Many2many(
        "mrp.bom.line",
        "bom_line_create_po_packaging_items_rel",
        string="Items"
    )

    def confirm_action(self):
        if self.item_ids:
            self.order_line_id.write({
                "bom_item_ids": self.item_ids.product_id.ids
            })

        return {
            "name": "Create PO for Packaging",
            "type": "ir.actions.act_window",
            "res_model": "create.po.packaging",
            "view_mode": "form",
            "res_id": self.env.context.get("wizard_id"),
            "target": "new"
        }

    def cancel_action(self):
        return {
            "name": "Create PO for Packaging",
            "type": "ir.actions.act_window",
            "res_model": "create.po.packaging",
            "view_mode": "form",
            "res_id": self.env.context.get("wizard_id"),
            "target": "new"
        }
