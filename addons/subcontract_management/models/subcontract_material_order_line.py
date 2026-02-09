from odoo import api, models, fields


class SubcontractMaterialOrderLine(models.Model):
    _name = "subcontract.material.order.line"
    _description = "Subcontract Material Order Line"

    subcontract_material_order_id = fields.Many2one('subcontract.material.order', string="Đơn cấp NVL", required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product',string="Nguyên vật liệu",required=True)
    uom_id = fields.Many2one('uom.uom',string="Đơn vị tính",related='product_id.uom_id',store=True,readonly=False)
    quantity = fields.Float(string="Số lượng",default=1.0)
    price_unit = fields.Monetary(string="Đơn giá")
    currency_id = fields.Many2one(related='subcontract_material_order_id.currency_id',store=True)
    subtotal = fields.Monetary(
        string="Thành tiền",
        compute="_compute_subtotal",
        store=True
    )

    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.price_unit
