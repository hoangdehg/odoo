from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.date_utils import relativedelta
from datetime import timedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default= lambda self: fields.Date.context_today(self)+ relativedelta(months=3))
    expected_price = fields.Float()
    selling_price = fields.Float(readonly=False, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
        string='Garden Orientation',)
    property_type_id = fields.Many2one(
        'estate.property.type',
        string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")
    active = fields.Boolean(default=True)
    state = fields.Selection(selection=[
        ('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'), ('canceled', 'Canceled')], required=True, default='new', copy = False)
    total_area = fields.Integer(compute='_compute_total_area', string="Total Area")
    best_price = fields.Float(compute='_compute_best_price', string="Best Offer")
    status = fields.Selection(selection=[('sold', 'Sold'), ('canceled', 'Canceled')], string="Status")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + (record.garden_area or 0)
    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0.0
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False
    
    def action_sold(self):
        for record in self:
            if record.status == False:
                record.status = 'sold'
            elif record.status == 'canceled':
                raise UserError("Canceled properties cannot be sold.")
        return True
    def action_cancel(self):
        for record in self:
            if record.status == False:
                record.status = 'canceled'
            elif record.status == 'sold':
                raise UserError("Sold properties cannot be canceled.")
        return True