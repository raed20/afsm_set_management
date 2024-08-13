# Copyright 2015 Anybox S.A.S
# Copyright 2016-2020 Camptocamp SA
# @author Simone Orsi <simahawk@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import _, api, exceptions, fields, models


class SaleProductSetWizard(models.TransientModel):
    _name = "sale.product.set.wizard"
    _description = "Wizard model to add product set into a quotation"

    order_id = fields.Many2one(
        "sale.order",
        "Sale Order",
        required=True,
        default=lambda self: self.env.context.get("active_id")
        if self.env.context.get("active_model") == "sale.order"
        else None,
        ondelete="cascade",
    )
    set_id = fields.Many2one('product.set', string='Product Set', required=True)
    partner_id = fields.Many2one(related="order_id.partner_id", ondelete="cascade")
    skip_existing_products = fields.Boolean(
        default=False,
        help="Enable this to not add new lines "
        "for products already included in SO lines.",
    )

    def add_set(self):
        """Add product set, multiplied by quantity in sale order line"""

        order_lines = self._prepare_order_lines()
        if order_lines:
            self.order_id.write({"order_line": order_lines})
        return order_lines

    def _prepare_order_lines(self):
        """Prepare the order lines to be added to the sale order."""
        max_sequence = self._get_max_sequence()
        order_lines = []
        for set_line in self._get_lines():
            values = self.prepare_sale_order_line_data(set_line, max_sequence)
            order_lines.append((0, 0, values))
            max_sequence += 1
        return order_lines

    def _get_max_sequence(self):
        """Get the maximum sequence number of the existing order lines."""
        max_sequence = 0
        if self.order_id.order_line:
            max_sequence = max(line.sequence for line in self.order_id.order_line)
        return max_sequence

    def _get_lines(self):
        """Get the product set lines to be added, skipping existing products if requested."""

        so_product_ids = self.order_id.order_line.mapped("product_id").ids
        for set_line in self.set_id.lines_ids:
            if not self.skip_existing_products or set_line.product_id.id not in so_product_ids:
                yield set_line

    def prepare_sale_order_line_data(self, set_line, max_sequence=0):
        """Prepare the sale order line data for a given product set line."""
        self.ensure_one()
        line_values = set_line.prepare_sale_order_line_values(
            self.order_id, set_line ,max_sequence
        )
        if not line_values.get('name'):
            line_values['name'] = set_line.name

        if set_line.display_type:
            line_values.update({"display_type": set_line.display_type})

        return line_values

