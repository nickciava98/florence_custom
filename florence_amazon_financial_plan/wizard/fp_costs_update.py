from odoo import models
from odoo.exceptions import ValidationError
import calendar
import datetime


class FpCostsUpdate(models.TransientModel):
    _name = "florence.fp.costs.update"
    _description = "FP Costs Update"

    def update_action(self, auto = None):
        if int(datetime.datetime.now().month) == 1:
            year = str(datetime.datetime.now().year - 1)
            prev_month = "12"
        else:
            year = str(datetime.datetime.now().year)
            prev_month = str(int(datetime.datetime.now().month) - 1)

        last_day = str(calendar.monthrange(int(year), int(prev_month))[1])
        current_month = datetime.datetime.now().month
        updates = 0

        if len(self.env["florence.fp.costs"].search([])) > 0:
            for fp_cost in self.env["florence.fp.costs"].search([]):
                if datetime.datetime.strptime(year + "-" + prev_month + "-1", "%Y-%m-%d") \
                    <= datetime.datetime(fp_cost.date.year, fp_cost.date.month, fp_cost.date.day) \
                    <= datetime.datetime.strptime(year + "-" + prev_month + "-" + last_day, "%Y-%m-%d"):
                    fp_costs_lines = []

                    for fp_cost_line in fp_cost.fp_costs_lines:
                        domain = [
                            "&",
                            ("move_type", "=", "in_invoice"),
                            ("invoice_date", "<=", year + "-" + str(current_month) + "-" + str(calendar.monthrange(int(year), int(current_month))[1]))
                        ]
                        bill_id = 0

                        for bill in self.env["account.move"].search(domain, order = "name desc"):
                            for invoice_line in bill.invoice_line_ids:
                                if invoice_line.product_id.id == fp_cost_line.component.id:
                                    bill_id = bill.id
                                    break

                            if bill_id != 0:
                                break

                        fp_costs_lines.append({
                            "component": fp_cost_line.component.id,
                            "cost": fp_cost_line.cost,
                            "bill": bill_id
                        })

                    fp_cost_id = self.env["florence.fp.costs"].sudo().create({
                        "name": fp_cost.name.id,
                        "sku_id": fp_cost.sku_id.id,
                        "date": datetime.datetime.now(),
                        "pieces": 1
                    })

                    if len(fp_costs_lines) > 0:
                        for fp_cost_line in fp_costs_lines:
                            fp_cost_line["name"] = fp_cost_id.id

                            self.env["florence.fp.costs.line"].sudo().create(fp_cost_line)

                    updates += 1
        else:
            if auto is None:
                raise ValidationError("No records found to update FP Cost!")

        if updates == 0:
            if auto is None:
                raise ValidationError("No records found to update FP Cost!")

    def auto_update_action(self):
        self.update_action(auto = "auto")
