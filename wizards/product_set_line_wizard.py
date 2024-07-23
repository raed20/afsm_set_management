from odoo import models, fields, api

class ProductSetLineWizard(models.TransientModel):
    _name = 'product.set.line.wizard'
    _description = 'Product Set Line Wizard'

    product_id = fields.Many2one('product.product', string='Product', required=True)
    set_id = fields.Many2one('product.set', string='Product Set', readonly=True)

    @api.model
    def default_get(self, fields):
        res = super(ProductSetLineWizard, self).default_get(fields)
        res.update({'set_id': self.env.context.get('default_set_id')})
        return res

    def action_add_product(self):
        self.ensure_one()
        if self.product_id:
            self.env['product.set.line'].create({
                'set_id': self.set_id.id,
                'product_id': self.product_id.id,
                'quantity': 1,  # Default quantity, can be modified
                'unit_id': self.product_id.uom_id.id,
                'reference_product_set_line': self.product_id.default_code or '',
                'set_name':False,
            })
        return {'type': 'ir.actions.act_window_close'}