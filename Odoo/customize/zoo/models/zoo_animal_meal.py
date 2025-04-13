from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

class ZooAnimalMeal(models.Model):
  _name = "zoo.animal.meal"
  _description = "Animal's Meal"

  name = fields.Many2one(comodel_name='Product.product', string='Meal Name', required=True)
  volume = fields.Float("Volume (kg)", required=True)
  meal = fields.Selection([("breakfast", "Breakfast"), ("lunch", "Lunch"), ("dinner", "Dinner"), ("supper", "Supper")], string="Meal Type", required=True)