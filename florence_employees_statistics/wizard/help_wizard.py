from odoo import models, fields, api


class HelpWizard(models.TransientModel):
    _name = "help.wizard.empl.stats"
    _description = "Help Wizard"

    state = fields.Selection(
        [("0", "Employees Statistics"),
         ("1", "Main Screen"),
         ("2", "Tab Statistics"),
         ("3", "Data entry"),
         ("4", "Lists and charts with and without filtering")],
        default = "0"
    )
    guide = fields.Text(
        compute = "_compute_guide"
    )

    @api.depends("state")
    def _compute_guide(self):
        for line in self:
            line.guide = ""

            if line.state == "0":
                line.guide = "" \
                    "Introducing help guide " \
                    "of Employees Statistics module developed " \
                    "by Niccolò Ciavarella for Florence Organics Ltd"
            elif line.state == "1":
                line.guide = "The main screen shows a summary with Employee's name " \
                             "and Job position, and chart manager"
            elif line.state == "2":
                line.guide = "Below the name and infos there is the main tab Statistics\n" \
                             "This tab shows a general summary with all of the datas available"
            elif line.state == "3":
                line.guide = "In the tab Statistics all data must be filled manually.\n" \
                             "Each column has a specific mean:\n" \
                             "- Date: this is the date of entry of the line datas\n" \
                             "- Benchmark: this is the value of the statistics\n" \
                             "- Value: this is a numeric value related to the benchmark"
            elif line.state == "4":
                line.guide = "It is possible to view custom chart based on:\n" \
                             "- Chart start and chart end: these values are used to define a temporal interval\n" \
                             "- Benchmark: this value is used to define the only benchmark to show\n" \
                             "When chart start, chart end and benchmark fields are filled, a new button will be visible below:\n" \
                             "- Employee's Statistics Chart: it will redirect to graph filtered with datas in chart manager" \
                             "In the top right corner there is a button called Employee's Statistics List:\n" \
                             "this button shows all of the datas available in the Statistics Tab but grouped by week"

    def action_next(self):
        self.write(
            {'state': str(int(self.state) + 1)}
        )

        return {
            'name': 'Help Guide',
            'type': 'ir.actions.act_window',
            'res_model': 'help.wizard.empl.stats',
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
            'name': 'Help Guide',
            'type': 'ir.actions.act_window',
            'res_model': 'help.wizard.empl.stats',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new'
        }
