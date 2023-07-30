import calendar
import datetime

from odoo import models


class SaleReport(models.Model):
    _inherit = "sale.report"

    def view_amazon_report_action(self):
        current_year = datetime.datetime.now().year
        current_month = datetime.datetime.now().month
        last_day = str(calendar.monthrange(int(current_year), int(current_month))[1])

        return {
            "name": "Sales Analysis",
            "res_model": "sale.report",
            "view_type": "dashboard",
            "view_mode": "dashboard",
            "type": "ir.actions.act_window",
            "context": {
                "graph": {
                    "graph_measure": "price_subtotal",
                    "graph_mode": "line",
                    "graph_groupbys": ["date:day"]
                },
                "pivot": {
                    "pivot_measures": [
                        "__count",
                        "order_id",
                        "price_subtotal",
                        "price_total"
                    ],
                    "pivot_column_groupby": [],
                    "pivot_row_groupby": [
                        "categ_id",
                        "product_tmpl_id"
                    ]
                },
                "group_by": []
            },
            "domain": [
                "&", "&",
                ("date", ">=", str(current_year) + "-" + str(current_month) + "-1 00:00:01"),
                ("date", "<=", str(current_year) + "-" + str(current_month) + "-" + str(last_day) + " 23:59:59"),
                ("team_id", "ilike", "Amazon")
            ]
        }
