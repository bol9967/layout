# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class product_product(models.Model):
    _inherit = 'product.product'

    brand_id = fields.Many2one('product.brand', 'Brand')
