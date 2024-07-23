from odoo import models, fields, api


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
    # _sql_constraints = [
    #     ('product_set_line_unique', 'unique(reference_product_set_line)', 'product set line reference exists ')
    # ]

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

