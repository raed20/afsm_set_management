from odoo import models, fields, api
from odoo.exceptions import UserError


class ProductSetSelectWizard(models.TransientModel):
    _name = 'product.set.select.wizard'
    _description = 'Product Set Select Wizard'

    set_id = fields.Many2one('product.set', string='Product Set', required=True)

    from odoo.exceptions import UserError

    def action_add_product_set(self):
        self.ensure_one()  # Ensure that only one record is processed at a time

        selected_set = self.set_id
        current_set_id = self.env.context.get('active_id')

        if not selected_set or not current_set_id:
            raise UserError("Selected set or current set ID is missing.")

        current_product_set = self.env['product.set'].browse(current_set_id)

        if not current_product_set:
            raise UserError("Current product set not found.")

        # Get the IDs of products already in the current set
        existing_product_ids = current_product_set.lines_ids.mapped('product_id.id')

        # Collect products from the selected set that are already in the current set
        duplicate_products = selected_set.lines_ids.filtered(lambda l: l.product_id.id in existing_product_ids)

        if duplicate_products:
            # Create a list of product names that are duplicates
            duplicate_product_names = ', '.join(duplicate_products.mapped('product_id.name'))
            raise UserError(f"The following products are already in the current set: {duplicate_product_names}")

        # Add products from the selected set to the current set if they are not duplicates
        for line in selected_set.lines_ids:
            if line.product_id.id not in existing_product_ids:
                self.env['product.set.line'].create({
                    'set_id': current_product_set.id,
                    'product_id': line.product_id.id,
                    'quantity': line.quantity,
                    'unit_id': line.unit_id.id,
                    'reference_product_set_line': line.reference_product_set_line,
                    'set_name': selected_set.name,
                })

        return {'type': 'ir.actions.act_window_close'}
