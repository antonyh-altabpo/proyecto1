# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AltaBpoProductTemplate(models.Model):
    _inherit = 'product.template'

    cost_fob = fields.Boolean(string="active in statistical", help="see product in statistical table of purchase")

    kg_box = fields.Float(string="Kg/Box")
    box_pal = fields.Float(string="Box/Pal")
    mt2_cja = fields.Float(string="mt2/CJA")
