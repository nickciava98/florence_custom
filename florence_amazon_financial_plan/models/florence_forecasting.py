import calendar
import datetime
import math

from odoo import models, fields, api


class FlorenceForecasting(models.Model):
    _name = "florence.forecasting"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Florence Forecasting"

    name = fields.Many2one(
        "product.product",
        string="Product"
    )
    date = fields.Date(
        default=datetime.datetime.now()
    )
    avg_qty_sold = fields.Float(
        digits=(11, 2)
    )
    threshold = fields.Float(
        default=2.0
    )
    est_value = fields.Float(
        digits=(11, 2),
        compute="_compute_est_value",
        store=True,
        string="Est. Value"
    )
    line_ids = fields.One2many(
        "florence.forecasting.line",
        "name",
        string="Components"
    )
    currency_id = fields.Many2one(
        "res.currency",
        default=lambda self: self.env.ref("base.main_company").currency_id
    )

    @api.depends("line_ids")
    def _compute_est_value(self):
        for line in self:
            line.est_value = sum([f_line.est_value for f_line in line.line_ids]) if line.line_ids else .0

    @api.onchange("avg_qty_sold")
    def _onchange_avg_qty_sold(self):
        for line in self:
            if line.line_ids:
                for f_line in line.line_ids:
                    f_line.avg_qty_sold = line.avg_qty_sold

    def update_values_action(self):
        if self.name:
            self.line_ids = [(5, 0, 0)]
            bom_id = self.env["mrp.bom"].search(
                [("product_id", "=", self.name.id)], limit=1
            )
            name_est_value = .0
            year = self.date.strftime("%Y")
            month = self.date.strftime("%m")
            last_day = str(calendar.monthrange(int(year), int(month))[1])

            purchase_ids = self.env["purchase.order"].search(
                [("date_order", "<=", "%s-%s-%s" % (year, month, last_day))],
                order="id desc"
            )

            if self.name and purchase_ids:
                for purchase_id in purchase_ids:
                    order_line = purchase_id.order_line.filtered(
                        lambda ol: ol.product_id.id == self.name.id
                    )

                    if order_line:
                        if purchase_id.invoice_ids:
                            for invoice_id in purchase_id.invoice_ids:
                                invoice_line = invoice_id.invoice_line_ids.filtered(
                                    lambda inv_line: inv_line.product_id.id == self.name.id
                                )

                                if invoice_line:
                                    name_est_value = invoice_line[0].price_unit
                                    break
                        else:
                            name_est_value = order_line[0].price_unit

                        break

                if math.isclose(name_est_value, .0):
                    bills = self.env["account.move"].search(
                        ["&", ("move_type", "=", "in_invoice"),
                         ("invoice_date", "<=", "%s-%s-%s" % (year, month, last_day))], order="id desc"
                    )

                    if bills:
                        for bill in bills:
                            invoice_line = bill.invoice_line_ids.filtered(
                                lambda inv_line: inv_line.product_id.id == self.name.id
                            )

                            if invoice_line:
                                name_est_value = invoice_line[0].price_unit
                                break

            name_est_value *= self.name.qty_available
            months_autonomy = self.name.qty_available / self.avg_qty_sold \
                if self.avg_qty_sold > 0 else .0
            self.line_ids = [(
                0, 0, {
                    "name": self.id,
                    "component": self.name.id,
                    "available_qty": self.name.qty_available,
                    "avg_qty_sold": self.avg_qty_sold,
                    "months_autonomy": months_autonomy,
                    "est_value": name_est_value
                    if months_autonomy < self.threshold else .0,
                    "currency_id": self.currency_id.id
                }
            )]

            if bom_id:
                for bom_line in bom_id.bom_line_ids:
                    est_value = bom_line.cost
                    est_value *= bom_line.product_id.qty_available
                    months_autonomy = bom_line.product_id.qty_available / self.avg_qty_sold \
                        if self.avg_qty_sold > 0 else .0
                    self.line_ids = [(
                        0, 0, {
                            "name": self.id,
                            "component": bom_line.product_id.id,
                            "available_qty": bom_line.product_id.qty_available,
                            "avg_qty_sold": self.avg_qty_sold,
                            "months_autonomy": months_autonomy,
                            "est_value": est_value if months_autonomy < self.threshold else 0.0,
                            "currency_id": self.currency_id.id
                        }
                    )]

        self._compute_est_value()

    def auto_update_action(self):
        year = str(datetime.datetime.now().year - 1) \
            if int(datetime.datetime.now().month) == 1 else str(datetime.datetime.now().year)
        prev_month = "12" \
            if int(datetime.datetime.now().month) == 1 else str(int(datetime.datetime.now().month) - 1) \
            if int(datetime.datetime.now().month) > 10 else "0" + str(int(datetime.datetime.now().month) - 1)
        curr_month = str(datetime.datetime.now().month) \
            if int(datetime.datetime.now().month) > 9 else "0" + str(datetime.datetime.now().month)
        prev_last_day = str(calendar.monthrange(int(year), int(prev_month))[1])
        curr_last_day = str(calendar.monthrange(int(year), int(curr_month))[1])
        domain = [
            "&", ("date", ">=", year + "-" + prev_month + "-1"),
            ("date", "<=", year + "-" + prev_month + "-" + prev_last_day)
        ]
        forecasts = self.env["florence.forecasting"].search(domain)
        domain_current = [
            "&", ("date", ">=", year + "-" + curr_month + "-1"),
            ("date", "<=", year + "-" + curr_month + "-" + curr_last_day)
        ]
        forecasts_current = self.env["florence.forecasting"].search(domain_current)

        if len(forecasts) > 0 and len(forecasts_current) == 0:
            for forecast in forecasts:
                forecast_id = self.env["florence.forecasting"].sudo().create({
                    "name": forecast.name.id,
                    "date": datetime.datetime.now().replace(day=1),
                    "avg_qty_sold": forecast.avg_qty_sold,
                    "threshold": forecast.threshold
                })
                forecast_id.update_values_action()


class FlorenceForecastingLine(models.Model):
    _name = "florence.forecasting.line"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Florence Forecasting Line"

    name = fields.Many2one(
        "florence.forecasting",
        ondelete="cascade"
    )
    component = fields.Many2one(
        "product.product"
    )
    available_qty = fields.Float(
        digits=(11, 2)
    )
    avg_qty_sold = fields.Float(
        digits=(11, 2)
    )
    months_autonomy = fields.Float(
        digits=(11, 2)
    )
    est_value = fields.Float(
        digits=(11, 2),
        string="Est. Value"
    )
    currency_id = fields.Many2one(
        "res.currency",
        related="name.currency_id",
        store=True
    )
