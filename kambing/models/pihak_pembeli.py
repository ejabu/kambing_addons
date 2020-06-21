from odoo import models, fields, api, _
from odoo.exceptions import UserError

class PihakPembeli(models.Model):
    _name = 'pihak.pembeli'

    name = fields.Char(string='Nama Pembeli')
    phone = fields.Char(string='No Handphone')
    kota = fields.Char(string='Nama Kota')


    ## Ge Default Name
    ## Reza - (Jakarta) - 08033303
    ## atau bikin related aja