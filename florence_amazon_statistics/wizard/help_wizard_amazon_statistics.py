from odoo import models, fields, api


class HelpWizardAmazonStatistics(models.TransientModel):
    _name = "help.wizard.amazon.statistics"
    _description = "Help Wizard for Amazon Statistics"

    state = fields.Selection(
        [("0", "Amazon Statistics"),
         ("1", "Schermata principale"),
         ("2", "I due tab Statistics e Statistics Test"),
         ("3", "Funzionamento del data entry"),
         ("4", "Liste e grafici con e senza filtraggio")],
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
                    "Introduzione alla guida di utilizzo " \
                    "del modulo Amazon Statistics sviluppato " \
                    "da Niccolò Ciavarella per Florence Organics Ltd"
            elif line.state == "1":
                line.guide = "La schermata principale mostra un riepilogo con " \
                             "Marketplace di riferimento e prodotto"
            elif line.state == "2":
                line.guide = "In basso è possibile visualizzare due tab:\n" \
                             "1 - Statistics\n" \
                             "2 - Statistics Test\n" \
                             "Ognuno di questi tab mostra un riepilogo generale" \
                             "dei dati, con il primo tab visto come ufficiale e il secondo " \
                             "come test per visualizzare una previsione dell'andamento"
            elif line.state == "3":
                line.guide = "Nel tab Statistics i dati vanno inseriti manualmente ad eccezione di:\n" \
                             "- #Stars Ratings New: verrà calcolato in automatico attraverso la seguente formula: " \
                             "#Stars Ratings[oggi] - #Stars Ratings[ieri]\n" \
                             "- #Stars Reviews New: verrà calcolato in automatico attraverso la seguente formula: " \
                             "#Stars Reviews[oggi] - #Stars Reviews[ieri]\n" \
                             "- Total #Stars Reviews: verrà calcolato in automatico attraverso la seguente formula: " \
                             "#Stars Ratings New + #Stars Reviews New\n" \
                             "- #Stars Value: verrà calcolato in automatico attraverso la seguente formula: " \
                             "#Stars x Total #Stars Reviews\n" \
                             "- General Reviews Statistics: verrà calcolato in automatico attraverso la seguente formula: " \
                             "Sum[#Stars Value] / Sum[Total #Stars Reviews]\n" \
                             "- Daily Total Reviews: verrà calcolato in automatico attraverso la seguente formula: " \
                             "Sum[Total #Stars Reviews]\n" \
                             "- Main Stat: verrà calcolato in automatico attraverso la seguente formula: " \
                             "Avg[General Reviews Statistics] complessiva di ogni linea\n" \
                             "Il tab Statistics Test segue le stesse regole del tab precedente"
            elif line.state == "4":
                line.guide = "In ognuno dei due tab sono presenti dei campi per il filtraggio nella sezione " \
                             "Pivot and Chart Analysis:\n" \
                             "- Filter by date: data inizio e data fine\n" \
                             "e dei pulsanti che richiamano delle azioni, i quali compaiono solo se le due date" \
                             "precedenti sono compilate:\n" \
                             "- Statistics List: lista di tutti i dati\n" \
                             "- Statistics Analysis: grafico con tutti i dati come misura\n" \
                             "- Statistics Pivot: tabella con la panoramica dei dati\n" \
                             "Nella sezione successiva è possibile vedere la media che viene calcolata in automatico" \
                             "attraverso la seguente formula: Sum[#Stars Value]/Sum[Total #Stars Reviews]\n" \
                             "Inoltre è presente un campo per un fattore correttivo che aggiusta la media eguagliandola" \
                             "al valore visibile su Amazon"

    def action_next(self):
        self.write(
            {'state': str(int(self.state) + 1)}
        )

        return {
            'name': 'Help Guide',
            'type': 'ir.actions.act_window',
            'res_model': 'help.wizard.amazon.statistics',
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
            'res_model': 'help.wizard.amazon.statistics',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new'
        }
