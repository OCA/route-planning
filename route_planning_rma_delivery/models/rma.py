# Copyright 2025 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Rma(models.Model):
    _inherit = "rma"

    reception_carrier_delivery_type = fields.Selection(
        related="reception_carrier_id.delivery_type",
        string="Reception carrier delivery type",
    )
    carrier_delivery_type = fields.Selection(
        related="carrier_id.delivery_type", string="Carrier delivery type"
    )
