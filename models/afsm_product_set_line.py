from odoo import models, fields, api

from odoo17.odoo.exceptions import ValidationError


class ProductSetLine(models.Model):
    _name = 'product.set.line'
    _description = 'Product Set Line'

    # Default methods

    # Fields declaration

    set_id = fields.Many2one('product.set', string='Product Set', required=False, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', required=True , ondelete='cascade')
    quantity = fields.Float(string='Quantity')
    unit_id = fields.Many2one('uom.uom', string='Unit of Measure', required=True)
    reference_product_set_line = fields.Char(string='Reference')
    set_name = fields.Char(string='Product Set Name')  # Add this field

    # -------------------------------------------------------------------------
    # COMPUTE METHODS
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # SELECTION METHODS
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # Constrains METHODS
    # -------------------------------------------------------------------------
    @api.constrains('set_id', 'product_id')
    def _check_unique_product_set(self):
        for record in self:
            # Search for existing records with the same set_id and product_id
            existing_lines = self.search([
                ('set_id', '=', record.set_id.id),
                ('product_id', '=', record.product_id.id),
                ('id', '!=', record.id)  # Exclude the current record to handle update cases
            ])
            if existing_lines:
                raise ValidationError(f"The product '{record.product_id.name}' is already in the current set.")
    # -------------------------------------------------------------------------
    # ONCHANGE METHODS
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # CRUD METHODS
    # -------------------------------------------------------------------------

    # CRUD methods (and name_get, name_search, ...) overrides

    # -------------------------------------------------------------------------
    # Action METHODS
    # -------------------------------------------------------------------------

