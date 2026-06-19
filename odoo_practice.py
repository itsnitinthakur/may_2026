
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

class SaleOrderExtension(models.Model):
    _inherit = 'sale.order'      # no _name — modifies sale.order itself
    
    custom_note = fields.Text(string='Custom Note')



subtotal = fields.Float(compute='_compute_subtotal', store=True)

@api.depends('qty', 'price_unit')
def _compute_subtotal(self):
    for rec in self:
        rec.subtotal = rec.qty * rec.price_unit


@api.onchange('partner_id')
def _onchange_partner(self):
    if self.partner_id:
        self.payment_term_id = self.partner_id.property_payment_term_id


@api.constrains('amount')
def _check_amount(self):
    for rec in self:
        if rec.amount < 0:
            raise ValidationError("Amount cannot be negative.")

@api.model
def create(self, vals):
    vals['name'] = self.env['ir.sequence'].next_by_code('my.sequence')
    return super().create(vals)

# search — returns a recordset
orders = self.env['sale.order'].search([('state', '=', 'sale')])

# search with limit and order
orders = self.env['sale.order'].search(
    [('partner_id', '=', partner.id)],
    limit=10,
    order='date_order desc'
)

# search_read — returns list of dicts, one DB call, faster
orders = self.env['sale.order'].search_read(
    domain=[('state', '=', 'sale')],
    fields=['name', 'amount_total', 'partner_id'],
)

# browse — when you already have IDs
order = self.env['sale.order'].browse(42)