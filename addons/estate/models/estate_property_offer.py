from odoo import api, models, fields
from datetime import timedelta
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float(string = "Price")
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(string="deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    status_offer = fields.Selection(selection=[('accepted', 'Accepted'), ('rejected', 'Rejected')],copy = False, string="Status")

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                create_date = record.create_date.date()
            else:
                create_date = fields.Date.today()
            record.date_deadline = create_date + timedelta(days=record.validity)
    
    def _inverse_date_deadline(self):
        for record in self:
            if not record.date_deadline:
                record.validity = 0
            if record.create_date:
                create_date = record.create_date.date()
            else:
                create_date = fields.Date.today()
            record.validity = (record.date_deadline - create_date).days
    
    def action_accept(self):
        for record in self:
            record.status_offer = 'accepted'
            property_record = record.property_id
            if property_record.buyer_id:
                raise UserError("This property already has a buyer.")
            property_record.buyer_id = record.partner_id
            property_record.selling_price= record.price 
        return True
    def action_reject(self):
        for record in self:
            record.status_offer = 'rejected'
        return True