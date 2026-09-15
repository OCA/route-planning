# Copyright 2026 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrderRmaWizard(models.TransientModel):
    _inherit = "sale.order.rma.wizard"

    reception_carrier_delivery_type = fields.Selection(
        related="reception_carrier_id.delivery_type"
    )
    reception_route_area_id = fields.Many2one(
        compute="_compute_reception_route_area_id",
        store=True,
        readonly=False,
    )

    @api.depends("can_use_route_area")
    def _compute_available_reception_carrier_ids(self):
        # If the selected operation does not allow route_area, we remove the carriers
        # of type route_planning
        res = super()._compute_available_reception_carrier_ids()
        for item in self.filtered(lambda x: not x.can_use_route_area):
            carriers = item.available_reception_carrier_ids.filtered(
                lambda x: x.delivery_type != "route_planning"
            )
            item.available_reception_carrier_ids = carriers
        return res

    @api.depends("reception_carrier_id")
    def _compute_reception_route_area_id(self):
        for item in self:
            if item.reception_carrier_delivery_type != "route_planning":
                # Set reception_route_area_id empty so that the data is consistent
                # with reception_carrier_id
                item.reception_route_area_id = False
