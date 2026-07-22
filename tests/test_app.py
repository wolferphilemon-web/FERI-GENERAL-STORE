import unittest

from app import app
import database


class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        database.initialize_database()
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_home_page_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'FERI GENERAL STORE', response.data)

    def test_cart_and_checkout_flow(self):
        self.client.get('/buy/1')
        response = self.client.get('/cart')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Shopping Cart', response.data)

        checkout_response = self.client.get('/checkout')
        self.assertEqual(checkout_response.status_code, 200)

        order_response = self.client.post('/place_order', data={
            'fullname': 'Jane Doe',
            'phone': '0712345678',
            'email': 'jane@example.com',
            'address': 'Nairobi'
        }, follow_redirects=True)
        self.assertEqual(order_response.status_code, 200)
        self.assertIn(b'Order Confirmed', order_response.data)


if __name__ == '__main__':
    unittest.main()
