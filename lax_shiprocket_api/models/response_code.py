from odoo import models, fields, api, _


class ShiprocketResponseCode(models.Model):
    _name = "shiprocket.response.code"
    _description = "Shiprocket response code data file"

    code = fields.Char(string="Code")
    name = fields.Char(string="Name")
    description = fields.Text(string="Description")
