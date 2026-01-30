from odoo import models, fields
from odoo.tools.date_utils import relativedelta

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char(required=True)
    description = fields.Text()
    
