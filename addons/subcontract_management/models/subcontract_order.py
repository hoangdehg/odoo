from odoo import api, models, fields

class SubcontractOrder(models.Model):
    _name = "subcontract.order"
    _description = "Subcontract Order"

    name = fields.Char(string="Order Reference", required=True, copy = False, default=lambda self: "New")
    state = fields.Selection([('draft', 'Nháp'), ('confirmed', 'Đơn gia công'), ('waiting_tpmh', 'Chờ TPMH duyệt')
                              ,('waiting_cfo', 'Chờ GĐTC duyệt'),
                              ('waiting_ceo', 'Chờ TGĐ duyệt'),
                              ('rejected', 'Từ chối'),
                              ('cancelled', 'Hủy'),
                              ('done', 'Hoàn thành')], string="Trạng Thái", default='draft', tracking=True)
    partner_id = fields.Many2one('res.partner', string="Đơn vị gia công", required=True)
    user_id = fields.Many2one('res.users', string="Người phụ trách", default=lambda self: self.env.user, required=True)
    finished_warehouse_id = fields.Many2one('stock.warehouse', string="Kho thành phẩm")
    material_warehouse_id = fields.Many2one('stock.warehouse', string="Kho NVL")
    date_order = fields.Date(string="Ngày tạo", default=fields.Date.context_today)
    expected_completion_date = fields.Date(string="Ngày hoàn thành dự kiến")
    finished_date = fields.Date(string="Ngày hoàn thành", readonly=True)
    amount_total = fields.Monetary(string="Tổng tiền", compute='_compute_amount_total',store=True)
    line_ids = fields.One2many(
        'subcontract.order.line',
        'subcontract_order_id',
        string='Chi tiết'
    )
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id, required=True)

    @api.depends('line_ids.subtotal')
    def _compute_amount_total(self):
        for record in self:
            record.amount_total = sum(record.line_ids.mapped('subtotal'))