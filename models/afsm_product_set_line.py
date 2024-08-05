from odoo import models, fields, api

from odoo.exceptions import ValidationError


class ProductSetLine(models.Model):
    _name = 'product.set.line'
    _description = 'Product Set Line'

    # Default methods

    # Fields declaration

    set_id = fields.Many2one('product.set', string='Product Set', required=False, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', ondelete='cascade')
    quantity = fields.Float(string='Quantity')
    unit_id = fields.Many2one('uom.uom', string='Unit of Measure')
    reference_product_set_line = fields.Char(string='Reference', compute='_compute_reference_product_set_line',
                                             store=True)
    set_name = fields.Char(string='Product Set Name')  # Add this field
    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note")])
    sequence = fields.Integer(string='Sequence', default=10)
    name = fields.Char(string='Description')

    # -------------------------------------------------------------------------
    # COMPUTE METHODS
    # -------------------------------------------------------------------------

    @api.depends('product_id')
    def _compute_reference_product_set_line(self):
        for line in self:
            if line.product_id:
                line.reference_product_set_line = line.product_id.default_code or ''
                line.unit_id = line.product_id.uom_id.id
                line.quantity = 1.00

    # -------------------------------------------------------------------------
    # SELECTION METHODS
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # Constrains METHODS
    # -------------------------------------------------------------------------

    # Constrain method using the custom function
    @api.constrains('set_id', 'product_id')
    def _check_product_unique_in_set(self):
        for record in self:
            if record.set_id and record.product_id:
                existing_lines = self.search([
                    ('set_id', '=', record.set_id.id),
                    ('product_id', '=', record.product_id.id),
                    ('id', '!=', record.id)
                ])
                if existing_lines:
                    raise ValidationError(f"The product '{record.product_id.name}' is already in the current set.")

    @api.constrains('product_id', 'quantity', 'unit_id', 'display_type')
    def _check_fields(self):
        for record in self:
            if record.display_type not in ['line_section', 'line_note']:
                if not record.product_id:
                    continue  # Skip records where product_id is not set
                else:
                    if not record.quantity:
                        raise ValidationError("The Quantity field is required.")
                    if not record.unit_id:
                        raise ValidationError("The Unit of Measure field is required.")

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
