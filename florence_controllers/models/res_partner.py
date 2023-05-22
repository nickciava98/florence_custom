from odoo import models, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    # def _get_contact_name(self, partner, name):
    #     return "%s [%s]" % (name, partner.commercial_company_name or partner.sudo().parent_id.name)
    #
    # def name_get(self):
    #     res = []
    #
    #     for partner in self:
    #         res.append((
    #             partner.id, "%s [%s]" % (
    #                 partner.name, partner.commercial_company_name or partner.sudo().parent_id.name
    #             ) if partner.commercial_company_name or partner.sudo().parent_id.name else "%s" % partner.name
    #         ))
    #
    #     return res
    #
    # @api.depends("is_company", "name", "parent_id.display_name", "type", "company_name", "commercial_company_name")
    # def _compute_display_name(self):
    #     for partner in self:
    #         partner.display_name = "%s [%s]" % (
    #             partner.name, partner.commercial_company_name or partner.sudo().parent_id.name
    #         ) if partner.commercial_company_name or partner.sudo().parent_id.name else "%s" % partner.name
