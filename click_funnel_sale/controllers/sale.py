from odoo import api, http, _
from odoo.http import request, Response

import json
import logging
import pprint


_logger = logging.getLogger(__name__)

# We are expecting to receive a payload like below as documented on the clickfunnel payload below:
# 96109587
# {'event': 'created',
# 'purchase': {'charge_id': 'pi_3KPltRAJMLcS71G72aR7r4lJ',
#              'contact': {'accepted_terms': 'false',
#                          'additional_info': {'accepted_terms': 'false',
#                                              'cf_affiliate_id': '',
#                                              'cf_uvid': 'null',
#                                              'purchase': {'order_saas_url': '',
#                                                           'payment_method_nonce': '',
#                                                           'product_id': '3952402',
#                                                           'product_ids': ['3952395',
#                                                                           '3952397',
#                                                                           '3952402'],
#                                                           'stripe_customer_token': 'pm_1KPltNAJMLcS71G7AyPBYtYU'},
#                                              'time_zone': 'Rome',
#                                              'utm_campaign': '',
#                                              'utm_content': '',
#                                              'utm_medium': '',
#                                              'utm_source': '',
#                                              'utm_term': '',
#                                              'webinar_delay': '-63811280565953'},
#                          'address': 'Via Giovanni XXIII',
#                          'aff_sub': '',
#                          'aff_sub2': '',
#                          'affiliate_id': None,
#                          'cart_affiliate_id': '',
#                          'cf_affiliate_id': None,
#                          'cf_uvid': 'null',
#                          'city': 'Oristano',
#                          'contact_profile': {'action_score': None,
#                                              'address': 'Via Giovanni XXIII',
#                                              'age': None,
#                                              'age_range_lower': None,
#                                              'age_range_upper': None,
#                                              'cf_uvid': '9a3fa29b3b2818a5d508e1f3b9e9587a',
#                                              'city': 'Oristano',
#                                              'country': 'US',
#                                              'created_at': '2022-02-05T09:49:51.000Z',
#                                              'deduced_location': None,
#                                              'email': 'roby.fichera@gmail.com',
#                                              'first_name': 'AAAA',
#                                              'gender': None,
#                                              'id': 885393042,
#                                              'known_ltv': '323.74',
#                                              'last_name': 'FFFF',
#                                              'location_general': None,
#                                              'middle_name': None,
#                                              'normalized_location': None,
#                                              'phone': '3285320709',
#                                              'shipping_address': 'Via '
#                                                                  'Giovanni '
#                                                                  'XXIII',
#                                              'shipping_city': 'Oristano',
#                                              'shipping_country': 'US',
#                                              'shipping_state': 'OR',
#                                              'shipping_zip': '09096',
#                                              'state': 'OR',
#                                              'tags': [],
#                                              'time_zone': 'Rome',
#                                              'unsubscribed_at': None,
#                                              'updated_at': '2022-02-05T10:50:02.000Z',
#                                              'vat_number': None,
#                                              'websites': None,
#                                              'zip': '09096'},
#                          'country': 'US',
#                          'created_at': '2022-02-05T10:53:23.000Z',
#                          'email': 'roby.fichera@gmail.com',
#                          'first_name': 'AAAA',
#                          'funnel_id': 9479339,
#                          'funnel_step_id': 75565704,
#                          'id': 1975269500,
#                          'ip': '91.81.75.194',
#                          'last_name': 'FFFF',
#                          'name': 'AAAA FFFF',
#                          'page_id': 52635212,
#                          'phone': '3285320709',
#                          'shipping_address': 'Via Giovanni XXIII',
#                          'shipping_city': 'Oristano',
#                          'shipping_country': 'US',
#                          'shipping_state': 'OR',
#                          'shipping_zip': '09096',
#                          'state': 'OR',
#                          'time_zone': 'Rome',
#                          'unsubscribed_at': None,
#                          'updated_at': '2022-02-05T10:53:23.000Z',
#                          'vat_number': '',
#                          'webinar_at': None,
#                          'webinar_ext': 'NJNWiVBI',
#                          'webinar_last_time': None,
#                          'zip': '09096'},
#              'created_at': '2022-02-05T10:53:23.000Z',
#              'ctransreceipt': None,
#              'error_message': None,
#              'fulfillment_id': None,
#              'fulfillment_status': None,
#              'fulfillments': {},
#              'funnel_id': 9479339,
#              'id': 96101889,
#              'infusionsoft_ccid': None,
#              'manual': False,
#              'member_id': None,
#              'nmi_customer_vault_id': None,
#              'oap_customer_id': None,
#              'original_amount': {'cents': 7594, 'currency_iso': 'EUR'},
#              'original_amount_cents': 7594,
#              'original_amount_currency': 'EUR',
#              'payment_instrument_type': None,
#              'payments_count': None,
#              'products': [{'amount': {'cents': 1399, 'currency_iso': 'EUR'},
#                            'amount_currency': 'EUR',
#                            'billing_integration': 'stripe_account-176527',
#                            'bump': False,
#                            'cart_product_id': None,
#                            'commissionable': True,
#                            'created_at': '2022-01-12T17:23:50.000Z',
#                            'description': '',
#                            'html_body': '<!DOCTYPE html PUBLIC "-//W3C//DTD '
#                                         'HTML 4.0 Transitional//EN" '
#                                         '"http://www.w3.org/TR/REC-html40/loose.dtd">\r\n'
#                                         '\r\n',
#                            'id': 3952395,
#                            'infusionsoft_product_id': None,
#                            'infusionsoft_subscription_id': None,
#                            'name': '1 Siero Con Vitamina C Florence + 3 '
#                                    'bonus: 13,99€',
#                            'netsuite_class': None,
#                            'netsuite_id': None,
#                            'netsuite_tag': None,
#                            'ontraport_gateway_id': None,
#                            'ontraport_invoice_id': None,
#                            'ontraport_payment_count': None,
#                            'ontraport_payment_type': None,
#                            'ontraport_product_id': None,
#                            'ontraport_unit': None,
#                            'statement_descriptor': '',
#                            'stripe_cancel_after_payments': None,
#                            'stripe_plan': None,
#                            'subject': '',
#                            'thank_you_page_id': 72089394,
#                            'updated_at': '2022-01-25T11:08:10.000Z'},
#                           {'amount': {'cents': 2598, 'currency_iso': 'EUR'},
#                            'amount_currency': 'EUR',
#                            'billing_integration': 'stripe_account-176527',
#                            'bump': True,
#                            'cart_product_id': None,
#                            'commissionable': True,
#                            'created_at': '2022-01-12T17:26:15.000Z',
#                            'description': '',
#                            'html_body': '<!DOCTYPE html PUBLIC "-//W3C//DTD '
#                                         'HTML 4.0 Transitional//EN" '
#                                         '"http://www.w3.org/TR/REC-html40/loose.dtd">\r\n'
#                                         '\r\n',
#                            'id': 3952397,
#                            'infusionsoft_product_id': None,
#                            'infusionsoft_subscription_id': None,
#                            'name': 'Offerta Speciale: 2 Sieri  Extra a 12,99€ '
#                                    "l'uno",
#                            'netsuite_class': None,
#                            'netsuite_id': None,
#                            'netsuite_tag': None,
#                            'ontraport_gateway_id': None,
#                            'ontraport_invoice_id': None,
#                            'ontraport_payment_count': None,
#                            'ontraport_payment_type': None,
#                            'ontraport_product_id': None,
#                            'ontraport_unit': None,
#                            'statement_descriptor': '',
#                            'stripe_cancel_after_payments': None,
#                            'stripe_plan': None,
#                            'subject': '',
#                            'thank_you_page_id': 72089394,
#                            'updated_at': '2022-01-25T11:08:27.000Z'},
#                           {'amount': {'cents': 3597, 'currency_iso': 'EUR'},
#                            'amount_currency': 'EUR',
#                            'billing_integration': 'stripe_account-176527',
#                            'bump': True,
#                            'cart_product_id': None,
#                            'commissionable': True,
#                            'created_at': '2022-01-12T17:27:08.000Z',
#                            'description': '',
#                            'html_body': '<!DOCTYPE html PUBLIC "-//W3C//DTD '
#                                         'HTML 4.0 Transitional//EN" '
#                                         '"http://www.w3.org/TR/REC-html40/loose.dtd">\r\n'
#                                         '\r\n',
#                            'id': 3952402,
#                            'infusionsoft_product_id': None,
#                            'infusionsoft_subscription_id': None,
#                            'name': 'Offerta Speciale: 3 Sieri Vitamina C '
#                                    "Extra a 11,99 € l'uno",
#                            'netsuite_class': None,
#                            'netsuite_id': None,
#                            'netsuite_tag': None,
#                            'ontraport_gateway_id': None,
#                            'ontraport_invoice_id': None,
#                            'ontraport_payment_count': None,
#                            'ontraport_payment_type': None,
#                            'ontraport_product_id': None,
#                            'ontraport_unit': None,
#                            'statement_descriptor': '',
#                            'stripe_cancel_after_payments': None,
#                            'stripe_plan': None,
#                            'subject': '',
#                            'thank_you_page_id': 72089394,
#                            'updated_at': '2022-01-25T11:08:46.000Z'}],
#              'status': 'paid',
#              'stripe_customer_token': 'pm_1KPltNAJMLcS71G7AyPBYtYU',
#              'subscription_id': None,
#              'updated_at': '2022-02-05T10:53:23.000Z'}}


class ClickFunnelSale(http.Controller):

    def _find_products(self, event):
        Product = request.env['product.product']
        click_product_ids = [product['id'] for product in event['purchase']['products']]
        prods = {product_id.click_funnel_id: product_id for product_id in Product.search([('click_funnel_id', 'in', click_product_ids)])}

        if len(click_product_ids) != Product.search_count([('click_funnel_id', 'in', click_product_ids)]):
            _logger.error('Some of the click funnel products id "%s" are not found', click_product_ids)
            return False

        product_ids = []
        for product in event['purchase']['products']:
            product_id = prods[product['id']]
            product_ids.append({
                'product_id': product_id.id,
                'name': product_id.name,
                'price_unit': product['amount']['cents'] / 100.0,
                'product_uom_qty': 1.0,
                'product_uom': product_id.uom_id.id,
            })

        return product_ids

    def _get_contact_value(self, contact):
        country_id = request.env['res.country'].search([('code', '=', contact['country'])])
        return {
            'street': contact['shipping_address'],
            'city': contact['shipping_city'],
            'zip': contact['shipping_zip'],
            'vat': contact['vat_number'] if contact['vat_number'] else False,
            'phone': contact['phone'],
            'firstname': contact['first_name'],
            'lastname': contact['last_name'],
            'name': contact['name'],
            'country_id': country_id.id,
            'email': contact['email'],
        }

    def _find_or_create_partner(self, event, funnel_id):
        contact = event['purchase']['contact']
        Partner = request.env['res.partner']
        partner_ids = Partner.search([('email', '=ilike', contact['email'])])

        partner_id = None
        if len(partner_ids) > 1:
            for contact_id in partner_ids:
                if (contact_id.street == contact['shipping_address'] and
                        contact_id.city == contact['shipping_city'] and
                        contact_id.zip == contact['shipping_zip'] and
                        ((contact['vat_number'] and contact_id.vat == contact['vat_number']) or not contact['vat_number']) and
                        contact_id.phone == contact['phone'] and
                        contact_id.firstname == contact['first_name'] and
                        contact_id.lastname == contact['last_name']
                ):
                    partner_id = contact_id.parent_id or contact_id
                    _logger.info(_('Choose contact %s from %s'), partner_id.name, partner_ids)
                    break

            # all info are different then we set the first contact
            if not partner_id:
                partner_id = partner_ids[0].parent_id or partner_ids[0]
                _logger.info(_('No Contact matches then choose contact %s from %s'), partner_id.name, partner_ids)

        elif len(partner_ids) == 1:
            partner_id = partner_ids
            _logger.info(_('Only one Contact found contact %s'), partner_id.name)

        if partner_id:
            # if something changes from our current info then we create a new contact for the partner
            if ( partner_id.street != contact['shipping_address'] or
                 partner_id.city != contact['shipping_city'] or
                 partner_id.zip != contact['shipping_zip'] or
                 ( contact['vat_number'] and partner_id.vat != contact['vat_number'] ) or
                 partner_id.phone != contact['phone'] or
                 partner_id.firstname != contact['first_name'] or
                 partner_id.lastname != contact['last_name']
            ):
                values = self._get_contact_value(contact)
                values['type'] = 'delivery'
                # Set the language based on the funnel
                if funnel_id and funnel_id.lang_id:
                    values['lang'] = funnel_id.lang_id.code
                parent_id = partner_id
                values['parent_id'] = parent_id.id
                partner_id = Partner.create(values)
                _logger.info(_('Creating a new delivery address %s for the parent %s'), partner_id.name, parent_id.name)
        else:
            # otherwise we will create a new one
            partner_id = Partner.create(self._get_contact_value(contact))
            _logger.info(_('Creating a new contact %s'), partner_id.name)

        return partner_id

    def _get_sale_value(self, partner_id, event):
        currency_id = self._find_currency(event['purchase']['original_amount_currency'])
        return {
            'partner_id': partner_id.id,
            'click_funnel_charge_id': event['purchase']['charge_id'],
            'currency_id': currency_id.id,
        }

    @api.returns('click.funnel')
    @api.model
    def _find_funnel(self, funnel_id):
        return request.env['click.funnel'].sudo().search([('click_funnel_id', '=', funnel_id)])

    @api.returns('res.currency')
    @api.model
    def _find_currency(self, currency):
        return request.env['res.currency'].search([('name', '=', currency)])

    @api.model
    def _send_order_confirmation_email(self, order_id, template_id=None, lang=None):
        if not template_id:
            template_id = order_id.with_context(lang=lang)._find_mail_template()
        template = request.env['mail.template'].with_context(lang=lang).browse(template_id)
        if template.lang:
            lang = template._render_lang(order_id.ids)[order_id.id]

        composer = (
            request.env["mail.compose.message"]
            .with_context(
                {
                    'lang': lang,
                    'default_model': 'sale.order',
                    'default_res_id': order_id.id,
                    'default_use_template': bool(template_id),
                    'default_template_id': template_id,
                    'default_composition_mode': 'comment',
                    'mark_so_as_sent': True,
                    'custom_layout': "mail.mail_notification_paynow",
                    'proforma': False,
                    'force_email': True,
                    'model_description': order_id.with_context(lang=lang).type_name,
                }
            )
            .create({})
        )
        values = composer.onchange_template_id(
            template_id, "comment", "sale.order", order_id.id
        )["value"]
        composer.write(values)
        composer.send_mail()

    @api.model
    def _send_invoice_email(self, invoice_id, template_id=None, lang=None):
        if not template_id:
            template_id = self.env.ref('account.email_template_edi_invoice', raise_if_not_found=False).id
        template = request.env['mail.template'].with_context(lang=lang).browse(template_id)
        if template.lang:
            lang = template.with_context(lang=lang)._render_lang(invoice_id.ids)[invoice_id.id]

        composer = (
            request.env["mail.compose.message"]
            .with_context(
                {
                    'lang': lang,
                    'default_model': 'account.move',
                    'default_res_id': invoice_id.id,
                    'default_use_template': bool(template_id),
                    'default_template_id': template_id,
                    'default_composition_mode': 'comment',
                    'mark_invoice_as_sent': True,
                    'custom_layout': "mail.mail_notification_paynow",
                    'proforma': False,
                    'force_email': True,
                    'model_description': invoice_id.with_context(lang=lang).type_name,
                }
            )
            .create({})
        )
        values = composer.onchange_template_id(
            template_id, "comment", "account.move", invoice_id.id
        )["value"]
        composer.write(values)
        composer.send_mail()

    @api.model
    def _pay_invoice(self, invoice_id, journal_id):
        return request.env['account.payment.register'].\
            with_context(active_model='account.move', active_ids=invoice_id.ids).\
            create({
                'company_id': invoice_id.company_id.id,
                'currency_id': invoice_id.currency_id.id,
                'amount': abs(invoice_id.amount_total),
                'payment_type': 'inbound',
                'payment_date': invoice_id.invoice_date,
                'journal_id': journal_id.id,
                'partner_id': invoice_id.commercial_partner_id.id,
            }).\
            _create_payments()

    @http.route(['/click_funnel/webhooks/sale', '/funnel_webhooks/test'], type='json', methods=['POST'], auth='public', csrf=False)
    def webhook_sale(self, **kwargs):
        httpdata = request.httprequest.data

        if type(httpdata) == bytes:
            httpdata = httpdata.decode('utf8')

        _logger.info(_('Creating a new sale order "{}"').format(httpdata))

        # so we use json.load() to convert the payload
        event = json.loads(httpdata)

        pprint.pprint(event)

        # We manage only purchase events
        if 'purchase' not in event or 'event' not in event:
            return Response(status=400)

        status = event['purchase']['status']

        if status == 'failed':
            _logger.warning('The sale has failed: "%s"', httpdata)
            return Response(status=200)

        funnel_id = self._find_funnel(event['purchase']['funnel_id'])
        request._env = None
        if funnel_id and funnel_id.user_id:
            request.uid = funnel_id.user_id.id
        else:
            request.uid = 1

        SaleOrder = request.env['sale.order']
        OrderLine = request.env['sale.order.line']
        lines = request.env['sale.order.line']

        click_funnel_charge_id = event['purchase']['charge_id']
        order_id = SaleOrder.search([('click_funnel_charge_id', '=', click_funnel_charge_id)])
        if SaleOrder.search([('click_funnel_charge_id', '=', click_funnel_charge_id)]):
            _logger.info(_('The sale order "%s" has been already generated'), order_id.name)
            return Response(status=200)

        product_ids = self._find_products(event)

        if not product_ids:
            return Response(status=400)

        partner_id = self._find_or_create_partner(event, funnel_id)

        sale_value = self._get_sale_value(partner_id, event)

        if funnel_id:
            _logger.info('Using Click Funnel configuration %s', funnel_id.name)
            sale_value.update({
                'click_funnel_id': funnel_id.id,
                'warehouse_id': funnel_id.warehouse_id.id,
                'company_id': funnel_id.company_id.id,
            })
            if funnel_id.user_id:
                sale_value['user_id'] = funnel_id.user_id.id
            if funnel_id.team_id:
                sale_value['team_id'] = funnel_id.team_id.id
            if funnel_id.pricelist_id:
                sale_value['pricelist_id'] = funnel_id.pricelist_id.id

            SaleOrder = SaleOrder.with_company(funnel_id.company_id)
            OrderLine = OrderLine.with_company(funnel_id.company_id)

        # Create the sale order
        _logger.info(_('Creating a new sale order for the funnel "%s" '), funnel_id.name if funnel_id else 'None')
        order_id = SaleOrder.create(sale_value)
        order_id.onchange_partner_id()
        # Log the payload as internal note
        order_id._message_log(body=_('ClickFunnel payload:\n{}').format(pprint.pformat(event, indent=4)))

        if funnel_id and funnel_id.user_id:
            order_id.user_id = funnel_id.user_id.id

        # Set the fiscal position if needed
        if funnel_id and not order_id.fiscal_position_id and funnel_id and funnel_id.fiscal_position_id:
            order_id.fiscal_position_id = funnel_id.fiscal_position_id.id

        # Compute the taxes if necessary
        order_id._compute_tax_id()

        for value in product_ids:
            value['order_id'] = order_id.id
            sale_order_line = OrderLine.create(value)

            sale_order_line.product_id_change()
            sale_order_line.update({
                'price_unit': value['price_unit'],
            })
            lines += sale_order_line

        order_id.order_line = lines

        # Automatic subscribe followers if needed
        if funnel_id and funnel_id.auto_followers:
            try:
                # We might fail to send the subscription email, so let's catch it and break it
                order_id.message_subscribe(partner_ids=funnel_id.auto_followers.ids)
            except AssertionError:
                pass

        if status == 'paid' and (not funnel_id or (funnel_id and funnel_id.can_confirm_sale)):
            order_id.action_confirm()
            _logger.info(_('Confirmed Sale Order %s from Click Funnel'), order_id.name)
            order_id._compute_tax_id()

            invoice_id = None
            lang = funnel_id.lang_id.code if funnel_id and funnel_id.lang_id else None

            if funnel_id and funnel_id.can_create_invoice and funnel_id.can_confirm_sale:
                order_id._force_lines_to_invoice_policy_order()
                _logger.info(_('Creating Invoice from Sale Order %s from Click Funnel'), order_id.name)
                invoice_id = order_id._create_invoices()
                invoice_id.journal_id = funnel_id.journal_id.id
                invoice_id.action_post()
                _logger.info(_('New Invoice %s from Sale Order %s from Click Funnel'), invoice_id.name, order_id.name)
                payment = self._pay_invoice(invoice_id, funnel_id.payment_journal_id)
                _logger.info(_('Creating Payment %s for Invoice %s from Click Funnel'), payment.name, invoice_id.name)

            if funnel_id and funnel_id.can_send_confirmation_email:
                template_id = funnel_id.confirmation_email_template_id.id if funnel_id.confirmation_email_template_id else None
                self._send_order_confirmation_email(order_id, template_id=template_id, lang=lang)

            if invoice_id and funnel_id and funnel_id.can_send_invoice_confirmation_email:
                template_id = funnel_id.invoice_email_template_id.id if funnel_id.invoice_email_template_id else None
                self._send_invoice_email(invoice_id, template_id=template_id, lang=lang)

        return Response(status=200)