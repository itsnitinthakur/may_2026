
#my_module/
#├── __init__.py
#├── __manifest__.py
#├── models/
#│   ├── __init__.py
#│   └── my_model.py
#├── views/
#│   └── my_views.xml
#├── security/
#│   └── ir.model.access.csv
#├── data/
#│   └── default_data.xml
#└── controllers/
#    ├── __init__.py
#    └── main.py. 

{
    'name': 'My Custom Module',
    'version': '16.0.1.0.0',
    'depends': ['sale', 'stock'],        # modules yours builds on
    'data': [
        'security/ir.model.access.csv',
        'views/my_views.xml',
    ],
    'installable': True,
    'application': False,
}

from odoo import models, fields, api

class SaleOrderCustom(models.Model):
    _name = 'sale.order.custom'       # creates a new DB table
    _description = 'Custom Sale Order'

    name = fields.Char(string='Name', required=True)
    date = fields.Date(string='Date')
    amount = fields.Float(string='Amount')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
    ], default='draft')
    partner_id = fields.Many2one('res.partner', string='Customer')
    line_ids = fields.One2many('sale.order.line', 'order_id', string='Lines')
    tag_ids = fields.Many2many('res.partner.category', string='Tags')



    class MyInheritedModel(models.Model):
    _name = 'my.model'           # new table in DB
    _inherit = 'sale.order'      # copies fields from sale.order