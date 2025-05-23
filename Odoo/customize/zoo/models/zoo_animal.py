# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

import datetime

class ZooAnimal(models.Model):
    _name = "zoo.animal"
    _description = "Animal in the zoo"

    name = fields.Char('Animal Name', required=True)    
    nickname = fields.Char('Nickname', required=False)
    information = fields.Text('Information (VI)')
    is_bought = fields.Boolean('Is Bought', default=False, help="Has this animal been bought before?")
    buy_price = fields.Float('Buy Price', required=False, help="Price of the animal when bought")

    description = fields.Text('Description')
    dob = fields.Date('DOB', required=False)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string='Gender', default='male', required=True)
    feed_time = fields.Datetime('Feed Time', copy=False)
    state = fields.Selection([('healthy', 'Healthy'), ('unhealthy', 'Unhealthy')], string="Status", readonly=True, tracking=True, default='healthy')
    is_alive = fields.Boolean('Is Alive', default=True)
    image = fields.Binary("Image", attachment=True, help="Animal Image")
    weight = fields.Float('Weight (kg)')
    weight_pound = fields.Float('Weight (pounds)')
    introduction = fields.Text('Introduction (EN)')

    age = fields.Integer('Pet Age', compute='_compute_age')    

    mother_id = fields.Many2one(comodel_name='zoo.animal', string='Mother', ondelete='set null') # ondelete: 'set null', 'restrict', 'cascade'
    mother_name = fields.Char('Mother Name', related='mother_id.name')
    female_children_ids = fields.One2many(comodel_name='zoo.animal', inverse_name='mother_id', string='Female Children')

    father_id = fields.Many2one(comodel_name='zoo.animal', string='Father', ondelete='set null') # ondelete: 'set null', 'restrict', 'cascade'
    father_name = fields.Char('Father Name', related='father_id.name')
    male_children_ids = fields.One2many(comodel_name='zoo.animal', inverse_name='father_id', string='Male Children')

    toy_ids = fields.Many2many(comodel_name='product.product', 
                                string="Toys", 
                                relation='animal_product_toy_rel',
                                column1='col_animal_id',
                                column2='col_product_id')

    creature_id = fields.Many2one(comodel_name='zoo.creature', string='Creature')

    doctor_id = fields.Many2one(comodel_name='res.partner',
                                string='Doctor',
                                relation='animal_partner_doctor_rel',
                                column1='col_animal_id',
                                column2='col_partner_id')
    cage_id = fields.Many2one(comodel_name='zoo.cage', string='Cage', ondelete='set null')

    number_of_children = fields.Integer(string='Number of Children', compute='_compute_number_of_children', store=True) 

    @api.depends('mother_id', 'father_id')
    def _compute_number_of_children(self):
        for i in self:
            children = self.search([('mother_id', '=', i.mother_id.id), ('father_id', '=', i.father_id.id)])
            i.number_of_children = len(children)
            if i.number_of_children < 0:
                raise ValidationError(_("Negative number of children!"))


    @api.depends('dob')
    def _compute_age(self):
        now = datetime.datetime.now()
        current_year = now.year
        for record in self:
            dob = record.dob
            if dob:
                dob_year = dob.year
                delta_year = current_year - dob_year
                if delta_year < 0:
                    raise ValidationError(_("Negative age: current year < DOB year!"))
                record.age = delta_year
            else:
                record.age = False
        pass

    @api.constrains('dob')
    def _check_dob(self):
        for record in self:
            if record.dob and record.dob.year < 1900:
                raise ValidationError(_("Invalid DOB!"))

    @api.onchange('weight')
    def _update_weight_pound(self):
        self.weight_pound = self.weight * 2.204623

    @api.onchange('weight_pound')
    def _update_weight_kg(self):
        self.weight = self.weight_pound / 2.204623

    @api.constrains('father_id', 'mother_id')
    def _check_mother_and_father(self):
        for record in self:
            if record.mother_id and record.father_id:
                if record.mother_id == record.father_id:
                    raise ValidationError(_("Mother and father cannot be the same animal!"))
            else:
                if record.id == record.mother_id or record.id == record.father_id:
                    raise ValidationError(_("Animal cannot be its own mother or father!"))
            
    @api.constrains('gender', 'female_children_ids', 'male_children_ids')
    def _check_gender(self):
        for record in self:
            if record.female_children_ids and record.male_children_ids:
                raise ValidationError(_("Cannot having female children and male children at the same time!"))
            if record.gender == "male" or "Male":
                if record.female_children_ids:
                    raise ValidationError(_("Male animal cannot have female children!"))
            else:
                if record.male_children_ids:
                    raise ValidationError(_("Female animal cannot have male children!"))
            
    def report_sickness(self):
        self.write({'state': 'unhealthy'})

    def recovered_health(self):
        self.write({'state': 'healthy'})

    def update_feed_time(self):
        self.write({'feed_time': fields.Datetime.now()})

        