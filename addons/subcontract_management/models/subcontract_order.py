from datetime import timedelta
from odoo import api, models, fields

class SubcontractOrder(models.Model):
    _name = "subcontract.order"
    _description = "Subcontract Order"

    name = fields.Char(string="Order Reference", required=True, copy = False, default=lambda self: "New")
    state = fields.Selection([('draft', 'Mới'), ('confirmed', 'Đơn chế tác'), ('deposit', 'Chờ đặt cọc'),
                              ('design', 'Chờ thiết kế'), ('delivery', 'Chờ giao hàng'),
                              ('done', 'Hoàn thành')], string="Trạng Thái", default='draft')

    partner_id = fields.Many2one('res.partner', string="Đơn vị gia công", required=True)
    user_id = fields.Many2one('res.users', string="Người phụ trách", default=lambda self: self.env.user, required=True)
    #finished_warehouse_id = fields.Many2one('stock.warehouse', string="Kho thành phẩm")
    #material_warehouse_id = fields.Many2one('stock.warehouse', string="Kho NVL")
    order_date = fields.Date(string="Ngày đặt hàng", default=fields.Date.context_today, required=True)
    expected_days = fields.Date(string="Số ngày dự kiến hoàn thành")
    expected_return_date = fields.Date(string="Ngày trả hàng dự kiến", compute='_compute_expected_return_date', store=True)
    #finished_date = fields.Date(string="Ngày hoàn thành", readonly=True)
    amount_total = fields.Monetary(string="Tổng tiền", compute='_compute_amount_total',store=True)
    line_ids = fields.One2many(
        'subcontract.order.line',
        'subcontract_order_id',
        string='Chi tiết'
    )
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id, required=True)

    deposit_amount = fields.Monetary(string="Số tiền đặt cọc", default=0.0)
    amount_remaining = fields.Monetary( string="Số tiền còn lại phải thanh toán", compute="_compute_amount_remaining", store=True)
    partner_phone = fields.Char(string="Số điện thoại")
    partner_address = fields.Char(string="Địa chỉ")
    receiver_is_customer = fields.Boolean(string="Người nhận là khách hàng", default=True)

    receiver_name = fields.Char(string="Người nhận")
    receiver_phone = fields.Char(string="Số điện thoại")
    receiver_address = fields.Char(string="Địa chỉ")

    @api.onchange('receiver_is_customer', 'partner_id')
    def _onchange_receiver_is_customer(self):
        for record in self:
            if record.receiver_is_customer and record.partner_id:
                record.receiver_name = record.partner_id.name
                record.receiver_phone = record.partner_id.phone
                record.receiver_address = record.partner_id.contact_address


    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        for record in self:
            if record.partner_id:
                record.partner_phone = record.partner_id.phone
                record.partner_address = record.partner_id.contact_address
            else:
                record.partner_phone = False
                record.partner_address = False


    @api.depends('amount_total', 'deposit_amount')
    def _compute_amount_remaining(self):
        for record in self:
            record.amount_remaining = record.amount_total - record.deposit_amount

    @api.depends('line_ids.subtotal')
    def _compute_amount_total(self):
        for record in self:
            record.amount_total = sum(record.line_ids.mapped('subtotal'))

    @api.depends('order_date', 'expected_days')
    def _compute_expected_return_date(self):
        for record in self:
            if record.order_date and record.expected_days:
                record.expected_return_date = record.order_date + timedelta(days=record.expected_days)
            else:
                record.expected_return_date = False
