# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import json
import http.client
import mimetypes
from codecs import encode


class ShiprocketAPI(models.Model):
    _name = 'lax.shiprocket.api'
    _description = "Shiprocket API Integration"

    name = fields.Char(string="Instance Name", required=True, copy=False, index=True)
    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    base_url = fields.Char(string="Base Url", default='apiv2.shiprocket.in')
    gmail = fields.Char(string="Gmail", store=True)
    password = fields.Char(string="Password", store=True)
    token = fields.Char(string="Token", readonly=True)
    status = fields.Selection([('draft', 'Draft'), ('done', 'Done')], string="Status", default="draft")
    order_ids = fields.One2many('sale.order', 'inherit_order_id', string="Order Ids")

    # Authentication
    # "POST"
    def generate_token(self):
        conn = http.client.HTTPSConnection(self.base_url)
        headers = {
            'Content-Type': 'application/json'
        }
        payload = json.dumps({
            "email": self.gmail,
            "password": self.password
        })
        conn.request("POST", "/v1/external/auth/login", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))
        data = json.loads(data)
        self.token = data['token']
        for key, value in data.items():
            print(f"{key}: {value}")
        print()

    # Create Or Update Order
    # "POST"
    def create_custom_order(self):
        conn = http.client.HTTPSConnection(self.base_url)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        payload = json.dumps({
            "order_id": "224-447",
            "order_date": "2024-02-24 11:11",
            "pickup_location": "TEST",
            "channel_id": "",
            "comment": "Reseller: M/s Goku",
            "billing_customer_name": "Naruto",
            "billing_last_name": "Uzumaki",
            "billing_address": "House 221B, Leaf Village",
            "billing_address_2": "Near Hokage House",
            "billing_city": "New Delhi",
            "billing_pincode": "110002",
            "billing_state": "Delhi",
            "billing_country": "India",
            "billing_email": "naruto@uzumaki.com",
            "billing_phone": "9876543210",
            "shipping_is_billing": True,
            "shipping_customer_name": "",
            "shipping_last_name": "",
            "shipping_address": "",
            "shipping_address_2": "",
            "shipping_city": "",
            "shipping_pincode": "",
            "shipping_country": "",
            "shipping_state": "",
            "shipping_email": "",
            "shipping_phone": "",
            "order_items": [
                {
                    "name": "Kunai",
                    "sku": "chakra123",
                    "units": 10,
                    "selling_price": "900",
                    "discount": "",
                    "tax": "",
                    "hsn": 441122
                }
            ],
            "payment_method": "Prepaid",
            "shipping_charges": 0,
            "giftwrap_charges": 0,
            "transaction_charges": 0,
            "total_discount": 0,
            "sub_total": 9000,
            "length": 10,
            "breadth": 15,
            "height": 20,
            "weight": 2.5
        })
        conn.request("POST", "/v1/external/orders/create/adhoc", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))
        str_data = json.loads(data)
        shipment_id = str_data['shipment_id']
        order_id = str_data['order_id']
        ord_id = self.env['sale.order'].search([('shiprocket_order_id', '=', order_id)])
        ship_id = self.env['lax.shipment.details'].search([('shiprocket_shipment_id', '=', shipment_id)])

    # "POST"
    def create_channel_specific_order(self):
        conn = http.client.HTTPSConnection(self.base_url)
        channel_id = self.env['lax.shiprocket.channel'].search([('gmail', '=', self.gmail)], limit=1)
        print("------->>>", channel_id.shiprocket_channel_id)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        payload = json.dumps({
            "order_id": "224-4779",
            "order_date": "2024-01-24 11:11",
            "pickup_location": "Test",
            "channel_id": channel_id.shiprocket_channel_id,
            "comment": "Reseller: M/s Goku",
            "billing_customer_name": "Naruto",
            "billing_last_name": "Uzumaki",
            "billing_address": "House 221B, Leaf Village",
            "billing_address_2": "Near Hokage House",
            "billing_city": "New Delhi",
            "billing_pincode": "110002",
            "billing_state": "Delhi",
            "billing_country": "India",
            "billing_email": "naruto@uzumaki.com",
            "billing_phone": "9876543210",
            "shipping_is_billing": True,
            "shipping_customer_name": "",
            "shipping_last_name": "",
            "shipping_address": "",
            "shipping_address_2": "",
            "shipping_city": "",
            "shipping_pincode": "",
            "shipping_country": "",
            "shipping_state": "",
            "shipping_email": "",
            "shipping_phone": "",
            "order_items": [
                {
                    "name": "Kunai",
                    "sku": "chakra123",
                    "units": 10,
                    "selling_price": "900",
                    "discount": "",
                    "tax": "",
                    "hsn": 441122
                }
            ],
            "payment_method": "Prepaid",
            "shipping_charges": 0,
            "giftwrap_charges": 0,
            "transaction_charges": 0,
            "total_discount": 0,
            "sub_total": 9000,
            "length": 10,
            "breadth": 15,
            "height": 20,
            "weight": 2.5
        })
        conn.request("POST", "/v1/external/orders/create", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # "PATCH"
    def update_pickup_location(self):
        conn = http.client.HTTPSConnection(self.base_url)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        payload = json.dumps({
            "order_id": [
                522677076
            ],
            "pickup_location": "Delhi",
            "pickup_code": "Test"
        })
        conn.request("PATCH", "/v1/external/orders/address/pickup", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # "POST"
    def update_customer_delivery_address(self):
        conn = http.client.HTTPSConnection(self.base_url)
        payload = json.dumps({
            "order_id": 16178831,
            "shipping_customer_name": "Majin Bu",
            "shipping_phone": "9988998899",
            "shipping_address": "Earth",
            "shipping_address_2": "",
            "shipping_city": "Pune",
            "shipping_state": "Maharashtra",
            "shipping_country": "India",
            "shipping_pincode": 110077
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        conn.request("POST", "/v1/external/orders/address/update", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # "POST"
    def update_order(self):
        conn = http.client.HTTPSConnection(self.base_url)
        payload = json.dumps({
            "order_id": "518935492",
            "order_date": "2024-03-05 09:46:44",
            "pickup_location": "Test",
            "channel_id": "",
            "comment": "",
            "reseller_name": "",
            "company_name": "My Flower Tree (P) LTD",
            "billing_customer_name": "DummyName",
            "billing_last_name": "",
            "billing_address": "Test Address",
            "billing_address_2": "",
            "billing_isd_code": "",
            "billing_city": "New delhi",
            "billing_pincode": "110030",
            "billing_state": "Delhi",
            "billing_country": "India",
            "billing_email": "mailto:support@gmail.com",
            "billing_phone": "8108102113",
            "billing_alternate_phone": "",
            "shipping_is_billing": True,
            "shipping_customer_name": "",
            "shipping_last_name": "",
            "shipping_address": "",
            "shipping_address_2": "",
            "shipping_city": "",
            "shipping_pincode": "",
            "shipping_country": "",
            "shipping_state": "",
            "shipping_email": "",
            "shipping_phone": "",
            "order_items": [
                {
                    "name": "Blue Tshirt 32 Size",
                    "sku": "Tshirt-Blue-32",
                    "units": "17",
                    "selling_price": 200,
                    "discount": "0",
                    "tax": "0",
                    "hsn": "4435"
                }
            ],
            "payment_method": "Prepaid",
            "shipping_charges": 0,
            "giftwrap_charges": 0,
            "transaction_charges": 0,
            "total_discount": 0,
            "sub_total": 3400,
            "length": 5,
            "breadth": 15,
            "height": 15,
            "weight": 1,
            "ewaybill_no": "",
            "customer_gstin": ""
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        conn.request("POST", "/v1/external/orders/update/adhoc", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # "POST"
    def cancel_an_order(self):
        conn = http.client.HTTPSConnection(self.base_url)
        payload = json.dumps({
            "ids": [
                16168898,
                16167171
            ]
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        conn.request("POST", "/v1/external/orders/cancel", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # "PATCH"
    def add_inventory_for_ordered_product(self):
        conn = http.client.HTTPSConnection(self.base_url)
        payload = json.dumps({
            "data": [
                {
                    "order_id": 14124005,
                    "order_product_id": 43737767570843,
                    "quantity": "1",
                    "action": "add"
                }
            ]
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        conn.request("PATCH", "/v1/external/orders/fulfill", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # "PATCH"
    def map_unmapped_products(self):
        conn = http.client.HTTPSConnection(self.base_url)
        payload = json.dumps({
            "data": [
                {
                    "order_id": 14303681,
                    "order_product_id": 16487731,
                    "master_sku": "delta123"
                }
            ]
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        conn.request("PATCH", "/v1/external/orders/mapping", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # POST
    def import_orders_in_bulk(self):
        conn = http.client.HTTPSConnection(self.base_url)
        dataList = []
        boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=file; filename={0}'.format('file')))

        fileTtype = mimetypes.guess_type('/path/to/file')[0] or 'application/octet-stream'
        dataList.append(encode('Content-Type: {}'.format(fileType)))
        dataList.append(encode(''))

        with open('/path/to/file', 'rb') as f:
            dataList.append(f.read())
        dataList.append(encode('--' + boundary + '--'))
        dataList.append(encode(''))
        body = b'\r\n'.join(dataList)
        payload = body
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token,
            'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
        }
        conn.request("POST", "/v1/external/orders/import", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # Couriers
    # "POST"
    def generate_awb_for_shipment(self):
        conn = http.client.HTTPSConnection(self.base_url)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        payload = json.dumps({
            "shipment_id": "520690807",
            "courier_id": "10"
        })
        conn.request("POST", "/v1/external/courier/assign/awb", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # "GET"
    def list_of_all_courier(self):
        conn = http.client.HTTPSConnection(self.base_url)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        payload = ''
        conn.request("GET", "/v1/external/courier/courierListWithCounts", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # "GET"
    def check_courier_serviceability(self):
        conn = http.client.HTTPSConnection(self.base_url)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        payload = json.dumps({
            "order_id": "522585096"
        })
        conn.request("GET", "/v1/external/courier/serviceability/", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # "POST"
    def request_for_shipment_pickup(self):
        conn = http.client.HTTPSConnection(self.base_url)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        payload = json.dumps({
            "shipment_id": [
                520690807
            ]
        })
        conn.request("POST", "/v1/external/courier/generate/pickup", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # Orders
    # "GET"
    def get_orders(self):
        conn = http.client.HTTPSConnection(self.base_url)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        payload = ''
        conn.request("GET", "/v1/external/orders", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # "GET"
    def get_specific_order(self):
        conn = http.client.HTTPSConnection(self.base_url)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        payload = ''
        conn.request("GET", "/v1/external/orders/show/522585096", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # "POST"
    def export_orders(self):
        conn = http.client.HTTPSConnection(self.base_url)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        payload = json.dumps({})
        conn.request("POST", "/v1/external/orders/export", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # Return Orders
    # "POST"
    def create_return_order(self):
        conn = http.client.HTTPSConnection(self.base_url)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        payload = json.dumps({
            "order_id": "r121579B09ap3o",
            "order_date": "2021-12-30",
            "channel_id": "27202",
            "pickup_customer_name": "iron man",
            "pickup_last_name": "",
            "company_name": "iorn pvt ltd",
            "pickup_address": "b 123",
            "pickup_address_2": "",
            "pickup_city": "Delhi",
            "pickup_state": "New Delhi",
            "pickup_country": "India",
            "pickup_pincode": 110030,
            "pickup_email": "deadpool@red.com",
            "pickup_phone": "9810363552",
            "pickup_isd_code": "91",
            "shipping_customer_name": "Jax",
            "shipping_last_name": "Doe",
            "shipping_address": "Castle",
            "shipping_address_2": "Bridge",
            "shipping_city": "ghaziabad",
            "shipping_country": "India",
            "shipping_pincode": 201005,
            "shipping_state": "Uttarpardesh",
            "shipping_email": "kumar.abhishek@shiprocket.com",
            "shipping_isd_code": "91",
            "shipping_phone": 8888888888,
            "order_items": [
                {
                    "name": "shoes",
                    "qc_enable": True,
                    "qc_product_name": "shoes",
                    "sku": "WSH234",
                    "units": 1,
                    "selling_price": 100,
                    "discount": 0,
                    "qc_brand": "Levi",
                    "qc_product_image": "https://assets.vogue.in/photos/5d7224d50ce95e0008696c55/2:3/w_2240,c_limit/Joker.jpg"
                }
            ],
            "payment_method": "PREPAID",
            "total_discount": "0",
            "sub_total": 400,
            "length": 11,
            "breadth": 11,
            "height": 11,
            "weight": 0.5
        })
        conn.request("POST", "/v1/external/orders/create/return", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # "GET"
    def get_all_return_orders(self):
        conn = http.client.HTTPSConnection(self.base_url)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        payload = json.dumps({})
        conn.request("GET", "/v1/external/orders/processing/return", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # "POST"
    def generate_awb_for_return_shipment(self):
        conn = http.client.HTTPSConnection(self.base_url)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        payload = json.dumps({
            "shipment_id": "",
            "courier_id": "",
            "status": "",
            "is_return": ""
        })
        conn.request("POST", "/v1/external/courier/assign/awb", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # Shipments
    # "GET"
    def get_all_shipments(self):
        conn = http.client.HTTPSConnection(self.base_url)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        payload = ''
        conn.request("GET", "/v1/external/shipments", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))
        data = json.loads(data)
        print(data)

    # "GET"
    def get_specific_shipment(self):
        conn = http.client.HTTPSConnection(self.base_url)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        payload = ''
        conn.request("GET", "/v1/external/shipments/515140411", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # "POST"
    def cancel_a_shipment(self):
        conn = http.client.HTTPSConnection(self.base_url)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        payload = json.dumps({
            "awbs": [
                "19041211125783"
            ]
        })
        conn.request("POST", "/v1/external/orders/cancel/shipment/awbs", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # Labels | Manifests | Invoice
    # "POST"
    def generate_manifest(self):
        conn = http.client.HTTPSConnection(self.base_url)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        payload = json.dumps({
            "shipment_id": [
                515140411
            ]
        })
        conn.request("POST", "/v1/external/manifests/generate", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # "POST"
    def print_manifest(self):
        conn = http.client.HTTPSConnection(self.base_url)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        payload = json.dumps({
            "order_ids": [
                515140411
            ]
        })
        conn.request("POST", "/v1/external/manifests/print", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # "POST"
    def generate_label(self):
        conn = http.client.HTTPSConnection(self.base_url)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        payload = json.dumps({
            "shipment_id": [
                "515140411"
            ]
        })
        conn.request("POST", "/v1/external/courier/generate/label", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # "POST"
    def generate_invoice(self):
        conn = http.client.HTTPSConnection(self.base_url)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        payload = json.dumps({
            "ids": [
                "523259367"
            ]
        })
        conn.request("POST", "/v1/external/orders/print/invoice", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # Wrapper API
    # "POST"
    def wrapper_forward(self):
        conn = http.client.HTTPSConnection(self.base_url)
        payload = json.dumps({
            "order_id": "22114477",
            "order_date": "2018-05-08 12:23",
            "channel_id": "27202",
            "billing_customer_name": "Jax",
            "billing_last_name": "Tank",
            "billing_address": "Dust2",
            "billing_city": "New Delhi",
            "billing_pincode": "110002",
            "billing_state": "Delhi",
            "billing_country": "India",
            "billing_email": "mailto:jax@counterstike.com",
            "billing_phone": "9988998899",
            "shipping_is_billing": True,
            "order_items": [
                {
                    "name": "T-shirt Round Neck",
                    "sku": "t-shirt-round1474",
                    "units": 10,
                    "selling_price": "400"
                }
            ],
            "payment_method": "COD",
            "sub_total": 4000,
            "length": 100,
            "breadth": 50,
            "height": 10,
            "weight": 0.5,
            "pickup_location": "HomeNew",
            "vendor_details": {
                "email": "mailto:abcdd@abcdd.com",
                "phone": 9879879879,
                "name": "Coco Cookie",
                "address": "Street 1",
                "address_2": "",
                "city": "delhi",
                "state": "new delhi",
                "country": "india",
                "pin_code": "110077",
                "pickup_location": "HomeNew"
            }
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        conn.request("POST", "/v1/external/shipments/create/forward-shipment", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # "POST"
    def wrapper_return(self):
        conn = http.client.HTTPSConnection(self.base_url)
        payload = json.dumps({
            "order_id": "r121579B09ap492",
            "order_date": "2022-02-16",
            "channel_id": "2113680",
            "pickup_customer_name": "iron man",
            "pickup_last_name": "",
            "company_name": "iorn pvt ltd",
            "pickup_address": "b-123",
            "pickup_address_2": "",
            "pickup_city": "Delhi",
            "pickup_state": "New Delhi",
            "pickup_country": "India",
            "pickup_pincode": 110030,
            "pickup_email": "mailto:deadpool@red.com",
            "pickup_phone": "9810363552",
            "pickup_isd_code": "91",
            "shipping_customer_name": "Jax",
            "shipping_last_name": "Doe",
            "shipping_address": "Castle",
            "shipping_address_2": "Bridge",
            "shipping_city": "Delhi",
            "shipping_country": "India",
            "shipping_pincode": 110015,
            "shipping_state": "New Delhi",
            "shipping_email": "mailto:kumar.abhishek@shiprocket.com",
            "shipping_isd_code": "91",
            "shipping_phone": 8888888888,
            "order_items": [
                {
                    "name": "shoes",
                    "qc_enable": True,
                    "qc_product_name": "shoes",
                    "sku": "WSH234",
                    "units": 1,
                    "selling_price": 100,
                    "discount": 0,
                    "qc_brand": "Levi",
                    "qc_product_image": "https://assets.vogue.in/photos/5d7224d50ce95e0008696c55/2:3/w_2240,c_limit/Joker.jpg"
                }
            ],
            "payment_method": "PREPAID",
            "total_discount": "0",
            "sub_total": 400,
            "length": 11,
            "breadth": 11,
            "height": 11,
            "weight": 0.5,
            "request_pickup": True
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        conn.request("POST", "/v1/external/shipments/create/return-shipment", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # NDR
    # "GET"
    def det_all_ndr_shipments(self):
        conn = http.client.HTTPSConnection(self.base_url)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        payload = ''
        conn.request("GET", "/v1/external/ndr/all", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # "GET"
    def get_specific_ndr_shipment_details(self):
        conn = http.client.HTTPSConnection(self.base_url)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        payload = ''
        conn.request("GET", "/v1/external/ndr/94711332", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # "POST"
    def action_ndr(self):
        conn = http.client.HTTPSConnection(self.base_url)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        payload = json.dumps({
            "action": "return",
            "comments": "The Byer does not want the product"
        })
        conn.request("POST", "/v1/external/ndr/8805225468/action", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # Tracking
    # "GET"
    def tracking_with_awb(self):
        conn = http.client.HTTPSConnection(self.base_url)
        payload = ''
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        conn.request("GET", "/v1/external/courier/track/awb/788830567028", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # "POST"
    def tracking_data_for_multiple_awbs(self):
        conn = http.client.HTTPSConnection(self.base_url)
        payload = json.dumps({
            "awbs": [
                "788830567028",
                "788829354408"
            ]
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        conn.request("POST", "/v1/external/courier/track/awbs", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # "GET"
    def track_orders_with_shipment_id(self):
        conn = http.client.HTTPSConnection(self.base_url)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        payload = ''
        conn.request("GET", "/v1/external/courier/track/shipment/520690807", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # "GET"
    def track_orders_with_order_id(self):
        conn = http.client.HTTPSConnection(self.base_url)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        payload = ''
        conn.request("GET", "/v1/external/courier/track?order_id=522585096&channel_id=4910762", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # Pickup Addresses
    # "GET"
    def get_all_pickup_location(self):
        conn = http.client.HTTPSConnection(self.base_url)
        headers = {
            'Authorization': 'Bearer ' + self.token
        }
        payload = ''
        conn.request("GET", "/v1/external/settings/company/pickup", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # "POST"
    def add_a_new_pickup_location(self):
        conn = http.client.HTTPSConnection(self.base_url)
        payload = json.dumps({
            "pickup_location": "Home",
            "name": "Deadpool",
            "email": "mailto:deadpool@chimichanga.com",
            "phone": "9777777779",
            "address": "Mutant Facility, Sector 3 ",
            "address_2": "",
            "city": "Pune",
            "state": "Maharshtra",
            "country": "India",
            "pin_code": "110022"
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        conn.request("POST", "/v1/external/settings/company/addpickup", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # International
    # "GET"
    def international_tracking(self):
        conn = http.client.HTTPSConnection(self.base_url)
        headers = {
            'accept': 'application/json'
        }
        payload = ''
        conn.request("GET", "/external/international/orders/track", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # "POST"
    def international_kyc(self):
        conn = http.client.HTTPSConnection(self.base_url)
        payload = ''
        headers = {}
        conn.request("POST", "/v1/external/international/settings/international_kyc", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # "POST"
    def add_bank_details(self):
        conn = http.client.HTTPSConnection(self.base_url)
        payload = json.dumps({
            "bank_account_type": "saving",
            "beneficiary_name": "JohnDoe",
            "bank_ifsc_code": "ABCD0123456",
            "bank_account_number": "1234567890"
        })
        headers = {
            'Content-Type': 'application/json'
        }
        conn.request("POST", "/v1/external/international/settings/add-bank-details", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # "POST"
    def create_order(self):
        conn = http.client.HTTPSConnection(self.base_url)
        payload = ""
        headers = {}
        conn.request("POST", "/v1/external/international/orders/create/adhoc", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # "POST"
    def update_international_order(self):
        conn = http.client.HTTPSConnection(self.base_url)
        payload = ""
        headers = {}
        conn.request("POST", "/v1/external/international/orders/update/adhoc", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # "POST"
    def international_wrapper_api(self):
        conn = http.client.HTTPSConnection(self.base_url)
        payload = json.dumps({
            "order_id": "320988727",
            "order_date": "2022-05-08 12:23",
            "channel_id": "",
            "billing_customer_name": "Jax",
            "billing_last_name": "Tank",
            "billing_address": "Dust2",
            "billing_city": "New Delhi",
            "billing_pincode": "442001",
            "billing_state": "Delhi",
            "billing_country": "India",
            "billing_email": "mailto:jax@counterstike.com",
            "billing_phone": "9988998899",
            "shipping_is_billing": False,
            "shipping_customer_name": "Elena ",
            "shipping_last_name": "",
            "shipping_address": "Plot 1, Panchkula, Haryana 134113, India",
            "shipping_address_2": "",
            "shipping_city": "UPTON",
            "order_type": 1,
            "shipping_country": "United States",
            "shipping_pincode": "11973",
            "shipping_state": "New York",
            "shipping_email": "mailto:test.test@shiprocket.com",
            "product_category": "",
            "shipping_phone": 9760853722,
            "order_items": [
                {
                    "name": "Delta",
                    "sku": "delta123",
                    "units": 10,
                    "selling_price": "1000",
                    "hsn": "24567870"
                }
            ],
            "payment_method": "PREPAID",
            "sub_total": 40,
            "length": 10,
            "breadth": 10,
            "height": 10,
            "weight": 0.7,
            "pickup_location": "rtryttest",
            "vendor_details": {
                "email": "mailto:mayur.p@iksula.com",
                "phone": 9879879879,
                "name": "Coco Cookie",
                "address": "F2004 Street  Street 1 Street ",
                "address_2": "",
                "city": "delhi",
                "state": "new delhi",
                "country": "india",
                "pin_code": "442001",
                "pickup_location": "rtryttest"
            },
            "purpose_of_shipment": 0,
            "currency": "INR",
            "igstPaymentStatus": "A",
            "Terms_Of_Invoice": "Paid",
            "igst_amount": 10,
            "ioss": "IM1234567890",
            "pickup_location_id": 647
        })
        headers = {
            'Content-Type': 'application/json'
        }
        conn.request("POST", "/v1/external/international/shipments/create/forward-shipment", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # "GET"
    def serviceability(self):
        conn = http.client.HTTPSConnection(self.base_url)
        payload = ''
        headers = {
            'Authorization': 'Bearer'
        }
        conn.request("GET",
                     "/v1/external/international/courier/serviceability?weight=0.5&cod=0&delivery_country=United%20States&pickup_postcode=110030",
                     payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # "POST"
    def awb_assignment(self):
        conn = http.client.HTTPSConnection(self.base_url)
        payload = "{\n    \"shipment_id\": 160169474,\n    \"courier_id\": 332,\n    \"status\": \"\"\n}"
        headers = {
            'accept': 'application/json'
        }
        conn.request("POST", "/external/international/courier/assign/awb", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # "POST"
    def manifest_generation(self):
        conn = http.client.HTTPSConnection(self.base_url)
        payload = "{\n    \"shipment_id\": [152757135]\n}"
        headers = {}
        conn.request("POST", "/external/international/manifests/generate", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # "POST"
    def generate_pickup(self):
        conn = http.client.HTTPSConnection(self.base_url)
        payload = "{\n    \"shipment_id\": 152757127\n}"
        headers = {
            'accept': 'application/json'
        }
        conn.request("POST", "/external/international/courier/generate/pickup", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # Account
    # "GET"
    def get_wallet_balance(self):
        conn = http.client.HTTPSConnection(self.base_url)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        payload = ''
        conn.request("GET", "/v1/external/account/details/wallet-balance", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # Products
    # "GET"
    def get_all_product(self):
        conn = http.client.HTTPSConnection(self.base_url)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        payload = ''
        conn.request("GET", "/v1/external/products", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # "GET"
    def get_specific_product_details(self):
        conn = http.client.HTTPSConnection(self.base_url)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        payload = ''
        conn.request("GET", "/v1/external/products/show/17484610", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # "POST"
    def add_new_product(self):
        conn = http.client.HTTPSConnection(self.base_url)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        payload = json.dumps({
            "name": "Batman",
            "category_code": "default",
            "type": "Single",
            "qty": "10",
            "sku": "bat1234"
        })
        conn.request("POST", "/v1/external/products", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # "POST"
    def bulk_import_products(self):
        conn = http.client.HTTPSConnection(self.base_url)
        dataList = []
        boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=file; filename={0}'.format('file')))

        fileType = mimetypes.guess_type('/path/to/file')[0] or 'application/octet-stream'
        dataList.append(encode('Content-Type: {}'.format(fileType)))
        dataList.append(encode(''))

        with open('/path/to/file', 'rb') as f:
            dataList.append(f.read())
        dataList.append(encode('--' + boundary + '--'))
        dataList.append(encode(''))
        body = b'\r\n'.join(dataList)
        payload = body
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token,
            'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
        }
        conn.request("POST", "/v1/external/products/import", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # "GET"
    def get_sample_csv_format(self):
        conn = http.client.HTTPSConnection(self.base_url)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        payload = ''
        conn.request("GET", "/v1/external/products/sample", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # Listings
    # "GET"
    def get_all_listings(self):
        conn = http.client.HTTPSConnection(self.base_url)
        payload = ''
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        conn.request("GET", "/v1/external/listings", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # "POST"
    def map_channel_product(self):
        conn = http.client.HTTPSConnection(self.base_url)
        payload = json.dumps({
            "product_id": 17908342,
            "listing_id": 15897064
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        conn.request("POST", "/v1/external/listings/link", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # "POST"
    def import_catalog_mappings(self):
        conn = http.client.HTTPSConnection(self.base_url)
        dataList = []
        boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=file; filename={0}'.format('file')))

        fileType = mimetypes.guess_type('/path/to/file')[0] or 'application/octet-stream'
        dataList.append(encode('Content-Type: {}'.format(fileType)))
        dataList.append(encode(''))

        with open('/path/to/file', 'rb') as f:
            dataList.append(f.read())
        dataList.append(encode('--' + boundary + '--'))
        dataList.append(encode(''))
        body = b'\r\n'.join(dataList)
        payload = body
        headers = {
            'Authorization': 'Bearer ' + self.token,
            'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
        }
        conn.request("POST", "/v1/external/listings/import", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # "GET"
    def export_mapped_products(self):
        conn = http.client.HTTPSConnection(self.base_url)
        payload = ''
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        conn.request("GET", "/v1/external/listings/export/mapped", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # "GET"
    def export_unmapped_products(self):
        conn = http.client.HTTPSConnection(self.base_url)
        payload = ''
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        conn.request("GET", "/v1/external/listings/export/unmapped", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # "GET"
    def export_catalog_sample(self):
        conn = http.client.HTTPSConnection(self.base_url)
        payload = ''
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        conn.request("GET", "/v1/external/listings/sample", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # Channels
    # "GET"
    def get_channel_details(self):
        channel_obj = self.env['lax.shiprocket.channel']
        conn = http.client.HTTPSConnection(self.base_url)
        payload = ''
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        conn.request("GET", "/v1/external/channels", payload, headers)
        res = conn.getresponse()
        data = res.read()
        data.decode("utf-8")
        str_data = json.loads(data)
        for rec in str_data.get('data'):
            print(":::::::::::::::::", rec)
            channel_id = rec.get('id')
            print("channel id", channel_id)
            cha_id = channel_obj.search([('shiprocket_channel_id', '=', channel_id)], limit=1)
            shiprocket_id = self.env['lax.shiprocket.api'].search([('gmail', '=', self.gmail)], limit=1)
            data = {
                'gmail': shiprocket_id.gmail,
                'shiprocket_channel_id': channel_id,
                'name': rec.get('name'),
                'status': rec.get('status')
            }
            if not cha_id:
                print("data", data)
                new_channel_id = channel_obj.create(data)
                print(",,,,,,,,,,", new_channel_id)
            else:
                print("old channle id", cha_id)
                print("::::::::::::::::::::", cha_id.write(data))

    # Inventory
    # "GET"
    def get_inventory_details(self):
        conn = http.client.HTTPSConnection(self.base_url)
        payload = ''
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        conn.request("GET", "/v1/external/inventory", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # "PUT"
    def update_inventory(self):
        conn = http.client.HTTPSConnection(self.base_url)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        payload = json.dumps({
            "quantity": 2,
            "action": "remove"
        })
        conn.request("PUT", "/v1/external/inventory/17454637/update", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # Countries
    # "GET"
    def get_country_codes(self):
        conn = http.client.HTTPSConnection(self.base_url)
        payload = ''
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        conn.request("GET", "/v1/external/countries", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # GET
    def get_all_zones(self):
        conn = http.client.HTTPSConnection(self.base_url)
        payload = ''
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        conn.request("GET", "/v1/external/countries/show/4", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # GET
    def get_locality_details(self):
        conn = http.client.HTTPSConnection(self.base_url)
        payload = ''
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        conn.request("GET", "/v1/external/open/postcode/details", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # Statement Details
    # GET
    def get_statement_details(self):
        conn = http.client.HTTPSConnection(self.base_url)
        payload = ''
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        conn.request("GET", "/v1/external/account/details/statement", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # Discrepancy Details
    # GET
    def get_discrepancy_data(self):
        conn = http.client.HTTPSConnection(self.base_url)
        payload = ''
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        conn.request("GET", "/v1/external/billing/discrepancy", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    # File Imports
    # GET
    def get_file_import_results(self):
        conn = http.client.HTTPSConnection(self.base_url)
        payload = ''
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        conn.request("GET", "/v1/external/errors/20212061/check", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    def configuration(self):
        return {
            'name': 'Configuration',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'lax.shiprocket.api',
            'res_id': self.id,
            'type': 'ir.actions.act_window',
            'target': 'current',
        }


class SalesOrderInherit(models.Model):
    _inherit = 'sale.order'

    shiprocket_order_id = fields.Char(string="Shiprocket Order Id")
    inherit_order_id = fields.Many2one('lax.shiprocket.api', string="Order Id")
