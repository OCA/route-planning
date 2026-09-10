# Copyright 2025-2026 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Route Planning RMA Sale Delivery Integration",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "Tecnativa,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/route-planning",
    "depends": [
        "route_planning_rma_delivery",
        "route_planning_rma_sale",
        "rma_sale_delivery",
    ],
    "data": ["wizard/sale_order_rma_wizard_views.xml"],
    "installable": True,
    "auto_install": True,
    "maintainers": ["victoralmau"],
}
