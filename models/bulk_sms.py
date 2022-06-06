# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, _
import time, random
import datetime
#import pywhatkit
#pywhatkit.start_server()
import urllib, requests
from datetime import datetime
from odoo.exceptions import UserError, Warning, ValidationError


class client_bulk_sms(models.Model):
    _name = "client.bulk.sms"
    _description = "Client de bulk SMS"
    _order = 'id DESC'

    name = fields.Char("Nom")
    company_id = fields.Many2one('res.company','Sociétes/Entités')
    phone = fields.Char("Telephone")
    #bulk_id = ma


class client_bulk_sms_state(models.Model):
    _name = "client.bulk.sms.etat"
    _description = "Etat du Client de bulk SMS"
    _order = 'id DESC'

    name = fields.Char("Nom")

class bulk_sms(models.Model):
    """Defining model for radio camando."""
    _description = 'Campagne de SMS en masse'
    _name = 'bulk.sms'
    _rec_name ='name'
    _order = 'id DESC'

    
    name = fields.Char("Objet")
    date_register = fields.Datetime('Date', default=fields.datetime.now())
    message = fields.Text("Message")
    company_ids = fields.Many2many('res.company', string="Sociétes/ Entités")
    partner_ids2 = fields.Many2many('res.partner', string="Personnes a toucher")

    partner_ids = fields.Many2many('client.bulk.sms', string="Personnes a toucher")
    photo = fields.Binary(string="Image à Envoyer")

    attachment_ids = fields.Many2many("ir.attachment")

    state = fields.Selection([('draft', 'Brouillon'),
                            ('send', 'Envoyé')],
                            string='Etat', default='draft',
                            help="Il s'agit de l'Etat des SMS, il peuvent etre en brouillon(en attente d'envoi) ou alors Envoyé")

    
    state_client = fields.Selection([('dac_month', "Est d'accord pour ce mois"),
                            ('dac-nect_month', "Est d'accord mais pas ce mois"),
                            ('pas_decroch', "N'a pas decroche"),
                            ('num_not_pas', 'Numero ne passe plus'),
                            ('not_dac', "N'est plus partant")],
                            string='Etat des clients', 
                            help="Il s'agit de l'Etat des Souscripteurs")

    user_id = fields.Many2one('res.partner', string="Utilisateur")

    souscripteur_etat_ids = fields.Many2many("client.bulk.sms.etat", string="Etat du Souscripteur")
    mobile = fields.Char("Mobile")

    def load_numers(self):
        for record in self:
            if not record.company_ids:
                clients_ids = self.env['res.partner'].search([('state', '=', record.state_client)])
            else: 
                clients_ids = self.env['res.partner'].search([('company_id', 'in', record.company_ids.ids),
                                                            ('state_client', '=', record.state_client)])

            #for record in self:
                #record.payment_ids = False
            lines = [(5, 0, 0)]
            for client in clients_ids:
                vals = {
                     'name': client.name,
                     'phone': client.phone,
                     'company_id': client.company_id and client.company_id.id, 
                     
                  }
                lines.append((0, 0, vals))
        record.partner_ids = lines
        #record.partner_ids2 = lines

                    #client.write({'partner_ids': [[0, 0, vals]]})



    def send_sms(self):
         #SMS a l'expediteur
        api_key='b0l5cGl6TE5JZmt6ZkdIZEZsTUQ='
        url = 'https://app.techsoft-web-agency.com/sms/api'
        #senderID = 'TESTE-DEMO'
        senderID='SOACAM'
        for record in self:
            for partner in record.partner_ids:
                destination = str(partner.phone)
                message = "M./Mme " + partner.name + " " + str(record.message)
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


    def send_whatsapp_message(self):
        if self.message and self.mobile:
            message_string = ''
            message = self.message.split(' ')
            for msg in message:
                message_string = message_string + msg + '%20'
            message_string = message_string[:(len(message_string) - 3)]
            url = 'https://api.whatsapp.com/send'
            destination = str(self.mobile)

            sms_body = {
                        'phone': destination,
                        'text': message_string,
                        }

            final_url1 = url + "?" + urllib.parse.urlencode(sms_body)
            requests.get(final_url1)
            
            raise UserError(_(final_url1))

            return {
                'type': 'ir.actions.act_url',
                'url': "https://api.whatsapp.com/send?phone="+self.mobile+"&text=" + message_string,
                'target': 'self',
                'res_id': self.id,
            }

    # def send_whatsapp_message(self):
    #     photo = self.photo
    #     pywhatkit.sendwhatmsg("+237697005649", "Bonjour Python", 10, 10)
    #     if self.photo and self.mobile:
    #         message_string = ''
    #         photo = self.photo
    #         # for msg in photo:
    #         #     message_string = message_string + msg + '%20'
    #         #message_string = message_string[:(len(message_string) - 3)]
    #         number = self.mobile

    #         link = "https://web.whatsapp.com/send?phone=" + number
    #         media="localhost:8069/web/image?model=bulk.sms&id=29&field=photo&unique=11022022114148"
    #         send_msg = {
    #             'type': 'ir.actions.act_url',
    #             'url': link + "&media=" + media,
    #             'target': 'new',
    #             'res_id': self.id,
    #         }

    #         return send_msg




    