# Copyright 2026 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ReturnPickingLine(models.TransientModel):
    _inherit = "stock.return.picking.line"

    def _prepare_rma_vals(self):
        vals = super()._prepare_rma_vals()
        route_area = self.wizard_id.reception_route_area_id
        if route_area:
            vals["reception_route_area_id"] = route_area.id
            vals["location_id"] = route_area.location_id.id
        return vals


class ReturnPicking(models.TransientModel):
    _inherit = "stock.return.picking"

    can_use_route_area = fields.Boolean(
        compute="_compute_can_use_route_area",
    )
    reception_route_area_id = fields.Many2one(
        comodel_name="route.area",
        string="Reception route area",
    )

    @api.depends("rma_operation_id")
    def _compute_can_use_route_area(self):
        for item in self:
            item.can_use_route_area = (
                item.rma_operation_id._can_use_route_area()
                if item.rma_operation_id
                else False
            )

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        if "picking_id" in res and "reception_route_area_id" in fields:
            picking = self.env["stock.picking"].browse(res.get("picking_id"))
            res["reception_route_area_id"] = picking.route_area_id.id
        return res
