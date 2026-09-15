# Copyright 2026 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class RmaOperation(models.Model):
    _inherit = "rma.operation"

    def _can_use_route_area(self):
        """A method that allows us to determine whether an operation will enable the
        selection of route area in the corresponding RMA and wizards.
        We have already implemented the logic to exclude route areas if the operation
        is a refund.
        """
        self.ensure_one()
        return not self.action_create_refund
