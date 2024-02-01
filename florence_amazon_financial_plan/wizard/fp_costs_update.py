import calendar
import datetime
import math

from odoo.exceptions import ValidationError

from odoo import models


class FpCostsUpdate(models.TransientModel):
    _name = "florence.fp.costs.update"
    _description = "FP Costs Update"

    def update_action(self, **kwargs):
        now = datetime.datetime.now()
        auto = kwargs.get("auto", None)
        current_month = kwargs.get("current_month", now.month)
        prev_month = kwargs.get("prev_mont", now.month - 1)
        year = now.year

        if current_month == 1:
            year = now.year - 1
            prev_month = 12

        last_day = calendar.monthrange(year, prev_month)[1]
        last_curr_day = calendar.monthrange(year, current_month)[1]
        updates = 0
        florence_fp_costs_ids = self.env["florence.fp.costs"].search(
            [("date", ">=", f"{year}-{prev_month}-01"),
             ("date", "<=", f"{year}-{prev_month}-{last_day}")]
        )
        florence_fp_costs_curr_month_ids = self.env["florence.fp.costs"].search(
            [("date", ">=", f"{year}-{current_month}-01"),
             ("date", "<=", f"{year}-{current_month}-{last_curr_day}")]
        )

        if florence_fp_costs_ids and not florence_fp_costs_curr_month_ids:
            for fp_cost in florence_fp_costs_ids:
                fp_costs_lines = []

                for fp_cost_line in fp_cost.fp_costs_lines:
                    invoice_last_date = f"{year}-{current_month}-{last_curr_day}"
                    domain = [("move_type", "=", "in_invoice"), ("invoice_date", "<=", invoice_last_date)]
                    bill_id = 0
                    cost = .0

                    for bill in self.env["account.move"].search(domain, order="id desc"):
                        invoice_line_id = bill.invoice_line_ids.filtered(
                            lambda l: l.product_id.id == fp_cost_line.component.id
                        )

                        if not invoice_line_id:
                            continue

                        bill_id = bill.id
                        cost = invoice_line_id[0].price_unit

                    fp_costs_lines.append({
                        "component": fp_cost_line.component.id,
                        "cost": cost,
                        "bill": bill_id
                    })

                fp_cost_id = self.env["florence.fp.costs"].sudo().create({
                    "name": fp_cost.name.id,
                    "sku_id": fp_cost.sku_id.id,
                    "date": datetime.datetime.now(),
                    "pieces": 1
                })

                if fp_costs_lines:
                    for fp_cost_line in fp_costs_lines:
                        fp_cost_line["name"] = fp_cost_id.id

                        self.env["florence.fp.costs.line"].sudo().create(fp_cost_line)

                updates += 1

        elif auto is None:
            raise ValidationError("No records found to update FP Cost!")

        if updates == 0 and auto is None:
            raise ValidationError("No records found to update FP Cost!")

    def auto_update_action(self):
        self.update_action(auto="auto")
