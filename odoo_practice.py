
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

# create
new_order = self.env['sale.order'].create({
    'partner_id': partner.id,
    'state': 'draft',
})

# write — updates all records in the recordset
orders.write({'state': 'cancel'})

# unlink — deletes
orders.unlink()

# Many2many commands
record.write({
    'tag_ids': [
        (4, tag_id),           # link existing record
        (3, tag_id),           # unlink (remove) existing record
        (6, 0, [id1, id2]),    # replace entire set with these IDs
        (5,),                  # remove all links
    ]
})

# One2many commands
record.write({
    'line_ids': [
        (0, 0, {'name': 'New Line', 'qty': 2}),  # create new child
        (1, line_id, {'qty': 5}),                 # update existing child
        (2, line_id),                             # delete child
    ]
})

# filtered — like Python filter
confirmed = orders.filtered(lambda o: o.state == 'sale')

# mapped — like Python map, returns list or recordset
amounts = orders.mapped('amount_total')          # [100.0, 250.0, ...]
partners = orders.mapped('partner_id')           # returns partner recordset

# sorted
orders_sorted = orders.sorted(key=lambda o: o.date_order, reverse=True)

<record id="view_my_model_form" model="ir.ui.view">
    <field name="name">my.model.form</field>
    <field name="model">sale.order.custom</field>
    <field name="arch" type="xml">
        <form string="Custom Order">
            <header>
                <button name="action_confirm" string="Confirm"
                        type="object" class="btn-primary"/>
                <field name="state" widget="statusbar"/>
            </header>
            <sheet>
                <group>
                    <field name="name"/>
                    <field name="partner_id"/>
                    <field name="date"/>
                </group>
                <notebook>
                    <page string="Order Lines">
                        <field name="line_ids">
                            <tree editable="bottom">
                                <field name="product_id"/>
                                <field name="qty"/>
                                <field name="price_unit"/>
                                <field name="subtotal"/>
                            </tree>
                        </field>
                    </page>
                </notebook>
            </sheet>
        </form>
    </field>
</record>

<record id="view_sale_order_form_inherit" model="ir.ui.view">
    <field name="name">sale.order.form.inherit.custom</field>
    <field name="model">sale.order</field>
    <field name="inherit_id" ref="sale.view_order_form"/>  <!-- parent view -->
    <field name="arch" type="xml">

        <!-- Add a field after an existing field -->
        <xpath expr="//field[@name='partner_id']" position="after">
            <field name="custom_note"/>
        </xpath>

        <!-- Replace a field -->
        <xpath expr="//field[@name='validity_date']" position="replace">
            <field name="custom_date"/>
        </xpath>

        <!-- Add inside a group -->
        <xpath expr="//group[@name='sale_info']" position="inside">
            <field name="custom_flag"/>
        </xpath>

    </field>
</record>

<template id="report_invoice_custom">
    <t t-call="web.html_container">
        <t t-foreach="docs" t-as="doc">
            <div class="page">
                <h2>Invoice: <t t-field="doc.name"/></h2>
                <table>
                    <t t-foreach="doc.invoice_line_ids" t-as="line">
                        <tr>
                            <td><t t-field="line.product_id.name"/></td>
                            <!-- This is what the invoice image module does -->
                            <td>
                                <t t-if="line.product_id.image_128">
                                    <img t-att-src="image_data_uri(line.product_id.image_128)"/>
                                </t>
                            </td>
                            <td><t t-field="line.price_subtotal"/></td>
                        </tr>
                    </t>
                </table>
            </div>
        </t>
    </t>
</template>


from odoo import http
from odoo.http import request
import json

class MyWebhookController(http.Controller):

    @http.route('/webhook/incoming', type='json',
                auth='public', methods=['POST'], csrf=False)
    def handle_webhook(self):
        payload = request.jsonrequest          # parsed JSON body
        order_ref = payload.get('order_ref')
        status = payload.get('status')

        # Find the Odoo record and update it
        order = request.env['sale.order'].sudo().search(
            [('name', '=', order_ref)], limit=1
        )
        if order:
            order.write({'custom_status': status})
            return {'success': True}
        return {'success': False, 'error': 'Order not found'}
    
    my_module/
└── migrations/
    └── 16.0.1.1.0/
        ├── pre-migrate.py    # runs BEFORE the ORM updates the DB
        └── post-migrate.py   # runs AFTER the ORM updates

# pre-migrate.py — example: rename a column before ORM sees it
def migrate(cr, version):
    cr.execute("""
        ALTER TABLE sale_order_custom
        RENAME COLUMN old_field_name TO new_field_name;
    """)

# post-migrate.py — example: populate a new field with default data
def migrate(cr, version):
    cr.execute("""
        UPDATE sale_order_custom
        SET status_flag = 'active'
        WHERE status_flag IS NULL;
    """)

    