from odoo import http
from odoo.addons.http_routing.models.ir_http import unslug
from odoo.http import request


import math
from odoo.addons.website.controllers.main import Home

PAGELIMIT = 20

class MyHome(Home):

    @http.route(['/', '/<kategori_name>'], type='http', website=True, auth='public')
    def index(self, kategori_name=False, **kwargs):
        search_query = []
        slug = '/'
        if kategori_name:
            kategori_search_query = [('slug_url', '=', kategori_name.lower())]
            kategori_id = request.env['barang.kategori'].sudo().search(kategori_search_query, limit=1)
            if kategori_id:
                search_query.append(('kategori_id', '=', kategori_id.id))
                slug = slug + kategori_name

        page_number = kwargs.get('page', '1')
        if page_number.isdigit():
            page_number = int(page_number)
            if page_number < 1:
                page_number = 1
            if page_number > 1000:
                page_number = 1000
        else:
            page_number = 1
        offset = (page_number - 1) * PAGELIMIT
        BarangDagang = request.env['barang.dagang'].sudo()
        barang_ids = BarangDagang.search(search_query, offset=offset, limit=PAGELIMIT)
        barang_ids = barang_ids.sorted(key=lambda r: r.state_index)

        item_count = len(barang_ids)
        total_item_count = BarangDagang.search_count(search_query)

        max_page_index = math.ceil(total_item_count / PAGELIMIT)

        page_displays = []
        for oix in range(5):
            oix = page_number + oix - 2
            if oix > 0 and oix <= max_page_index:
                page_displays.append(oix)

        if 1 not in page_displays:
            if len(page_displays) > 4:
                page_displays[0] = 1
            else:
                page_displays.insert(0, 1)
        if max_page_index not in page_displays:
            if len(page_displays) > 4:
                page_displays[len(page_displays)-1] = max_page_index
            else:
                page_displays.append(max_page_index)
        if item_count < PAGELIMIT:
            next_page_index = 0
        else:
            next_page_index = page_number + 1
        
        if page_number > 1:
            prev_page_index = page_number - 1
        else:
            prev_page_index = 0

        values = {
            'barang_ids': barang_ids,
            'next_page_index': next_page_index,
            'prev_page_index': prev_page_index,
            'slug': slug,
            'page_displays': page_displays,
            'page_number': page_number,
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

    # @http.route([
    #     '/<kategori_name>',
    # ], type='http', auth="public", website=True)
    # def barang_all(self, kategori_name=False, **post):
    #     search_query = []
    #     if kategori_name:
    #         print('Flag Here')
    #         kategori_search_query = [('slug_url', '=', kategori_name.lower())]
    #         kategori_id = request.env['barang.kategori'].sudo().search(kategori_search_query, limit=1)
    #         if kategori_id:
    #             search_query.append(('kategori_id', '=', kategori_id.id))
    #         else:
    #             values = {
    #                 'barang_ids': [],
    #             }
    #             return request.render("kambing.barang_dagang_all_temp", values)
    #     order = "name"
    #     barang_ids = request.env['barang.dagang'].sudo().search(search_query, order=order)
    #     barang_ids = barang_ids.sorted(key=lambda r: r.state_index)
    #     values = {
    #         'barang_ids': barang_ids,
    #     }
    #     return request.render("kambing.barang_dagang_all_temp", values)
