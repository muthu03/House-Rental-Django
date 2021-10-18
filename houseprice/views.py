from django.http import HttpResponse
from django.shortcuts import render
import joblib
from houseprice.settings import RAZORPAY_API_KEY, RAZORPAY_API_SECERT_KEY
import razorpay

from django.contrib.auth. forms import UserCreationForm


def index(request):
    return render(request, 'index.html')


def app(request):
    return render(request, 'app.html')


def result(request):

    import numpy as np
    import pandas as pd

    dff = pd.read_csv('final_cleaned_data_4.csv')
    dummies_dff = pd.get_dummies(dff.location)
    dff1 = pd.concat([dff, dummies_dff], axis='columns')
    dff = dff1.drop(columns=['Vittasandra', 'location'])
    from sklearn.linear_model import LinearRegression
    from sklearn.model_selection import train_test_split
    from sklearn import preprocessing
    model = LinearRegression()
    x = dff.drop(columns=['price', 'price_per_sqft'])
    y = dff1['price']
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.35, random_state=10)
    model.fit(x_train, y_train)
    model.score(x_test, y_test)

    def prediction(location, sqft, bhk, bath):
        location_index = np.where(x.columns == location)[0][0]
        X = np.zeros(len(x.columns))
        X[0] = bhk
        X[1] = sqft
        X[2] = bath
        # X[3]=price_per_sqft
        # X[3]= pricepersqft'( if we want to add price_p_sqft as a feature)
        if location_index >= 0:
            X[location_index] = 1
        y = model.predict([X])[0]
        y = (y/300)*-1
        y = y/1.5
        return y
    area = float((request.GET['Squareft']))
    bhk = float((request.GET['uiBHK']))

    bath = float((request.GET['uiBathrooms']))
    location = str((request.GET['location']))
    Price_prediction = prediction(location, area, bhk, bath)

    return render(request, "result.html", {'price_prediction': Price_prediction})


def login(request):
    return render(request, "login.html")


def faq(request):
    return render(request, 'faq.html')


def search(request):

    return render(request, 'search.html')


client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECERT_KEY))


def pay(request):
    order_amount = 100000
    order_currency = 'INR'
    payment_order = client.order.create(
        dict(amount=order_amount, currency=order_currency, payment_capture=1))
    payment_order_id = payment_order['id']
    context = {
        'amount': order_amount, 'api_key': RAZORPAY_API_KEY, 'order_id': payment_order_id
    }
    return render(request, 'pay.html', context)
