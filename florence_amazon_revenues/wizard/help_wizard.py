from odoo import models, fields, api


class HelpWizard(models.TransientModel):
    _name = "help.wizard"
    _description = "Help Wizard"

    state = fields.Selection(
        [("1", "Step 1"),
         ("2", "Step 2")],
        default = "1"
    )
    step = fields.Integer(
        compute = "_compute_step"
    )
    guide = fields.Text(
        compute = "_compute_guide"
    )

    @api.depends("state")
    def _compute_step(self):
        for line in self:
            line.step = int(line.state) - 1

    @api.depends("state")
    def _compute_guide(self):
        for line in self:
            line.guide = ""

            if line.state == "1":
                line.guide = "" \
                    "Introduzione alla guida di utilizzo " \
                    "del modulo Amazon Revenues sviluppato " \
                    "da Niccolò Ciavarella per Florence Organics Ltd"
            elif line.state == "2":
                line.guide = "Primo passo per la guida"

    def action_next(self):
        self.write(
            {'state': str(int(self.state) + 1)}
        )

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'help.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new'
        }

    def action_previous(self):
        self.write(
            {'state': str(int(self.state) - 1)}
        )

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'help.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new'
        }
