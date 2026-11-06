# Copyright 2025 Tecnativa - Carlos Lopez
# Copyright 2025 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _get_route_area(self):
        if self.move_orig_ids and any(
            p.route_area_id for p in self.move_orig_ids.picking_id
        ):
            return self.move_orig_ids.picking_id.route_area_id
        return self.env["route.area"]

    def _get_new_picking_values(self):
        values = super()._get_new_picking_values()
        route_area = self._get_route_area()
        if route_area:
            values["route_area_id"] = route_area.id
        return values

    def _assign_picking_post_process(self, new=False):
        res = super()._assign_picking_post_process(new=new)
        if new:
            route_area_pickings = self.picking_id.filtered(lambda x: x.route_area_id)
            if route_area_pickings:
                route_area_pickings._find_auto_route()
        return res

    def _set_locations_from_record_route_area(self):
        """This method will be extended by other modules to apply the appropriate
        changes to the location of the linked picking moves.
        This method is called from a picking when the route area changes.
        """
        return

    def _get_stock_move_vals_from_record_route_area(self, location):
        """This method will be extended by other modules to apply the appropriate
        changes of the linked picking moves.
        """
        self.ensure_one()
        rule = self.rule_id
        vals = {}
        if not location or not rule:
            return vals
        procurement_group = self.env["procurement.group"]
        rule_values = {
            "route_ids": self.route_ids,
            "product_packaging_id": self.product_packaging_id,
            "warehouse_id": (
                self.warehouse_id or self.picking_id.picking_type_id.warehouse_id
            ),
        }
        if rule.action == "push":
            new_rule = procurement_group._get_push_rule(
                self.product_id, location, rule_values
            )
        else:
            new_rule = procurement_group._get_rule(
                self.product_id, location, rule_values
            )
        if not new_rule:
            return vals
        vals["rule_id"] = new_rule.id
        vals["location_id"] = new_rule.location_src_id.id
        if rule.action == "push":
            location_dest = new_rule.location_dest_id
            if self.location_final_id and self.location_final_id._child_of(
                location_dest
            ):
                location_dest = self.location_final_id
            vals["location_dest_id"] = location_dest.id
        elif new_rule.location_dest_from_rule or not self._get_route_area():
            vals["location_dest_id"] = new_rule.location_dest_id.id
        return vals
