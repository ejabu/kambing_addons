from odoo import models, fields, api
from PIL import Image
from odoo.tools import image

class BarangDagang(models.Model):
    _name = 'barang.dagang'

    name = fields.Char(string='Nama Barang')
    bobot = fields.Char(string='Bobot')

    website_published = fields.Boolean("Web Published", default=True)

    image = fields.Binary(string='Image', attachment=True,)
    image_web_string = fields.Char('Image Web String', compute="_get_image", store=True,)
    image_medium = fields.Binary('Medium', compute="_get_image", store=True, attachment=True)
    image_thumb = fields.Binary('Thumbnail', compute="_get_image", store=True, attachment=True)

    @api.depends('image')
    def _get_image(self):
        for record in self:
            if record.image:
                record.image_medium = image.crop_image(record.image, type='top', ratio=(4, 3), size=(500, 400))
                record.image_thumb = image.crop_image(record.image, type='top', ratio=(4, 3), size=(200, 200))
                record.image_web_string = "data:image/png;base64," + record.image_medium.decode("utf-8") 
            else:
                record.image_medium = False
                record.image_thumb = False
                record.image_web_string = False

    @api.depends('state')
    def _get_state_index(self):
        for record in self:
            if record.state == 'tersedia':
                record.state_index = 1
            elif record.state == 'reservasi':
                record.state_index = 2
            elif record.state == 'terjual':
                record.state_index = 3
            else:
                record.state_index = 99

    kategori_id = fields.Many2one(
        comodel_name='barang.kategori',
        string='Kategori'
        )
    state = fields.Selection([
            ('tersedia', 'Tersedia'),
            ('reservasi', 'Reservasi'),
            ('terjual', 'Terjual'),
        ], string='Status', default='tersedia')
    
    state_index = fields.Integer("State Index", compute="_get_state_index")
    recheck_state = fields.Selection(
        selection=[
            ('tersedia', 'Tersedia'),
            ('reservasi', 'Reservasi'),
            ('terjual', 'Terjual'),
        ], 
        string='Status',
        compute="set_recheck_state",
        )

    harga = fields.Float(string='Harga')

    nota_line_ids = fields.One2many(
        comodel_name='nota.jual.line',
        inverse_name='barang_id',
        string='Riwayat Jual',
        )
    
    
    def set_recheck_state(self):
        for doc in self:
            kumpulan_state = [line.nota_id.state for line in doc.nota_line_ids]
            if "lunas" in kumpulan_state:
                self.recheck_state = "terjual"
                
            elif "dp" in kumpulan_state:
                self.recheck_state = "terjual"

            elif "waiting" in kumpulan_state:
                self.recheck_state = "reservasi"
            