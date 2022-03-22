import random
# from os import environ
import  os
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

from PaytmGatway import Checksum
MID = os.environ.get("MERCHANTID")
MKEY = os.environ.get("MERCHANTKEY")
# env = os.environ.
#
# environ.Env.read_env()


@api_view(['POST'])
def start_payment(request):
    if request.auth is None:
        return Response({"detail":"authentication credential not provided"})
    amount = 100
    # name = request.data['name']
    # email = request.data['email']

    # we are saving an order instance (keeping isPaid=False)
    # order = Order.objects.create(product_name=name,
    #                              order_amount=amount,
    #                              user_email=email, )
    #
    # serializer = OrderSerializer(order)
    # # we have to send the param_dict to the frontend
    # these credentials will be passed to paytm order processor to verify the business account
    param_dict = {
        'MID': MID,
        'ORDER_ID': "SSHFJ"+str(random.randint(100,10000)),
        'TXN_AMOUNT': str(amount),
        'CUST_ID': "email@emaikl.com",
        'INDUSTRY_TYPE_ID': 'Retail',
        'WEBSITE': 'WEBSTAGING',
        'CHANNEL_ID': 'WEB',
        'CALLBACK_URL': 'http://127.0.0.1:8000/api/payment/handlepayment/',
        # this is the url of handlepayment function, paytm will send a POST request to the fuction associated with this CALLBACK_URL
    }

    param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MKEY)
    # send the dictionary with all the credentials to the frontend
    return Response({'param_dict': param_dict})


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
            # after successfull payment we will make isPaid=True and will save the order
            # order.isPaid = True
            # order.save()
            # we will render a template to display the payment status
            return render(request, 'paytm/paymentstatus.html', {'response': response_dict})
        else:
            print('order was not successful because' + response_dict['RESPMSG'])

            print(response_dict)
            return render(request, 'paytm/paymentstatus.html', {'response': response_dict})