# Copyright 2026 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    """We need to amend all moves (except returns) linked to RMAs that have an
    incorrect final location (no final location or a route area location).
    """
    for rma in env["rma"].search([("delivery_move_ids", "!=", False)]):
        moves = rma._get_delivery_moves()  # To get all the linked moves
        moves_to_change = moves.filtered(
            lambda x: not x.origin_returned_move_id
            and (not x.location_final_id or x.location_final_id.route_area_ids)
        )
        if not moves_to_change:
            continue
        location_final = rma._get_location_final()
        if not location_final:
            continue
        moves_to_change.write({"location_final_id": location_final.id})
