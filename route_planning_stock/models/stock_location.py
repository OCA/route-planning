# Copyright 2026 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockLocation(models.Model):
    _inherit = "stock.location"

    route_area_ids = fields.One2many(
        comodel_name="route.area",
        inverse_name="location_id",
        string="Route Areas",
    )

    def _is_outgoing(self):
        condition = super()._is_outgoing()
        # It is important to define an additional context to avoid side effects
        # for example confirmed SO:
        # OUT1: Done
        # OUT2: Pending
        # Return OUT1 + done
        # Cancel OUT2
        # Cancel SO + confirm again
        if self.env.context.get("route_planning_force_outgoing"):
            condition = condition or bool(self.route_area_ids)
        return condition
