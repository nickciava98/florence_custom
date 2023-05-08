from odoo import models, fields, api
import calendar
import math


class FlorenceFpCostsLine(models.Model):
    _name = "florence.fp.costs.line"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Florence FP Costs Line"

    name = fields.Many2one(
        "florence.fp.costs",
        ondelete = "cascade"
    )
    component = fields.Many2one(
        "product.product"
    )
    cost = fields.Float(
        digits = (12, 4)
    )
    vendor = fields.Many2one(
        "res.partner",
        related = "bill.partner_id",
        store = True
    )
    bill = fields.Many2one(
        "account.move"
    )
    bill_date = fields.Date(
        related = "bill.invoice_date",
        store = True
    )
    currency_id = fields.Many2one(
        "res.currency",
        compute = "_compute_currency_id"
    )
    to_refill = fields.Boolean(
        compute = "_compute_to_refill",
        store = True
    )

    @api.depends("component", "bill")
    def _compute_to_refill(self):
        for line in self:
            line.to_refill = False

            if line.component:
                configuration_id = self.env["forecast.configuration"].search([], limit = 1)
                stock_quant_product_id = self.env["stock.quant"].search(
                    ["&", ("product_id", "=", line.component.id), ("location_id.is_valuable_stock", "=", True)],
                    limit = 1
                )
                line.cost = 0.0

                if line.bill:
                    if len(line.bill.invoice_line_ids) > 0:
                        for invoice_line in line.bill.invoice_line_ids:
                            if invoice_line.product_id.id == line.component.id:
                                line.cost = invoice_line.price_unit
                                break

                line.to_refill = True \
                    if stock_quant_product_id.to_be_computed \
                       and stock_quant_product_id.months_autonomy < configuration_id.months_treshold \
                    else False

                if line.to_refill:
                    line.cost = 0.0

                    if line.bill:
                        if len(line.bill.invoice_line_ids) > 0:
                            for invoice_line in line.bill.invoice_line_ids:
                                if invoice_line.product_id.id == line.component.id:
                                    line.cost = invoice_line.price_unit
                                    break

                    if configuration_id:
                        line.message_post(
                            body_message = "Please Refill " + line.component.name,
                            partner_ids = configuration_id.partner_ids.ids
                        )
                    else:
                        line.message_post(
                            body_message = "Please Refill " + line.component.name
                        )

            line.name._compute_price()
            line.name._compute_total()

    def _recompute_to_refill_action(self):
        self._compute_to_refill()

    # @api.depends("component")
    # def _compute_bill(self):
    #     for line in self:
    #         line.bill = False
    #
    #         if line.component:
    #             year = line.name.date.strftime("%Y")
    #             month = line.name.date.strftime("%m")
    #
    #             for bill in self.env["account.move"].search(
    #                 ["&", "&",
    #                  ("move_type", "=", "in_invoice"),
    #                  ("invoice_date", ">=", year + "-" + month + "-1"),
    #                  ("invoice_date", "<=", year + "-" +  month + "-" + str(calendar.monthrange(int(year), int(month))[1]))],
    #                 order = "name desc"):
    #                 for invoice_line in bill.invoice_line_ids:
    #                     if invoice_line.product_id == line.component:
    #                         line.bill = bill
    #                         break
    #
    #                 if line.bill:
    #                     break
    #
    # @api.depends("component", "bill")
    # def _compute_cost(self):
    #     for line in self:
    #         line.cost = 0
    #
    #         if line.component:
    #             year = line.name.date.strftime("%Y")
    #             month = line.name.date.strftime("%m")
    #
    #             for bill in self.env["account.move"].search(
    #                 ["&", "&",
    #                  ("move_type", "=", "in_invoice"),
    #                  ("invoice_date", ">=", year + "-" + month + "-1"),
    #                  ("invoice_date", "<=", year + "-" + month + "-" + str(calendar.monthrange(int(year), int(month))[1]))],
    #                 order = "name desc"):
    #                 for invoice_line in bill.invoice_line_ids:
    #                     if invoice_line.product_id == line.component:
    #                         line.cost = invoice_line.price_unit
    #                         break
    #
    #                 if line.cost > 0:
    #                     break

    def _compute_currency_id(self):
        for line in self:
            line.currency_id = self.env.ref("base.main_company").currency_id
