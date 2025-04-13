from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
#import requests
import logging
_logger = logging.getLogger(__name__)

class ZooCreaturePlus(models.Model):
  _name="zoo.creature"
  _inherit="zoo.creature"
  _description="Extends zoo creature model"

  name = fields.Char('Creature')
  description = fields.Text('Description')
  creature_ids = fields.One2many(comodel_name='zoo.animal', inverse_name='creature_id', string='Animal ID')
  total_animals = fields.Integer(string='Total Animal', compute='_compute_total_animals')

  @api.depends('creature_ids')
  def _compute_total_animals(self):
    for i in self:
      i.total_animals = len(i.creature_ids)

  def get_animal_names(self):
    animal_names = []
    for i in self:
      for animal in i.creature_ids:
        animal_names.append(animal.name)
    return animal_names



  