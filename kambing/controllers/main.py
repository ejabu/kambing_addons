from odoo import http
from odoo.addons.http_routing.models.ir_http import unslug
from odoo.http import request
# from odoo.addons.web.controllers.main import Home
from odoo.addons.website.controllers.main import Home

class MyHome(Home):

    @http.route(['/', '/index', '/home'], type='http', website=True, auth='public')
    def index(self, **kw):
        search_query = []
        order = "name"
        barang_ids = request.env['barang.dagang'].sudo().search(search_query, order=order)
        barang_ids = barang_ids.sorted(key=lambda r: r.state_index)
        values = {
            'barang_ids': barang_ids,
        }
        return request.render("kambing.barang_dagang_all_temp", values)



    def get_prev_next_vals(self, data, current_value):
        current_index = data.index(current_value)
        prev_index = current_index - 1
        next_index = current_index + 1
        last_index = len(data) - 1
        if prev_index == -1:
            prev_index = last_index
        if next_index > last_index:
            next_index = 0
        return data[prev_index], data[next_index]

    @http.route(['/barang/<barang_id>'], type='http', auth="public", website=True)
    def barang_detail(self, barang_id, **post):
        search_query = []
        _, barang_id = unslug(barang_id)
        if barang_id:
            partner_sudo = request.env['barang.dagang'].sudo().browse(barang_id)
            available_ids = request.env['barang.dagang'].sudo().search(search_query).ids

            prev_value, next_value = self.get_prev_next_vals(available_ids, barang_id)
            if partner_sudo.exists():
                values = {
                    'main_object': partner_sudo,
                    "prev_url": '/barang/' + str(prev_value),
                    "next_url": '/barang/' + str(next_value),
                    'partner': partner_sudo,
                    'edit_page': False
                }
                return request.render("kambing.barang_dagang_template", values)
        return request.not_found()

    @http.route([
        '/<kategori_name>',
    ], type='http', auth="public", website=True)
    def barang_all(self, kategori_name=False, **post):
        search_query = []
        if kategori_name:
            print('Flag Here')
            kategori_search_query = [('slug_url', '=', kategori_name.lower())]
            kategori_id = request.env['barang.kategori'].sudo().search(kategori_search_query, limit=1)
            if kategori_id:
                search_query.append(('kategori_id', '=', kategori_id.id))
            else:
                values = {
                    'barang_ids': [],
                }
                return request.render("kambing.barang_dagang_all_temp", values)
        order = "name"
        barang_ids = request.env['barang.dagang'].sudo().search(search_query, order=order)
        barang_ids = barang_ids.sorted(key=lambda r: r.state_index)
        values = {
            'barang_ids': barang_ids,
        }
        return request.render("kambing.barang_dagang_all_temp", values)
