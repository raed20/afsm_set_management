from odoo import models, fields, api
from odoo.exceptions import UserError

from odoo17.odoo.exceptions import ValidationError


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
        self.ensure_one()  # Ensure that only one record is processed at a time

        # Ensure product_id and set_id are valid
        if not self.product_id or not self.set_id:
            raise ValidationError("Product or Set information is missing.")

        try:
            # Create a new product set line
            self.env['product.set.line'].create({
                'set_id': self.set_id.id,
                'product_id': self.product_id.id,
                'quantity': 1,
                'unit_id': self.product_id.uom_id.id,
                'reference_product_set_line': self.product_id.default_code or '',
                'set_name': False,
            })
        except ValidationError as e:
            # Handle the validation error
            raise UserError(str(e))
        except Exception as e:
            # Handle other potential exceptions
            raise UserError(f"An unexpected error occurred: {str(e)}")

        # Close the window after the operation
        return {'type': 'ir.actions.act_window_close'}
