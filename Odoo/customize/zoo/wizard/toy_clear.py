from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

class ToyClearWizard(models.TransientModel):
  _name = "zoo.toy.clear.wizard"
  _description = "Clear all toys"

  def clear_all_toys(self):
    ids = self.env.context['active_ids']
    zoo_animals = self.env['zoo.animal'].browse(ids)

    data = {
      "toy_ids": [(5, 0, 0)]
    }
    zoo_animals.write(data)