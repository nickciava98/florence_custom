from odoo import models, fields, api


class HelpWizard(models.TransientModel):
    _name = "help.wizard.amz.stats"
    _description = "Help Wizard"

    state = fields.Selection(
        [("0", "Amazon Statistics"),
         ("1", "Schermata principale"),
         ("2", "I due tab Statistics e Statistics Test"),
         ("3", "Funzionamento del data entry"),
         ("4", "Liste e grafici con e senza filtraggio")],
        default="0"
    )
    guide = fields.Text(
        compute="_compute_guide"
    )
    info_and_contacts = fields.Text(
        default="For more info and questions send a mail to: "
                "<a href='mailto:niccolo@florenceorganics.com'>niccolo@florenceorganics.com</a> "
                "or call/SMS to: <a href='tel:+393317438243'>(+39) 331 743 8243</a> "
                "or WhatsApp to: <a href='https://wa.me/393317438243'>Niccolò Ciavarella</a>"
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
                line.guide = "In basso è possibile visualizzare due tab:\n\n" \
                             "1 - Statistics\n\n" \
                             "2 - Statistics Test\n\n" \
                             "Ognuno di questi tab mostra un riepilogo generale" \
                             "dei dati, con il primo tab visto come ufficiale e il secondo " \
                             "come test per visualizzare una previsione dell'andamento"
            elif line.state == "3":
                line.guide = "Nel tab Statistics i dati vanno inseriti manualmente ad eccezione di:\n\n" \
                             "- #Stars Ratings New: verrà calcolato in automatico attraverso la seguente formula: " \
                             "#Stars Ratings[oggi] - #Stars Ratings[ieri]\n\n" \
                             "- #Stars Reviews New: verrà calcolato in automatico attraverso la seguente formula: " \
                             "#Stars Reviews[oggi] - #Stars Reviews[ieri]\n\n" \
                             "- Total #Stars Reviews: verrà calcolato in automatico attraverso la seguente formula: " \
                             "#Stars Ratings New + #Stars Reviews New\n\n" \
                             "- #Stars Value: verrà calcolato in automatico attraverso la seguente formula: " \
                             "#Stars x Total #Stars Reviews\n\n" \
                             "- General Reviews Statistics: verrà calcolato in automatico attraverso la seguente formula: " \
                             "Sum[#Stars Value] / Sum[Total #Stars Reviews]\n\n" \
                             "- Daily Total Reviews: verrà calcolato in automatico attraverso la seguente formula: " \
                             "Sum[Total #Stars Reviews]\n\n" \
                             "- Main Stat: verrà calcolato in automatico attraverso la seguente formula: " \
                             "Avg[General Reviews Statistics] complessiva di ogni linea\n\n" \
                             "Il tab Statistics Test segue le stesse regole del tab precedente"
            elif line.state == "4":
                line.guide = "In ognuno dei due tab sono presenti dei campi per il filtraggio nella sezione " \
                             "Pivot and Chart Analysis:\n\n" \
                             "- Filter by date: data inizio e data fine\n" \
                             "- Group by: daily/weekly/monthly statistics, per il raggrupamento dei dati (ad es. nella lista)\n\n" \
                             "e dei pulsanti che richiamano delle azioni, i quali compaiono solo se group by e le due date " \
                             "precedenti sono compilate:\n\n" \
                             "- Statistics List: lista di tutti i dati\n\n" \
                             "- Statistics Dashboard: dashboard con tutti i valori fondamentali (grafici, pivot e aggregazioni)\n\n" \
                             "- Statistics Analysis: grafico con tutti i dati come misura\n\n" \
                             "- Statistics Pivot: tabella con la panoramica dei dati\n\n" \
                             "Nella sezione successiva è possibile vedere la media che viene calcolata in automatico" \
                             "attraverso la seguente formula: Sum[#Stars Value]/Sum[Total #Stars Reviews]\n\n" \
                             "Inoltre è presente un campo per un fattore correttivo che aggiusta la media eguagliandola" \
                             "al valore visibile su Amazon"

    def action_next(self):
        self.write(
            {'state': str(int(self.state) + 1)}
        )

        return {
            'name': 'Help Guide',
            'type': 'ir.actions.act_window',
            'res_model': 'help.wizard.amz.stats',
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
            'res_model': 'help.wizard.amz.stats',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new'
        }
