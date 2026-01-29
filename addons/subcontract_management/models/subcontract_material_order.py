from odoo import api, models, fields

class SubcontractMaterialOrder(models.Model):
    _name = "subcontract.material.order"
    _description = "Subcontract Material Order"

    name = fields.Char(string="Order Reference", required=True, default="New")
    partner_id = fields.Many2one('res.partner', string="Đơn vị gia công")
    user_id = fields.Many2one('res.users', string="Người phụ trách", default=lambda self: self.env.user)
    currency_id = fields.Many2one(
    'res.currency',
    default=lambda self: self.env.company.currency_id,
    required=True
)
    line_ids = fields.One2many(
    'subcontract.material.order.line',
    'subcontract_material_order_id',
    string="Chi tiết nguyên vật liệu"
)
    