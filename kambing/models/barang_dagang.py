from odoo import models, fields, api
from PIL import Image
from odoo.tools import image


import io
import PIL
from PIL import Image
import base64

class BarangDagang(models.Model):
    _name = 'barang.dagang'

    name = fields.Char(string='Nama Barang')
    bobot = fields.Char(string='Bobot')

    website_published = fields.Boolean("Web Published", default=True)

    image = fields.Binary(string='Image', attachment=True,)
    image_web_string = fields.Char('Image Web String', compute="_get_image", store=True,)
    image_medium = fields.Binary('Medium', compute="_get_image", store=True, attachment=True)
    image_thumb = fields.Binary('Thumbnail', compute="_get_image", store=True, attachment=True)

    image_size = fields.Char(string='Image Size', compute="_get_image", store=True,)
    image_medium_size = fields.Char(string='Image Medium Size', compute="_get_image", store=True,)
    image_thumb_size = fields.Char(string='Image Thumb Size', compute="_get_image", store=True,)

    def recalc_images_size(self):
        # for doc in self.search([]):
        for doc in self:
            if doc.image:
                imgdata = base64.b64decode(doc.image)
                im = Image.open(io.BytesIO(imgdata))
                width, height = im.size
                doc.image_size = "{}x{}".format(width, height)


                
                imgdata = base64.b64decode(doc.image_medium)
                im = Image.open(io.BytesIO(imgdata))
                width, height = im.size
                doc.image_medium_size = "{}x{}".format(width, height)

                imgdata = base64.b64decode(doc.image_thumb)
                im = Image.open(io.BytesIO(imgdata))
                width, height = im.size
                doc.image_thumb_size = "{}x{}".format(width, height)
            else:
                doc.image_size = "256x256"
                doc.image_medium_size = "256x256"
                doc.image_thumb_size = "256x256"

    def reupload_images(self):

        # for doc in self.search([('image', '!=', False)]):
        for doc in self.search([]):
            if doc.image:
                imgdata = base64.b64decode(doc.image)
                img = Image.open(io.BytesIO(imgdata))

                basewidth = 800
                wpercent = (basewidth/float(img.size[0]))
                hsize = int((float(img.size[1])*float(wpercent)))
                
                new_img = img.resize((basewidth,hsize), Image.ANTIALIAS)
                buffered = io.BytesIO()
                new_img.save(buffered, format="PNG")
                new_img_str = base64.b64encode(buffered.getvalue())

                doc.image_thumb = new_img_str


                basewidth = 1200
                wpercent = (basewidth/float(img.size[0]))
                hsize = int((float(img.size[1])*float(wpercent)))
                
                new_img = img.resize((basewidth,hsize), Image.ANTIALIAS)
                buffered = io.BytesIO()
                new_img.save(buffered, format="PNG")
                new_img_str = base64.b64encode(buffered.getvalue())

                doc.image_medium = new_img_str

            doc.recalc_images_size()



    @api.depends('image')
    def _get_image(self):
        for doc in self:
            if doc.image:
                imgdata = base64.b64decode(doc.image)
                img = Image.open(io.BytesIO(imgdata))

                width, height = img.size
                doc.image_size = "{}x{}".format(width, height)

                basewidth = 800
                wpercent = (basewidth/float(img.size[0]))
                hsize = int((float(img.size[1])*float(wpercent)))
                
                new_img = img.resize((basewidth,hsize), Image.ANTIALIAS)
                width, height = new_img.size
                doc.image_thumb_size = "{}x{}".format(width, height)
                buffered = io.BytesIO()
                new_img.save(buffered, format="PNG")
                new_img_str = base64.b64encode(buffered.getvalue())

                doc.image_thumb = new_img_str


                basewidth = 1200
                wpercent = (basewidth/float(img.size[0]))
                hsize = int((float(img.size[1])*float(wpercent)))
                
                new_img = img.resize((basewidth,hsize), Image.ANTIALIAS)
                width, height = new_img.size
                doc.image_medium_size = "{}x{}".format(width, height)
                buffered = io.BytesIO()
                new_img.save(buffered, format="PNG")
                new_img_str = base64.b64encode(buffered.getvalue())

                doc.image_medium = new_img_str
                # doc.image_web_string = "data:image/png;base64," + doc.image_medium.decode("utf-8")
            else:
                doc.image_medium = False
                doc.image_thumb = False
                doc.image_web_string = False

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
            