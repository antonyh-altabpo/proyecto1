# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools import date_utils
from dateutil.relativedelta import relativedelta
from datetime import datetime

MONTHS_YEARS = [('january', 'Enero'), ('february', 'Febrero'), ('march', 'Marzo'), ('april', 'Abril'), ('may', 'Mayo'),
                ('june', 'Junio'), ('july', 'Julio'), ('august', 'Agosto'), ('september', 'Septiembre'),
                ('october', 'Octubre'), ('november', 'Noviembre'), ('december', 'Diciembre')
                ]


class PurchaseStatistic(models.Model):
    _name = 'purchase.statistic'
    _description = 'purchasing statistics'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    product_id = fields.Many2one('product.product', string='Product', required=True,
                                 domain=[('active', '=', True), ('cost_fob', '=', True)])
    # fields related product
    categ_id = fields.Many2one('product.category', related='product_id.categ_id')
    default_code = fields.Char(related='product_id.default_code', string='Internal Reference')
    description_purchase = fields.Text(related='product_id.description_purchase', string='Purchase Description',
                                       translate=True)
    qty_available = fields.Float(related='product_id.qty_available', string="Available")

    # standar fields
    analysis_date = fields.Date('Date', default=fields.Date.today(), required=True, copy=True, readonly=True)
    str_year = fields.Char(compute='_compute_str_year')

    name = fields.Char(string='Label')
    account_move_line_ids = fields.One2many('account.move.line', 'purchase_statistic_id', string='Related invoice',
                                            ondelete='restrict')

    # 12 months
    m1 = fields.Integer(string='January', compute="_compute_m")
    m2 = fields.Integer(string='February', compute="_compute_m")
    m3 = fields.Integer(string='March', compute="_compute_m")
    m4 = fields.Integer(string='April', compute="_compute_m")
    m5 = fields.Integer(string='May', compute="_compute_m")
    m6 = fields.Integer(string='June', compute="_compute_m")
    m7 = fields.Integer(string='July', compute="_compute_m")
    m8 = fields.Integer(string='August', compute="_compute_m")
    m9 = fields.Integer(string='September', compute="_compute_m")
    m10 = fields.Integer(string='October', compute="_compute_m")
    m11 = fields.Integer(string='November', compute="_compute_m")
    m12 = fields.Integer(string='December', compute="_compute_m")

    # compute fields
    # total_amount_year = fields.Integer(string="Total amount per year", compute="_compute_m")

    current_month_projection = fields.Float(string="Current month projection",
                                            compute="_compute_current_month_projection")
    average_sales = fields.Float(string="Average sales", compute="_compute_average_sales")
    current_break_date = fields.Date(string="current break date", compute="_compute_current_break")

    @api.depends('average_sales')
    def _compute_current_break(self):
        """= fecha actual +
        (stock / promedio
        de ventas * 30)
        Promedio de ventas anual
        """
        for record in self:
            date_today = fields.date.today()
            year = date_today.year
            if record.analysis_date.year == year:
                test = round(record.qty_available / record.average_sales * 30, 0)
                expired_date = fields.Datetime.from_string(date_today) + relativedelta(days=test)
                record.current_break_date = expired_date

    @api.depends('account_move_line_ids')
    def _compute_current_month_projection(self):
        """
        Campo numérico resultado de: Proyeccion mes
        actual = total ventas al día / cantidad de días
        concurridos * total días del mes
        Ejemplo:
        Total de ventas hoy = 30
        días hasta hoy = 10
        Total días del mes = 30
        Proyección mes actual = 10/15*28
        Proyección mes actual = 90
        :return:
        """
        for record in self:
            date_today = fields.date.today()
            year = date_today.year
            if record.analysis_date.year == year:
                month = date_today.month
                days = date_today.day
                end_date = date_utils.end_of(date_today, 'year').day
                m_count = getattr(record, "m" + str(month))
                record.current_month_projection = (m_count / days) * end_date
            else:
                record.current_month_projection = 0
                # m_all = [record.m1, record.m2, record.m3, record.m4, record.m5, record.m6, record.m7, record.m8,
                #          record.m9, record.m10, record.m11, record.m12]
                # max_value = max(m_all)
                # max_index = m_all.index(max_value)
                # year = record.analysis_date.year
                # old_date = fields.Date.from_string(str(year) + "-" + str(max_index + 1) + "-" + "01")
                # end_date = date_utils.end_of(old_date, 'month').day
                # record.current_month_projection = (m_all[max_index] / end_date) * end_date

    @api.depends('account_move_line_ids')
    def _compute_average_sales(self):
        """
        Campo numérico resultado de:
        Promedio ventas = total de la cantidad de
        seleccionados / la cantidad de los meses
        seleccionados
        ejemplo:
        Total ventas de los 8 meses seleccionado=
        100
        total meses seleccionado = 8
        Promedio = 100 / 8
        Promedio = 12,5
        :return:
        """
        for record in self:
            date_today = fields.date.today()
            year = date_today.year
            if record.analysis_date.year == year:
                expired_date = fields.Datetime.from_string(date_today) - relativedelta(years=1)
                account_line = record.env['account.move.line'].search([('settlement_date', '>=', expired_date),
                                                                       ('settlement_date', '<=', date_today),
                                                                       ('product_id', '=', record.product_id.id)])
                quantity = sum(account_line.mapped('quantity'))
            else:
                quantity = 0
                # quantity = record.total_amount_year
            prom = quantity / 12
            record.average_sales = prom

    @api.depends('analysis_date')
    def _compute_str_year(self):
        for record in self:
            if record.analysis_date:
                record.analysis_date = date_utils.start_of(record.analysis_date, 'year')
                record.str_year = record.analysis_date.strftime('%Y').lower()

    @api.depends('account_move_line_ids')
    def _compute_m(self):
        m = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for record in self:
            if record.account_move_line_ids:
                for line in record.account_move_line_ids:
                    month = line.move_id.settlement_date.month
                    if line.move_id.settlement_date.year == record.analysis_date.year:
                        if month == 1:
                            m[0] += line.quantity
                        elif month == 2:
                            m[1] += line.quantity
                        elif month == 3:
                            m[2] += line.quantity
                        elif month == 4:
                            m[3] += line.quantity
                        elif month == 5:
                            m[4] += line.quantity
                        elif month == 6:
                            m[5] += line.quantity
                        elif month == 7:
                            m[6] += line.quantity
                        elif month == 8:
                            m[7] += line.quantity
                        elif month == 9:
                            m[8] += line.quantity
                        elif month == 10:
                            m[9] += line.quantity
                        elif month == 11:
                            m[10] += line.quantity
                        else:
                            m[11] += line.quantity
            record.m1 = m[0]
            record.m2 = m[1]
            record.m3 = m[2]
            record.m4 = m[3]
            record.m5 = m[4]
            record.m6 = m[5]
            record.m7 = m[6]
            record.m8 = m[7]
            record.m9 = m[8]
            record.m10 = m[9]
            record.m11 = m[10]
            record.m12 = m[11]
            # record.total_amount_year = sum(m)
