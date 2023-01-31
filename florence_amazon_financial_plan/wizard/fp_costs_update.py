from odoo import models
from odoo.exceptions import ValidationError
import calendar
import datetime


class FpCostsUpdate(models.TransientModel):
    _name = "florence.fp.costs.update"
    _description = "FP Costs Update"

    def update_action(self):
        year = str(datetime.datetime.now().year)

        if int(datetime.datetime.now().month) == 1:
            prev_month = "12"
        else:
            prev_month = str(int(datetime.datetime.now().month) - 1)

        last_day = str(calendar.monthrange(int(year), int(prev_month))[1])
        updates = 0

        if len(self.env["florence.fp.costs"].search([])) > 0:
            for fp_cost in self.env["florence.fp.costs"].search([]):
                print(year + "-" + prev_month + "-1")
                print("<=")
                print(str(fp_cost.date.year) + "-" + str(fp_cost.date.month + fp_cost.date.day))
                if datetime.datetime.strptime(year + "-" + prev_month + "-1", "%Y-%m-%d") \
                    <= datetime.datetime(fp_cost.date.year, fp_cost.date.month, fp_cost.date.day) \
                    <= datetime.datetime.strptime(year + "-" + prev_month + "-" + last_day, "%Y-%m-%d"):
                    fp_costs_lines = []

                    for fp_cost_line in fp_cost.fp_costs_lines:
                        fp_costs_lines.append((0, 0, {
                            "name": fp_cost.id,
                            "component": fp_cost_line.component.id,
                            "cost": fp_cost_line.cost
                        }))

                    self.env["florence.fp.costs"].sudo().create({
                        "name": fp_cost.name.id,
                        "sku_id": fp_cost.sku_id.id,
                        "date": datetime.datetime.now(),
                        "pieces": 1,
                        "fp_costs_lines": fp_costs_lines if len(fp_costs_lines) > 0 else [(5, 0, 0)]
                    })

                    updates += 1
        else:
            raise ValidationError("No records found to update FP Cost!")

        if updates == 0:
            raise ValidationError("No records found to update FP Cost!")
