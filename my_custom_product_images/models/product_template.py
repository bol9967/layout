from odoo import fields, models, api
import base64
import requests
from odoo.exceptions import UserError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    direct_link = fields.Char(string='Direct Link')
    article_number = fields.Char(string='Article Number')
    ean = fields.Char(string='EAN')
    long_description = fields.Html(string='Long Description')

    main_image = fields.Binary(string='Main Image')
    additional_image_1 = fields.Binary(string='Additional Image 1')
    additional_image_2 = fields.Binary(string='Additional Image 2')
    additional_image_3 = fields.Binary(string='Additional Image 3')
    additional_image_4 = fields.Binary(string='Additional Image 4')
    additional_image_5 = fields.Binary(string='Additional Image 5')
    additional_image_6 = fields.Binary(string='Additional Image 6')

    main_image_url = fields.Char(string='Main Image URL')
    additional_image_1_url = fields.Char(string='Additional Image 1 URL')
    additional_image_2_url = fields.Char(string='Additional Image 2 URL')
    additional_image_3_url = fields.Char(string='Additional Image 3 URL')
    additional_image_4_url = fields.Char(string='Additional Image 4 URL')
    additional_image_5_url = fields.Char(string='Additional Image 5 URL')
    additional_image_6_url = fields.Char(string='Additional Image 6 URL')

    @api.model
    def _get_image_from_url(self, url):
        """ Helper method to download image from URL and convert to base64 """
        if url:
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    return base64.b64encode(response.content)
                else:
                    raise UserError(f"Error downloading image: HTTP {response.status_code}")
            except Exception as e:
                raise UserError(f"Failed to download image from {url}: {str(e)}")
        return False

    @api.model
    def create(self, vals):
        """ Override create to handle image download when importing via CSV """
        if vals.get('main_image_url'):
            vals['main_image'] = self._get_image_from_url(vals['main_image_url'])
        
        for i in range(1, 7):
            url_field = f'additional_image_{i}_url'
            image_field = f'additional_image_{i}'
            if vals.get(url_field):
                vals[image_field] = self._get_image_from_url(vals[url_field])

        return super(ProductTemplate, self).create(vals)

    def write(self, vals):
        """ Override write to handle image download when importing via CSV """
        if vals.get('main_image_url'):
            vals['main_image'] = self._get_image_from_url(vals['main_image_url'])

        for i in range(1, 7):
            url_field = f'additional_image_{i}_url'
            image_field = f'additional_image_{i}'
            if vals.get(url_field):
                vals[image_field] = self._get_image_from_url(vals[url_field])

        return super(ProductTemplate, self).write(vals)

    @api.onchange('main_image_url', 'additional_image_1_url', 'additional_image_2_url',
                  'additional_image_3_url', 'additional_image_4_url', 'additional_image_5_url', 'additional_image_6_url')
    def _onchange_image_urls(self):
        """ Download and update image fields when URLs are set via form """
        if self.main_image_url:
            self.main_image = self._get_image_from_url(self.main_image_url)

        for i in range(1, 7):
            url_field = f'additional_image_{i}_url'
            image_field = f'additional_image_{i}'
            if getattr(self, url_field):
                setattr(self, image_field, self._get_image_from_url(getattr(self, url_field)))
