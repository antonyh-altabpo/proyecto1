# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AltaBpoAccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    purchase_statistic_id = fields.Many2one('purchase.statistic', string='Purchase Order', readonly=True, copy=False)
    settlement_date = fields.Date(related='move_id.settlement_date', string='Settlement date', copy=False)
