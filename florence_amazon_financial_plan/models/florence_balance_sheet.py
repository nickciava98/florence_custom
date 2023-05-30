from odoo import models, fields, api
import datetime
import xlsxwriter
import base64


class FlorenceBalanceSheet(models.Model):
    _name = "florence.balance.sheet"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Florence Balance Sheet"

    def _default_products_cash(self):
        products_cash = .0

        for fp in self.env["amazon.financial.plan"].search([]):
            products_cash += fp.total_to_use

        return products_cash

    def _default_balance_sheet_inventory_lines(self):
        balance_sheet_inventory_lines = [(5, 0, 0)]

        for item in self.env["stock.quant"].search([("location_id.is_valuable_stock", "=", True)]):
            balance_sheet_inventory_lines.append((
                0, 0, {
                    "product_id": item.product_id,
                    "location_id": item.location_id,
                    "lot_id": item.lot_id,
                    "available_quantity": item.available_quantity,
                    "value": item.value,
                    "sale_ok": item.sale_ok,
                    "can_be_used": item.can_be_used
                }
            ))

        return balance_sheet_inventory_lines

    name = fields.Char(
        copy = False
    )
    date = fields.Date(
        default = datetime.datetime.now()
    )
    products_cash = fields.Float(
        default = _default_products_cash,
        readonly = True,
        copy = False,
        string = "Products Cash (i)"
    )
    inventory_value = fields.Float(
        compute = "_compute_inventory_value",
        store = True,
        string = "Inventory Value (ii)"
    )
    amazon_products_cash = fields.Float(
        compute = "_compute_amazon_products_cash",
        string = "Amazon Products Cash (iii)"
    )
    other_value = fields.Float(
        compute = "_compute_other_value",
        string = "Other Values (iv)"
    )
    balance_sheet_lines = fields.One2many(
        "florence.balance.sheet.line",
        "name",
        copy = True
    )
    notebook_invisible = fields.Boolean(
        default = False
    )
    balance_sheet_more_lines = fields.One2many(
        "florence.balance.sheet.more",
        "name",
        copy = True
    )
    balance_sheet_inventory_lines = fields.One2many(
        "florence.balance.sheet.inventory",
        "name",
        default = _default_balance_sheet_inventory_lines
    )
    balance_sheet_inventory_more_lines = fields.One2many(
        "florence.balance.sheet.inventory.more",
        "name",
        copy = True
    )
    currency_id = fields.Many2one(
        "res.currency",
        default = lambda self: self.env.ref("base.main_company").currency_id
    )
    total = fields.Float(
        compute = "_compute_total"
    )
    xlsx_file_name = fields.Char(
        string = "XLSX Name"
    )
    xlsx_file = fields.Binary(
        string = "XLSX File"
    )

    @api.depends("balance_sheet_inventory_lines", "balance_sheet_inventory_more_lines")
    def _compute_inventory_value(self):
        for line in self:
            line.inventory_value = .0

            if len(line.balance_sheet_inventory_lines) > 0:
                for bs_inv_line in line.balance_sheet_inventory_lines:
                    line.inventory_value += bs_inv_line.value

            if len(line.balance_sheet_inventory_more_lines) > 0:
                for bs_inv_line in line.balance_sheet_inventory_more_lines:
                    line.inventory_value += bs_inv_line.value

    @api.depends("products_cash", "inventory_value",
                 "amazon_products_cash", "other_value")
    def _compute_total(self):
        for line in self:
            line.total = sum([line.products_cash, line.inventory_value, line.amazon_products_cash, line.other_value])

    @api.depends("balance_sheet_more_lines")
    def _compute_other_value(self):
        for line in self:
            line.other_value = .0

            if len(line.balance_sheet_more_lines) > 0:
                for balance_sheet_more_line in line.balance_sheet_more_lines:
                    line.other_value += balance_sheet_more_line.value

    @api.depends("balance_sheet_lines")
    def _compute_amazon_products_cash(self):
        for line in self:
            line.amazon_products_cash = .0

            if len(line.balance_sheet_lines) > 0:
                for balance_sheet_line in line.balance_sheet_lines:
                    line.amazon_products_cash += balance_sheet_line.price_unit * balance_sheet_line.quantity

    def show_hide_notebook_action(self):
        self.notebook_invisible = not self.notebook_invisible

    def export_xlsx_action(self):
        file_name = "temp"
        workbook = xlsxwriter.Workbook(file_name, {"in_memory": True})
        header_format = workbook.add_format({
            "bold": True
        })
        header_format.set_align("vcenter")
        header_format_right = workbook.add_format({
            "bold": True,
            "align": "right"
        })
        header_format_right.set_align("vcenter")
        header_format_center = workbook.add_format({
            "bold": True,
            "align": "center"
        })
        header_format_center.set_align("vcenter")
        currency_format = workbook.add_format({
            "num_format": "_-* #,##0.0000 €_-;-* #,##0.0000 €_-;_-* -?? €_-;_-@_-",
            "align": "right"
        })
        currency_format.set_align("vcenter")
        qty_format = workbook.add_format({
            "num_format": "#,##0",
            "align": "right"
        })
        qty_format.set_align("vcenter")
        text_format = workbook.add_format({
            "text_wrap": True,
            "align": "left"
        })
        text_format.set_align("vcenter")
        text_center = workbook.add_format({
            "align": "center"
        })
        text_center.set_align("vcenter")

        # Summary
        summary = workbook.add_worksheet(name = "Summary")

        summary.write(0, 0, "Name", header_format)
        summary.write(1, 0, self.name, text_format)

        summary.write(0, 1, "Products Cash", header_format_right)
        summary.write(1, 1, self.products_cash, currency_format)

        summary.write(0, 2, "Inventory Value", header_format_right)
        summary.write(1, 2, self.inventory_value, currency_format)

        summary.write(0, 3, "Amazon Products Cash", header_format_right)
        summary.write(1, 3, self.amazon_products_cash, currency_format)

        summary.write(0, 4, "Other Value", header_format_right)
        summary.write(1, 4, self.other_value, currency_format)

        summary.write(0, 5, "Total", header_format_right)
        summary.write(1, 5, self.total, currency_format)

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

        for value in self.balance_sheet_lines:
            amazon_values.write(index, 0, value.product_id.name, text_format)
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

        for value in self.balance_sheet_more_lines:
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

        index = 1

        for value in self.balance_sheet_inventory_lines:
            can_be_used = "Yes" if value.can_be_used else "No"
            can_be_sold = "Yes" if value.sale_ok else "No"
            lot = value.lot_id.name if value.lot_id else ""

            inventory_values.write(index, 0, value.product_id.name, text_format)
            inventory_values.write(index, 1, can_be_used, text_center)
            inventory_values.write(index, 2, can_be_sold, text_center)
            inventory_values.write(index, 3, value.location_id.display_name)
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

        index = 1

        for value in self.balance_sheet_inventory_more_lines:
            can_be_used = "Yes" if value.can_be_used else "No"
            can_be_sold = "Yes" if value.sale_ok else "No"
            lot = value.lot_id.name if value.lot_id else ""

            external_inventory_values.write(index, 0, value.product_id.name, text_format)
            external_inventory_values.write(index, 1, can_be_used, text_center)
            external_inventory_values.write(index, 2, can_be_sold, text_center)
            external_inventory_values.write(index, 3, value.location_id.display_name)
            external_inventory_values.write(index, 4, lot, text_format)
            inventory_values.write(index, 5, value.available_quantity, qty_format)
            external_inventory_values.write(index, 6, value.value, currency_format)

            index += 1

        external_inventory_values.set_column(0, 6, 30)

        workbook.close()

        with open(file_name, "rb") as file:
            file_base64 = base64.b64encode(file.read())

        name = "Balance Sheet - " + self.date.strftime("%b").capitalize() + " " + self.date.strftime("%y") + ".xlsx"

        self.sudo().write({
            "xlsx_file_name": name,
            "xlsx_file": file_base64
        })

    _sql_constraint = [
        ("unique_name", "unique(name)", "Name must be unique!")
    ]
