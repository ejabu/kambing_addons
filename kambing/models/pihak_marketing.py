from odoo import models, fields, api, _
from odoo.exceptions import UserError

class PihakMarketing(models.Model):
    _name = 'pihak.marketing'

    name = fields.Char(string='Nama Marketing')
    phone = fields.Char(string='No Handphone')
    kota = fields.Char(string='Nama Kota')
