# Copyright 2026 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _can_add_to_route(self):
        condition = super()._can_add_to_route()
        rma_receiver = fields.first(self.move_ids.rma_receiver_ids)
        if rma_receiver:
            delivery_moves = rma_receiver.delivery_move_ids
            return bool(
                condition
                and rma_receiver.operation_id
                and rma_receiver.operation_id._can_use_route_area()
                and (
                    not delivery_moves
                    or (
                        delivery_moves
                        and all(
                            m.state in ("assigned", "done", "cancel")
                            for m in delivery_moves
                        )
                        and any(
                            m.state not in ("draft", "waiting", "cancel")
                            for m in delivery_moves
                        )
                    )
                )
            )
        return condition
