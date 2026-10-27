# Copyright 2026 Tecnativa - Carlos Lopez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.tools import float_compare


class ChooseDeliveryCarrier(models.TransientModel):
    _inherit = "choose.delivery.carrier"

    route_area_id = fields.Many2one(
        "route.area",
        compute="_compute_route_area_id",
        store=True,
        readonly=False,
    )

    @api.depends("partner_id", "company_id", "delivery_type", "order_id")
    def _compute_route_area_id(self):
        self.route_area_id = False
        for wizard in self.filtered(lambda w: w.delivery_type == "route_planning"):
            company = wizard.company_id or self.env.company
            partner = wizard.partner_id.with_company(company)
            wizard.route_area_id = self.order_id.route_area_id or partner.route_area_id

    def button_confirm(self):
        order = self.order_id
        if order.carrier_id == self.carrier_id and self.route_area_id:
            # If the carrier is the same and the route area is being changed,
            # we will not call super() if there are billed lines
            delivery_lines = order.order_line.filtered("is_delivery")
            delivery_lines_price = sum(delivery_lines.mapped("price_unit"))
            delivery_lines_to_delete = delivery_lines.filtered(
                lambda x: x.qty_invoiced == 0
            )
            dp = self.env["decimal.precision"].precision_get("Product Price")
            if (
                not delivery_lines_to_delete
                and float_compare(
                    delivery_lines_price, self.delivery_price, precision_digits=dp
                )
                == 0
            ):
                order.write({"route_area_id": self.route_area_id.id})
                return
        res = super().button_confirm()
        order.write({"route_area_id": self.route_area_id.id})
        return res
