from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

class ZooDomainCategory(models.Model):
    _name = "zoo.dummy.category"
    _description = "Zoo Dummy Category"
    _parent_name = "parent_category_id"
    _parent_store = True

    name = fields.Char('Name', required=True)
    parent_category_id = fields.Many2one(comodel_name='zoo.dummy.category', string='Parent Category', index=True, ondelete='cascade')
    parent_path = fields.Char(index=True)
    child_category_ids = fields.One2many(comodel_name='zoo.dummy.category', inverse_name='parent_category_id', string='Child Categories')

    dummy_ids = fields.One2many(comodel_name='zoo.dummy', inverse_name='category_id', string='Dummies')

class ZooDomain(models.Model):
    _name = "zoo.dummy"
    _description = "Zoo Dummy Data"

    name = fields.Char('Name', required=True)
    a = fields.Float('A')
    b = fields.Float('B')
    c = fields.Float('C')

    date = fields.Date('Date')
    state = fields.Selection([
        ('first', 'First State'),
        ('second', 'Second State'),
        ('third', 'Third State')
    ], string='State', default='first', required=False)
    dtime = fields.Datetime('Date Time')
    is_online = fields.Boolean('Is Online', default=True)

    category_id = fields.Many2one(comodel_name='zoo.dummy.category', string='Category')
    category_name = fields.Char('Category Name', related='category_id.name')