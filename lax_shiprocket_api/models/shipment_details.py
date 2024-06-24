from odoo import models, fields, api, _


class ShiprocketShipmentDetails(models.Model):
    _name = 'lax.shipment.details'
    _description = "Shiprocket shipment details"

    shiprocket_shipment_id = fields.Char(string="Shiprocket Shipment ID")

