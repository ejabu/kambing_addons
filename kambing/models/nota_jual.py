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

    marketing_id = fields.Many2one(
        comodel_name='pihak.marketing',
        string='Marketing'
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



    jalan = fields.Char(string='Jalan')
    rt = fields.Char(string='RT')
    rw = fields.Char(string='RW')
    no_rumah = fields.Char(string='No Rumah')
    kelurahan = fields.Char(string='Kelurahan')
    kecamatan = fields.Char(string='Kecamatan')
    provinsi= fields.Char(string='Provinsi / Kabupaten')
    kode_pos= fields.Char(string='Kode Pos')
    penjelasan_alamat= fields.Text(string='Penjelasan Alamat')


    # attachment_ids = fields.One2many('ir.attachment', 'res_id', domain=[('res_model', '=', 'nota.jual')], string='Attachments')
    attachment_ids = fields.Many2many('ir.attachment', 'email_template_attachment_rel', 'email_template_id',
                                      'attachment_id', 'Attachments',
                                      help="You may attach files to this template, to be added to all "
                                           "emails created from this template")