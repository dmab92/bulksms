# -*- coding: utf-8 -*-
# from odoo import http


# class BulkSms(http.Controller):
#     @http.route('/bulk_sms/bulk_sms/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bulk_sms/bulk_sms/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('bulk_sms.listing', {
#             'root': '/bulk_sms/bulk_sms',
#             'objects': http.request.env['bulk_sms.bulk_sms'].search([]),
#         })

#     @http.route('/bulk_sms/bulk_sms/objects/<model("bulk_sms.bulk_sms"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bulk_sms.object', {
#             'object': obj
#         })
