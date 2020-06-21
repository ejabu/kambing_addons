from odoo import models, fields, api, _
from odoo.exceptions import UserError

class NotaJualLine(models.Model):
    _name = 'nota.jual.line'

    barang_id = fields.Many2one(
        comodel_name='barang.dagang',
        string='Barang'
        )
    name = fields.Char(string='Keterangan')

    tanggal_kirim = fields.Date(
        string='Tanggal Kirim', 
        default=fields.Date.today(),
    )
    nota_id = fields.Many2one(
        comodel_name='nota.jual',
        string='Related Nota'
        )
    tanggal_pesan = fields.Date(
        string='Tanggal Pesan', 
        default=fields.Date.today(),
        related="nota_id.tanggal_pesan",
    )
    kategori_id = fields.Many2one(
        comodel_name='barang.kategori',
        string='Kategori',
        related='barang_id.kategori_id',
        )