from odoo import models, fields, api

class ProductSetSelectWizard(models.TransientModel):
    _name = 'product.set.select.wizard'
    _description = 'Product Set Select Wizard'

    set_id = fields.Many2one('product.set', string='Product Set', required=True)

    def action_add_product_set(self):
        self.ensure_one()
        selected_set = self.set_id
        current_set = self.env.context.get('active_id')
        if selected_set:
            current_product_set = self.env['product.set'].browse(current_set)
            for line in selected_set.lines_ids:
                self.env['product.set.line'].create({
                    'set_id': current_product_set.id,
                    'product_id': line.product_id.id,
                    'quantity': line.quantity,
                    'unit_id': line.unit_id.id,
                    'reference_product_set_line': line.reference_product_set_line,
                })
        return {'type': 'ir.actions.act_window_close'}
