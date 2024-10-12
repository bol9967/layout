# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _


class ProductBrand(models.Model):
    _inherit = 'product.template'

    brand_id = fields.Many2one('product.brand', 'Brand')

    @api.model_create_multi
    def create(self, vals_list):
        brand = super(ProductBrand, self).create(vals_list)
        for vals in vals_list:
            if vals.get('brand_id'):
                brand_brw = self.env['product.brand'].browse(vals.get('brand_id'))
                brand_brw.write({'product_ids': [(4, brand.id)]})
        return brand

    def write(self, value):
        brand = super(ProductBrand, self).write(value)
        if value.get('brand_id'):
            brand_brw = self.env['product.brand'].browse(value.get('brand_id'))
            brand_brw.write({'product_ids': [(4, self.id)]})
            products = self.env['product.product'].search([('product_tmpl_id', '=', self.id)])
            product_ids = self.env['product.template'].search([('brand_id', '=', brand_brw.id)])
            brand_ids = self.env['product.brand'].search([])
            for brand in brand_ids:
                for product_id in brand.product_ids:
                    if product_id in product_ids and product_id.brand_id != brand:
                        brand.write({
                            'product_ids': [(3, product_id.id)]
                        })
            for product_variants in products:
                product_variants.update({'brand_id': self.brand_id.id})
        return brand

    def _prepare_variant_values(self, combination):
        variant_dict = super()._prepare_variant_values(combination)
        variant_dict['brand_id'] = self.brand_id.id
        return variant_dict
