from odoo import api, models, fields

class SubcontractOrderLine(models.Model):
    _name = "subcontract.order.line"
    _description = "Subcontract Order Line"

    subcontract_order_id = fields.Many2one('subcontract.order', string="Subcontract Order", required=True, ondelete='cascade')
    service_product_id = fields.Many2one('product.product', string="Dịch vụ gia công", required=True)
    product_id = fields.Many2one('product.product', string="Sản phâm")
    uom_id = fields.Many2one('uom.uom', string="Đơn vị tính")
    quantity = fields.Float(string="Số lượng", default=1.0)
    price_unit = fields.Float(string="Đơn giá")
    subtotal = fields.Monetary(string='Thành tiền', compute='_compute_subtotal', store=True)
    currency_id = fields.Many2one(related='subcontract_order_id.currency_id', store=True)

    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.price_unit