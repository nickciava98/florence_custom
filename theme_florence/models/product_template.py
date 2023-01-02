# -*- coding: utf-8 -*-

from odoo import models, fields
import datetime


class ProductTemplate(models.Model):
    _inherit = "product.template"

    theme_notes = fields.Html('Short Notes')

    timer_set = fields.Datetime('Timer Date time')
    timer_text_msg = fields.Text()
    show_product_in_nav = fields.Boolean()
    payment_image = fields.Binary(string='Payment Image')


    def get_duration(self):
        duration = (self.timer_set - datetime.datetime.now()).total_seconds()
        print(">>>>>>>duration",duration)
        if duration >= 0:
            return round(duration, 0)


class Website(models.Model):
    _inherit = "website"

    def get_header_product(self):
        product_ids = self.env['product.template'].sudo().search([('show_product_in_nav', '=', True)])
        return product_ids
    live_chat = fields.Text('Live Chat')