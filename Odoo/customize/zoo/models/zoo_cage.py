from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError 

class ZooCage(models.Model):
  _name = "zoo.cage"
  _description = "Animal's Cage"

  name = fields.Char('Cage Name', required=True)
  code = fields.Char('Cage Code', required=True)
  length = fields.Float("Cage's Length (m)", required=True)
  width = fields.Float("Cage's Width (m)", required=True)
  height = fields.Float("Cage's Height (m)", required=True)
  description = fields.Text('Description')