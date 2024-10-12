from odoo import fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    direct_link = fields.Char(string='Direct Link')
    article_number = fields.Char(string='Article Number')
    ean = fields.Char(string='EAN')
    long_description = fields.Html(string='Long Description')
