from odoo import models, fields, api


class HelpWizardSaleOrder(models.TransientModel):
    _name = "help.wizard.sale.order"
    _description = "Help Wizard for Sale Order"

    state = fields.Selection(
        [("0", "Sale Order"),
         ("1", "Schermata principale"),
         ("2", "Order Line"),
         ("3", "Data entry"),
         ("4", "Gestione dei Free Sample")],
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
                line.guide = "Introduzione alla guida di utilizzo " \
                             "del Sale Order per la creazione di PRO-Forma"
            elif line.state == "1":
                line.guide = "La schermata principale mostra una panoramica dei dati del " \
                             "destinatario, come anagrafica e contatti, e la selezione del " \
                             "Quotation Template, utile per la creazione di PRO-Forma da modello"
            elif line.state == "2":
                line.guide = "Nel tab Order Lines ci saranno le righe dell'ordine con tutti i prodotti " \
                             "inseriti o presenti nel template.\n\n" \
                             "Per ognuno di essi è necessario inserire una descrizione (che apparirà nel PDF), " \
                             "la quantità e il costo"
            elif line.state == "3":
                line.guide = "L'inserimento dei dati è immediato e spesso automatico.\n\n" \
                             "Bisogna fare attenzione al campo VAT, il quale non sarà popolato in automatico, " \
                             "sarà dunque necessario selezionare l'aliquota corrispondente in manuale, altrimenti " \
                             "verrà mostrato un messaggio di errore.\n\n" \
                             "N.B. questa regola non si applica al prodotto Free Sample"
            elif line.state == "4":
                line.guide = "Per la corretta gestione dei Free Sample è necessario innanzitutto selezionare un " \
                             "Quotation Template che contiene la spunta sul campo Is Free Sample.\n\n" \
                             "Dopo aver fatto ciò sarà necessario controllare le righe dell Order Line per assicurarsi " \
                             "che tutto sia corretto, aggiungendo eventualmente l'aliquota IVA dove mancante.\n\n" \
                             "Qualora siano state effettuate modifiche ai prodotti prelevati dal template (es. aggiunta di " \
                             "nuove righe, rimozione di altre o modifica del prezzo) sarà necessario cliccare sul cestino " \
                             "situato accanto alla riga relativa al prodotto Free Sample per permettere al sistema di rigenerare " \
                             "il prodotto Free Sample con prezzo negativo integrando le nuove modifiche.\n\n" \
                             "Questa operazione è assolutamente necessaria in quanto la non esecuzione della stessa può creare " \
                             "problemi sul calcolo del totale (il quale sarà diverso da zero) con ripercussioni contabili.\n\n" \
                             "N.B. non è necessario inserire lo sconto del 100%, in quanto l'applicazione di uno sconto del 100% " \
                             "invaliderebbe tutti i passaggi precedenti e renderebbe l'ordine errato. Tuttavia verrà in automatico " \
                             "visualizzato uno sconto del 100% nel PDF di stampa in ogni riga dell'order line"

    def action_next(self):
        self.write(
            {'state': str(int(self.state) + 1)}
        )

        return {
            'name': 'Help Guide',
            'type': 'ir.actions.act_window',
            'res_model': 'help.wizard.sale.order',
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
            'res_model': 'help.wizard.sale.order',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new'
        }