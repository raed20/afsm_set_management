from collections import Counter

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProductSet(models.Model):
    _name = 'product.set'
    _description = 'Product Set'

    # Default methods

    # Fields declaration
    name = fields.Char(string='Name', required=True)
    lines_ids = fields.One2many('product.set.line', 'set_id', string='Lines')
    reference_set = fields.Char(string='Reference')
    quantity = fields.Float(string='Quantity')


    # -------------------------------------------------------------------------
    # COMPUTE METHODS
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # SELECTION METHODS
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # Constrains METHODS
    # -------------------------------------------------------------------------
    _sql_constraints = [
        ('product_set_unique', 'unique(reference_set)', ' reference set exists ')
    ]


    # ONCHANGE METHODS
    # -------------------------------------------------------------------------
    @api.onchange('quantity')
    def _onchange_quantity(self):
        if not self._origin.quantity:
            # If the set is new, we can't calculate a ratio, so we just skip the adjustment.
            return

        # Calculate the ratio of the new quantity to the old quantity
        ratio = self.quantity / self._origin.quantity if self._origin.quantity else 1

        for line in self.lines_ids:
            line.quantity = line.quantity * ratio
    # -------------------------------------------------------------------------
    # CRUD METHODS
    # -------------------------------------------------------------------------

    # CRUD methods (and name_get, name_search, ...) overrides

    # -------------------------------------------------------------------------
    # Action METHODS
    # -------------------------------------------------------------------------


    def action_add_product_set(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Select Product Set',
            'view_mode': 'form',
            'res_model': 'product.set.select.wizard',
            'target': 'new'
        }




