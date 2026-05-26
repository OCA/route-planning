# Copyright 2026 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class RmaRmaWizard(models.TransientModel):
    _inherit = "rma.rma.wizard"

    delivery_type = fields.Selection(related="reception_carrier_id.delivery_type")

    @api.onchange("reception_carrier_id")
    def _onchange_reception_carrier_id(self):
        if self.reception_carrier_id.delivery_type != "route_planning":
            self.reception_route_area_id = False
