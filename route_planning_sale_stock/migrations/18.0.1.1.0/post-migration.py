# Copyright 2026 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    """We need to amend all moves (except returns) linked to sales that have an
    incorrect final location (no final location or a route area location).
    It is important that the data is consistent to avoid unintended consequences
    (incorrect quantities) if the order is cancelled and then confirmed again.
    """
    moves = env["stock.move"].search(
        [
            ("sale_line_id", "!=", False),
            ("origin_returned_move_id", "!=", False),
            "|",
            ("location_final_id", "=", False),
            ("location_final_id.route_area_ids", "!=", False),
        ]
    )
    for move in moves:
        location_final = move.sale_line_id._get_location_final()
        if not location_final:
            continue
        move.write({"location_final_id": location_final.id})
