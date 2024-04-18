from odoo import models, fields, api, _


class ShiprocketChannel(models.Model):
    _name = 'lax.shiprocket.channel'
    _description = "Shiprocket channel details"

    gmail = fields.Many2one('lax.shiprocket.api', string="Gmail")
    shiprocket_channel_id = fields.Char(string="Channel ID")
    name = fields.Char(string="Channel Name")
    status = fields.Char(string="Channel Status")

