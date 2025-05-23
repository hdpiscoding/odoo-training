from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

#import logging _logger = logging.getLogger(__name__)

class ToyWizard(models.TransientModel):
  _name = "zoo.toy.add.wizard"
  _description = "Add toy"

  product_id = fields.Many2one(comodel_name='product.product', string='Toy', required=True)

  def add_toy(self):
    ids = self.env.context['active_ids']
    zoo_animals = self.env['zoo.animal'].browse(ids)

    data = {
      "toy_ids": [(4, self.product_id.id, 0)]
    }
    zoo_animals.write(data)