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
        string='No. Nota Jual',
        ondelete='cascade',
        )
    
    currency_id = fields.Many2one(
        'res.currency', 
        string='Currency', 
        compute='get_currency',
        )

    def get_currency(self):
        for doc in self:
            doc.currency_id = self.env.user.company_id.currency_id

    harga = fields.Float(
        string='Harga',
        related="barang_id.harga",
        )
    marketing_id = fields.Many2one(
        comodel_name='pihak.marketing',
        string='Marketing',
        related="nota_id.marketing_id",
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