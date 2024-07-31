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

        # Get existing product IDs, sections, and notes in the current set
        existing_product_ids = current_product_set.lines_ids.filtered(
            lambda l: l.display_type != 'line_section' and l.display_type != 'line_note').mapped('product_id.id')
        existing_lines = current_product_set.lines_ids

        # Collect products, sections, and notes from the selected set that are already in the current set
        duplicate_products = selected_set.lines_ids.filtered(lambda
                                                                 l: l.display_type != 'line_section' and l.display_type != 'line_note' and l.product_id.id in existing_product_ids)

        if duplicate_products:
            # Create a list of product names that are duplicates
            duplicate_product_names = ', '.join(duplicate_products.mapped('product_id.name'))
            raise UserError(f"The following products are already in the current set: {duplicate_product_names}")

        # Add products, sections, and notes from the selected set to the current set if they are not duplicates
        for line in selected_set.lines_ids.sorted(key=lambda l: l.sequence):
            if line.display_type == 'line_section' or line.display_type == 'line_note':
                # Create sections or notes directly, preserving the sequence
                self.env['product.set.line'].create({
                    'set_id': current_product_set.id,
                    'display_type': line.display_type,
                    'sequence': line.sequence,
                    'name': line.name,
                    'set_name': selected_set.name,
                })
            elif line.product_id.id not in existing_product_ids:
                # Create new product lines, preserving the sequence
                self.env['product.set.line'].create({
                    'set_id': current_product_set.id,
                    'product_id': line.product_id.id,
                    'quantity': line.quantity,
                    'unit_id': line.unit_id.id,
                    'reference_product_set_line': line.reference_product_set_line,
                    'set_name': selected_set.name,
                    'sequence': line.sequence,  # Preserve the sequence
                })

        return {'type': 'ir.actions.act_window_close'}
