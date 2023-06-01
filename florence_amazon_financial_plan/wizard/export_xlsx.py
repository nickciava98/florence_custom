from odoo import models, fields
import xlsxwriter
import base64
import locale


class ExportXlsxBalanceSheet(models.TransientModel):
    _name = "export.xlsx.balance.sheet"
    _description = "Export XLSX Balance Sheet"
    
    balance_sheet_id = fields.Many2one(
        "florence.balance.sheet"
    )
    xlsx_file_name = fields.Char(
        string = "XLSX Name"
    )
    xlsx_file = fields.Binary(
        string = "XLSX File"
    )
    
    def export_xlsx_action(self):
        file_name = "temp"
        workbook = xlsxwriter.Workbook(file_name, {"in_memory": True})
        header_format = workbook.add_format({
            "bold": True,
            "border": 1
        })
        header_format.set_bg_color("#F2F2F2")
        header_format.set_align("vcenter")
        header_format_right = workbook.add_format({
            "bold": True,
            "align": "right",
            "border": 1
        })
        header_format_right.set_bg_color("#F2F2F2")
        header_format_right.set_align("vcenter")
        header_format_center = workbook.add_format({
            "bold": True,
            "align": "center",
            "border": 1
        })
        header_format_center.set_bg_color("#F2F2F2")
        header_format_center.set_align("vcenter")
        currency_format = workbook.add_format({
            "num_format": "_-* #,##0.0000 €_-;-* #,##0.0000 €_-;_-* -?? €_-;_-@_-",
            "align": "right",
            "border": 1
        })
        currency_format.set_align("vcenter")
        qty_format = workbook.add_format({
            "num_format": "#,##0",
            "align": "right",
            "border": 1
        })
        qty_format.set_align("vcenter")
        text_format = workbook.add_format({
            "text_wrap": True,
            "align": "left",
            "border": 1
        })
        text_format.set_align("vcenter")
        text_center = workbook.add_format({
            "align": "center",
            "border": 1
        })
        text_center.set_align("vcenter")
        text_center_italic = workbook.add_format({
            "italic": True,
            "align": "center",
            "border": 1
        })
        text_center_italic.set_align("vcenter")

        # Summary
        summary = workbook.add_worksheet(name = "Summary")

        summary.write(0, 0, "Name", header_format)
        summary.write(1, 0, self.balance_sheet_id.name, text_format)

        summary.write(0, 1, "Products Cash", header_format_right)
        summary.write(1, 1, self.balance_sheet_id.products_cash, currency_format)

        summary.write(0, 2, "Inventory Value", header_format_right)
        summary.write(1, 2, self.balance_sheet_id.inventory_value, currency_format)

        summary.write(0, 3, "Amazon Products Cash", header_format_right)
        summary.write(1, 3, self.balance_sheet_id.amazon_products_cash, currency_format)

        summary.write(0, 4, "Other Value", header_format_right)
        summary.write(1, 4, self.balance_sheet_id.other_value, currency_format)

        summary.write(0, 5, "Total", header_format_right)
        summary.write(1, 5, self.balance_sheet_id.total, currency_format)

        summary.set_column(0, 5, 30)
        summary.set_column(1, 5, 30)

        # Amazon Values
        amazon_values = workbook.add_worksheet(name = "Amazon Values")

        amazon_values.write(0, 0, "Product", header_format)
        amazon_values.write(0, 1, "Amazon Marketplace", header_format_center)
        amazon_values.write(0, 2, "Quantity", header_format_right)
        amazon_values.write(0, 3, "Price Unit", header_format_right)
        amazon_values.write(0, 4, "Total", header_format_right)

        index = 1

        for value in self.balance_sheet_id.balance_sheet_lines:
            amazon_values.write(index, 0, value.product_id.display_name, text_format)
            amazon_values.write(index, 1, value.amazon_marketplace, text_center)
            amazon_values.write(index, 2, value.quantity, qty_format)
            amazon_values.write(index, 3, value.price_unit, currency_format)
            amazon_values.write(index, 4, value.price_unit * value.quantity, currency_format)

            index += 1

        amazon_values.set_column(0, 4, 30)

        # More Values
        more_values = workbook.add_worksheet(name = "More Values")

        more_values.write(0, 0, "Item", header_format)
        more_values.write(0, 1, "Value", header_format_right)

        index = 1

        for value in self.balance_sheet_id.balance_sheet_more_lines:
            more_values.write(index, 0, value.item, text_format)
            more_values.write(index, 1, value.value, currency_format)

            index += 1

        more_values.set_column(0, 1, 30)

        # Inventory Values
        inventory_values = workbook.add_worksheet(name = "Inventory Values")

        inventory_values.write(0, 0, "Product", header_format)
        inventory_values.write(0, 1, "Can Be Used", header_format_center)
        inventory_values.write(0, 2, "Can Be Sold", header_format_center)
        inventory_values.write(0, 3, "Location", header_format)
        inventory_values.write(0, 4, "Lot", header_format)
        inventory_values.write(0, 5, "Available Quantity", header_format_right)
        inventory_values.write(0, 6, "Value", header_format_right)

        locations = [
            inv_line.location_id.display_name for inv_line in self.balance_sheet_id.balance_sheet_inventory_lines
        ]
        locations = sorted(list(dict.fromkeys(locations)))
        locations_formats = {
            "BIONA/Stock": workbook.add_format({
                "italic": True,
                "align": "center",
                "border": 1
            }),
            "LFA I/Stock": workbook.add_format({
                "italic": True,
                "align": "center",
                "border": 1
            }),
            "LFA I/Stock-NonVendibile": workbook.add_format({
                "italic": True,
                "align": "center",
                "border": 1
            }),
            "OFFLI/Stock": workbook.add_format({
                "italic": True,
                "align": "center",
                "border": 1
            })
        }

        locations_formats["BIONA/Stock"].set_bg_color("#EBF1DE")
        locations_formats["LFA I/Stock"].set_bg_color("#DCE6F1")
        locations_formats["LFA I/Stock-NonVendibile"].set_bg_color("#FDE9D9")
        locations_formats["OFFLI/Stock"].set_bg_color("#E4DFEC")

        index = 1

        for location in locations:
            inv_lines = self.balance_sheet_id.balance_sheet_inventory_lines.filtered(
                lambda inv_line: inv_line.location_id and inv_line.location_id.display_name == location
            )
            location_value = str(locale.currency(
                sum([inv_line.value for inv_line in inv_lines]), grouping = True, symbol = False
            )) + " €"
            location_header = location + " [ " + location_value + " ]"

            inventory_values.merge_range(index, 0, index, 6, location_header, locations_formats[location])

            index += 1

            for value in inv_lines:
                can_be_used = "Yes" if value.can_be_used else "No"
                can_be_sold = "Yes" if value.sale_ok else "No"
                lot = value.lot_id.name if value.lot_id else ""

                inventory_values.write(index, 0, value.product_id.display_name, text_format)
                inventory_values.write(index, 1, can_be_used, text_center)
                inventory_values.write(index, 2, can_be_sold, text_center)
                inventory_values.write(index, 3, value.location_id.display_name, text_format)
                inventory_values.write(index, 4, lot, text_format)
                inventory_values.write(index, 5, value.available_quantity, qty_format)
                inventory_values.write(index, 6, value.value, currency_format)

                index += 1

        inventory_values.set_column(0, 6, 30)

        # External Inventories Values
        external_inventory_values = workbook.add_worksheet(name = "External Inventories Values")

        external_inventory_values.write(0, 0, "Product", header_format)
        external_inventory_values.write(0, 1, "Can Be Used", header_format_center)
        external_inventory_values.write(0, 2, "Can Be Sold", header_format_center)
        external_inventory_values.write(0, 3, "Location", header_format)
        external_inventory_values.write(0, 4, "Lot", header_format)
        external_inventory_values.write(0, 5, "Available Quantity", header_format_right)
        external_inventory_values.write(0, 6, "Value", header_format_right)

        locations = [
            inv_line.location_id.display_name for inv_line in self.balance_sheet_id.balance_sheet_inventory_more_lines
        ]
        locations = sorted(list(dict.fromkeys(locations)))
        index = 1

        for location in locations:
            inv_lines = self.balance_sheet_id.balance_sheet_inventory_more_lines.filtered(
                lambda inv_line: inv_line.location_id and inv_line.location_id.display_name == location
            )
            location_value = str(locale.currency(
                sum([inv_line.value for inv_line in inv_lines]), grouping = True, symbol = False
            )) + " €"
            location_header = location + " [ " + location_value + " ]"

            external_inventory_values.merge_range(index, 0, index, 6, location_header, text_center_italic)

            index += 1

            for value in inv_lines:
                can_be_used = "Yes" if value.can_be_used else "No"
                can_be_sold = "Yes" if value.sale_ok else "No"
                lot = value.lot_id.name if value.lot_id else ""

                external_inventory_values.write(index, 0, value.product_id.display_name, text_format)
                external_inventory_values.write(index, 1, can_be_used, text_center)
                external_inventory_values.write(index, 2, can_be_sold, text_center)
                external_inventory_values.write(index, 3, value.location_id.display_name, text_format)
                external_inventory_values.write(index, 4, lot, text_format)
                inventory_values.write(index, 5, value.available_quantity, qty_format)
                external_inventory_values.write(index, 6, value.value, currency_format)

                index += 1

        external_inventory_values.set_column(0, 6, 30)

        workbook.close()

        with open(file_name, "rb") as file:
            file_base64 = base64.b64encode(file.read())

        month = self.balance_sheet_id.date.strftime("%b").capitalize()
        year = self.balance_sheet_id.date.strftime("%y")
        name = "Balance Sheet - " + month + " " + year + ".xlsx"

        self.sudo().write({
            "xlsx_file_name": name,
            "xlsx_file": file_base64
        })

        export_form_id = self.env.ref("florence_amazon_financial_plan.export_xlsx_balance_sheet_post_view_form")

        return {
            "name": "Export XLSX Balance Sheet",
            "type": "ir.actions.act_window",
            "res_model": "export.xlsx.balance.sheet",
            "view_mode": "form",
            "view_type": "tree,form",
            "views": [(export_form_id.id, "form")],
            "context": {
                "default_balance_sheet_id": self.balance_sheet_id.id
            },
            "res_id": self.id,
            "target": "new"
        }
