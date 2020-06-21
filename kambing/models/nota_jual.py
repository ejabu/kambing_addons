from odoo import models, fields, api

class NotaJual(models.Model):
    _name = 'nota.jual'

    name = fields.Char(string='Nota')

    state = fields.Selection([
            ('draft', 'Draft'),
            ('waiting', 'Waiting'),
            ('dp', 'DP'),
            ('lunas', 'Lunas'),
            ('cancel', 'Cancel'),
        ], string='Status', default='draft')
    
    pembeli_id = fields.Many2one(
        comodel_name='pihak.pembeli',
        string='Pembeli'
        )

    phone = fields.Char(string='No Handphone', related='pembeli_id.phone')
    kota = fields.Char(string='Nama Kota', related='pembeli_id.kota')

    tanggal_pesan = fields.Date(
        string='Tanggal Pesan', 
        default=fields.Date.today(),
    )

    line_ids = fields.One2many(
        comodel_name='nota.jual.line',
        inverse_name='nota_id',
        string='Riwayat Jual',
        )