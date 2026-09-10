# Copyright 2026 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ReturnPickingLine(models.TransientModel):
    _inherit = "stock.return.picking.line"

    def _prepare_rma_vals(self):
        vals = super()._prepare_rma_vals()
        carrier = self.wizard_id.reception_carrier_id
        if carrier and carrier.delivery_type != "route_planning":
            vals["reception_route_area_id"] = False
        return vals


class ReturnPicking(models.TransientModel):
    _inherit = "stock.return.picking"

    reception_carrier_delivery_type = fields.Selection(
        related="reception_carrier_id.delivery_type"
    )
