from odoo import models, fields, api, _
from odoo.exceptions import UserError

class BarangKategori(models.Model):
    _name = 'barang.kategori'

    name = fields.Char(string='Nama Kategori')
    slug_url = fields.Char(string='Slug Website')
    kategori_id = fields.Many2one(
        comodel_name='barang.kategori',
        string='Parent Kategori'
        )