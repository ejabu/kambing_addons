{
  'name': 'Kambing',
  'author': 'Reza',
  'version': '0.1',
  'depends': [
    'website',
  ],
  'data': [
    'security/role.xml',
    'security/ir.model.access.csv',
    
    'views/_menu_item.xml',
    'views/nota_jual.xml',
    'views/nota_jual_line.xml',
    'views/pihak_pembeli.xml',
    'views/barang_dagang.xml',
    'views/barang_kategori.xml',
    'web_views/barang.xml',
    'web_views/barang_all.xml',
  ],
  'qweb': [
    # 'static/src/xml/nama_widget.xml',
  ],
  'sequence': 1,
  'auto_install': False,
  'installable': True,
  'application': True,
  'category': '- Arkademy Part 1',
  'summary': 'Catat Penjualan Kambing',
  'license': 'OPL-1',
  'website': 'https://www.arkana.co.id/',
  'description': '-'
}