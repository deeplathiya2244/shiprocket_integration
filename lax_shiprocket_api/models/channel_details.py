from odoo import models, fields, api, _


class ShiprocketChannel(models.Model):
    _name = 'lax.shiprocket.channel'
    _description = "Shiprocket channel details"

    # shiprocket_id = fields.Many2one('lax.shiprocket.api', string="shiprocket id")
    shiprocket_channel_id = fields.Char(string="Shiprocket Channel ID")
    gmail = fields.Char(string="Gmail")
    name = fields.Char(string="Channel Name")
    status = fields.Char(string="Channel Status")
