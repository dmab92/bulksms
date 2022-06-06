# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, _

from odoo.exceptions import UserError, Warning, ValidationError


class locataire(models.Model):
    _name = "bulk.locataire"
    _description = "locataire pour bulk SMS"
    _order = 'id DESC'

    name = fields.Char("Nom et Prenoms", required=True)
    phone = fields.Char("Telephone", default='237', required=True)
    date_register = fields.Datetime("Date d''Entree")
    state = fields.Selection( [('actif', 'Actif'),
                             ('inactif', 'Inactif')],
                            string='Etat', default='actif')
    
    locataire_id = fields.Many2one('locataire.bulk.sms')

    date_next_pay = fields.Datetime("Date du prochain Payement")
    civility = fields.Selection([('M', 'M.'),
                            ('Mme', 'Mme')],
                            string='Civilité', required=True,
                            help="Il s'agit de la civilité du Locataire")
    
    
class sms_locataire(models.Model):
    _name = "locataire.bulk.sms"
    _description = "Envoi de bulk SMS au locataire"
    _order = 'id DESC'

    name = fields.Char("Nom de la campagne de SMS", required=True)
    date_register = fields.Datetime("Date d'envoi")
    line_locataires = fields.Many2many('bulk.locataire', string="Liste des locataires Actifs")
    state_sms = fields.Selection([('draft', 'Brouillon'),
                            ('send', 'Envoyé')],
                            string='Etat', default='draft',
                            help="Il s'agit de l'Etat des SMS, il peuvent etre en brouillon(en attente d'envoi) ou alors Envoyé")



    def load_locataire(self):
        for record in self:
            locataires_ids = self.env['locataire.bulk.sms'].search([('state', '=', 'actif')])
            lines = [(5, 0, 0)]
            for locataire in locataires_ids:
                vals = {
                     'name': locataire.name,
                     'phone': locataire.phone,
                     'date_next_pay':locataire.date_next_pay,
                     'stae': 'actif', 
                  }
                lines.append((0, 0, vals))
        record.line_locataires = lines


    def send_sms(self):
         #SMS a l'expediteur
        api_key='b0l5cGl6TE5JZmt6ZkdIZEZsTUQ='
        url = 'https://app.techsoft-web-agency.com/sms/api'
        senderID='MTCS SARL'
        for record in self:
            for locataire in record.line_locataires:
                destination = str(locataire.phone)
                message = +locataire.civility +" " +locataire.name + " votre loyer arrive a expiration ce " + str(locataire.date_next_pay)+" Veillez penser à le renouveller. Merci"
                sms_body = {
                    'action': 'send-sms',
                    'api_key': api_key,
                    'to': destination,
                    'from': senderID,
                    'sms': message
                }
                final_url1 = url + "?" + urllib.parse.urlencode(sms_body)
                requests.get(final_url1)
        return self.write({'state': 'send'})
