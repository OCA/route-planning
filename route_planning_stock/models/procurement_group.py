# Copyright 2026 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, models


class ProcurementGroup(models.Model):
    _inherit = "procurement.group"

    @api.model
    def _get_rule(self, product_id, location_id, values):
        if values.get("route_area_location_id"):
            location_id = values.get("route_area_location_id")
        return super()._get_rule(product_id, location_id, values)
