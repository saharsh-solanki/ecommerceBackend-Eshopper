import random
# from os import environ
import os

from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

from PaytmGatway import Checksum
from cart.serializer import CartSerializer
from userOrders.models import Orders
from userOrders.serializer import OrderSerializer

MID = "OUEept11459745037985"#os.environ.get("MERCHANTID")
MKEY = "1Ihx&s#y1St!Dk0m"#os.environ.get("MERCHANTKEY","1Ihx&s#y1St!Dk0m")


# env = os.environ.
#
# environ.Env.read_env()


@api_view(['POST'])
def start_payment(request):
    if request.auth is None:
        return Response({"detail": "authentication credential not provided"})
    data = {"address_id": request.data["address_id"],
            "user_id": request.user.id,
            "status": "PENDING",
            "paymentType": "ONLINE"
            }
    serializer = OrderSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        # these credentials will be passed to paytm order processor to verify the business account
        param_dict = {
            'MID': MID,
            'ORDER_ID': serializer.data["order_id"],
            'TXN_AMOUNT': str(serializer.getCart(request.user)["total"]),
            'CUST_ID': request.user.email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': os.getenv("ISLOCAL","https://e-shopper-backend.herokuapp.com/")+'api/payment/handlepayment/',
            # this is the url of handlepayment function, paytm will send a POST request to the fuction associated with this CALLBACK_URL
        }

        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MKEY)
        # send the dictionary with all the credentials to the frontend
        return Response({'param_dict': param_dict})
        # return Response(serializer.data)
    else:
        return Response(serializer.errors)


@api_view(['POST'])
def handlepayment(request):
    checksum = ""
    # the request.POST is coming from paytm
    form = request.POST

    response_dict = {}
    order = None  # initialize the order varible with None

    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            # 'CHECKSUMHASH' is coming from paytm and we will assign it to checksum variable to verify our paymant
            checksum = form[i]

        # if i == 'ORDERID':
        #     # we will get an order with id==ORDERID to turn isPaid=True when payment is successful
        #     order = Order.objects.get(id=form[i])

    # we will verify the payment using our merchant key and the checksum that we are getting from Paytm request.POST
    verify = Checksum.verify_checksum(response_dict, MKEY, checksum)

    if verify:
        if response_dict['RESPCODE'] == '01':
            # if the response code is 01 that means our transaction is successfull
            print('order successful')
            order = Orders.objects.get(order_id=response_dict["ORDERID"])
            order.status = "SUCCESS"
            order.save()
            OrderSerializer(instance=order).deleteCart(order.user)
            return  HttpResponseRedirect(os.getenv("ISLOCAL","https://e-shopper-ujjain.herokuapp.com/")+"user/orders/"+str(order.id))
        else:
            order = Orders.objects.get(order_id=response_dict["ORDERID"])
            order.status = "FAILED"
            order.save()
            print('order was not successful because' + response_dict['RESPMSG'])
            print(response_dict)
            return  HttpResponseRedirect("http://localhost:3000/user/orders/"+str(order.id))
