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
