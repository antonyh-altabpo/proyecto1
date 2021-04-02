# -*- coding: utf-8 -*-
# from odoo import http


# class AltabpoStock(http.Controller):
#     @http.route('/altabpo_stock/altabpo_stock/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/altabpo_stock/altabpo_stock/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('altabpo_stock.listing', {
#             'root': '/altabpo_stock/altabpo_stock',
#             'objects': http.request.env['altabpo_stock.altabpo_stock'].search([]),
#         })

#     @http.route('/altabpo_stock/altabpo_stock/objects/<model("altabpo_stock.altabpo_stock"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('altabpo_stock.object', {
#             'object': obj
#         })
