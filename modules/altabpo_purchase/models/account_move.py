# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools import date_utils


class AltaBpoAccountMove(models.Model):
    _inherit = 'account.move'

    settlement_date = fields.Date(compute="_compute_amount", string='Settlement date', store=True, copy=False)

    @api.depends(
        'line_ids.debit',
        'line_ids.credit',
        'line_ids.currency_id',
        'line_ids.amount_currency',
        'line_ids.amount_residual',
        'line_ids.amount_residual_currency',
        'line_ids.payment_id.state')
    def _compute_amount(self):
        res = super(AltaBpoAccountMove, self)._compute_amount()
        for record in self:
            if record.invoice_payment_state == 'paid':
                record.settlement_date = fields.date.today()
                star_date = date_utils.start_of(record.settlement_date, 'year')
                end_date = date_utils.end_of(record.settlement_date, 'year')
                for line in record.invoice_line_ids:
                    if line.purchase_statistic_id:
                        # error
                        analysis_date = line.purchase_statistic_id  .analysis_date
                        if star_date <= analysis_date <= end_date:
                            # si la fecha de liquidacion esta en el mismo mes, no hace nada
                            pass
                        else:
                            line.write({'purchase_statistic_id': False})
                            if line.product_id.cost_fob:
                                purchase_statistic = record.env['purchase.statistic'].search([
                                    ('analysis_date', '>=', star_date),
                                    ('analysis_date', '<=', end_date),
                                    ('product_id', '=', line.product_id.id)])
                                if purchase_statistic:
                                    line.write({'purchase_statistic_id': purchase_statistic.id})
                                else:
                                    purchase_statistic = record.env['purchase.statistic'].create(
                                        {'product_id': line.product_id.id, 'analysis_date': record.settlement_date
                                         })
                                    line.write({'purchase_statistic_id': purchase_statistic.id})
                    else:
                        if line.product_id.cost_fob:
                            purchase_statistic = record.env['purchase.statistic'].search([
                                ('analysis_date', '>=', star_date),
                                ('analysis_date', '<=', end_date),
                                ('product_id', '=', line.product_id.id)])
                            if purchase_statistic:
                                line.write({'purchase_statistic_id': purchase_statistic.id})
                            else:
                                purchase_statistic = record.env['purchase.statistic'].create(
                                    {'product_id': line.product_id.id, 'analysis_date': record.settlement_date
                                     })
                                line.write({'purchase_statistic_id': purchase_statistic.id})
                    print("product_id--->", line.product_id.cost_fob)
            else:
                record.settlement_date = False
        return res

