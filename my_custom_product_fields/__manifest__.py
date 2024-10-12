{
    'name': 'Custom Product Fields',
    'version': '1.0',
    'category': 'Product',
    'summary': 'Add custom fields to product template',
    'description': 'This module adds new fields (Direct Link, Article Number, EAN, Short Description, Long Description) to product.template.',
    'author': 'M Jamshaid +923006868234',
    'depends': ['base', 'product'],
    'data': [
        'views/product_template_view.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
