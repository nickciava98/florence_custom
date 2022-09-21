from odoo import models, fields, api


class HelpWizard(models.TransientModel):
    _name = "help.wizard.amz.rev"
    _description = "Help Wizard"

    state = fields.Selection(
        [("0", "Amazon Revenues"),
         ("1", "Schermata principale"),
         ("2", "I due tab Incidence e Test Area"),
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
                    "del modulo Amazon Revenues sviluppato " \
                    "da Niccolò Ciavarella per Florence Organics Ltd"
            elif line.state == "1":
                line.guide = "La schermata principale mostra un riepilogo con " \
                             "Marketplace di riferimento e prodotto"
            elif line.state == "2":
                line.guide = "In basso è possibile visualizzare due tab:\n" \
                             "1 - Incidence\n" \
                             "2 - Test Area\n" \
                             "Ognuno di questi tab mostra un riepilogo generale" \
                             "dei dati, con il primo tab visto come ufficiale e il secondo" \
                             "come test per visualizzare una previsione dell'andamento"
            elif line.state == "3":
                line.guide = "Nel tab Incidence i dati vanno inseriti manualmente ad eccezione di:\n" \
                             "- VAT: verrà inserito in automatico in base al marketplace selezionato, " \
                             "rispettando le aliquote IVA del paese di riferimento e lo scorporo effettuato da Amazon\n" \
                             "- Sku Cost: verrà inserito in automatico prelevando il valore dal modulo Manufacturing Cost " \
                             "se il prodotto è presente, altrimenti verrà inserito 0.00 come valore da modificare manualmente\n" \
                             "- Gross Revenues: verrà calcolato in automatico attraverso la seguente formula: " \
                             "Selling Price - Amazon Fees - VAT - Sku Cost\n" \
                             "- Ads Cost Per Unit: verrà calcolato in automatico attraverso la seguente formula: " \
                             "Ads Total Cost / Pcs Sold\n" \
                             "- Earned Per Pc: verrà calcolato in automatico attraverso la seguente formula: " \
                             "Gross Revenues - Ads Cost Per Unit\n" \
                             "- Probable Income: verrà calcolato in automatico attraverso la seguente formula: " \
                             "Earned Per Pc x Pcs Sold\n" \
                             "Il tab Test Area segue le stesse regole del tab precedente"
            elif line.state == "4":
                line.guide = "In ognuno dei due tab sono presenti dei campi per il filtraggio:\n" \
                             "- Filter by date: data inizio e data fine\n" \
                             "e dei pulsanti che richiamano delle azioni:\n" \
                             "- Revenues Analysis\n" \
                             "- Revenues List\n" \
                             "I primi due campi data servono per stabilire l'intervallo temporale attraverso" \
                             "cui filtrare i dati presenti nel grafico richiamabile tramite il pulsante" \
                             "Revenues Analysis e nella lista richiamabile tramite il pulsante Revenues List.\n" \
                             "Questi due campi possono anche essere vuoti, e se sono vuoti i due pulsanti richiamano" \
                             "lista e grafico complessivo, visualizzando tutti i dati presenti"

    def action_next(self):
        self.write(
            {'state': str(int(self.state) + 1)}
        )

        return {
            'name': 'Help Guide',
            'type': 'ir.actions.act_window',
            'res_model': 'help.wizard.amz.rev',
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
            'res_model': 'help.wizard.amz.rev',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new'
        }
