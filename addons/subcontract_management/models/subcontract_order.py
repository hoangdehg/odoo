from odoo import models, fields

class SubcontractOrder(models.Model):
    _name = "subcontract.order"
    _description = "Subcontract Order"

    name = fields.Char(string="Order Reference", required=True)
    state = fields.Selection([('draft', 'Nháp'), ('confirmed', 'Đơn gia công'), ('waiting_tpmh', 'Chờ TPMH duyệt')
                              ,('waiting_cfo', 'Chờ GĐTC duyệt'),
                              ('waiting_ceo', 'Chờ TGĐ duyệt'),
                              ('rejected', 'Từ chối'),
                              ('cancelled', 'Hủy'),
                              ('done', 'Hoàn thành')], string="Trạng Thái", default='draft')
    partner_id = fields.Many2one('res.partner', string="Đơn vị gia công")
    user_id = fields.Many2one('res.users', string="Người tạo", default=lambda self: self.env.user)
    '''order_date = fields.Date(string="Order Date", default=fields.Date.context_today)
    material_ids = fields.One2many('subcontract.material', 'order_id', string="Materials")'''