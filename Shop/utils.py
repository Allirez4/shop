from kavenegar import *
from decimal import Decimal

def sendOTP(phone_number,code):
    try:
        api = KavenegarAPI('303079775678456676524133746D7974306835544F315334343239714A67626A5A797833716853567165493D')
        params = {
            'sender': '2000660110',#optional
            'receptor': phone_number,#multiple mobile number, split by comma
            'message': f'Your verification code is: {code}',
        } 
        response = api.sms_send(params)
        print(response)
    except APIException as e: 
        print(e)
    except HTTPException as e: 
        print(e)
def sum_cart(cart):
    total = sum(
                Decimal(item['unit_price']) * int(item['quantity']) 
             for item in cart.values()
             )
    return total