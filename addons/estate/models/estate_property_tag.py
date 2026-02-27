from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"

    name = fields.Char(required=True)
    _sql_constraints = [('check_name', 'UNIQUE(name)', 'The name of the tag must be unique.')]
    
