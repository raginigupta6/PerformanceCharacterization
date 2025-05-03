from flask import Flask, render_template, redirect, request, current_app
app=Flask(__name__)
from functools import wraps
from Adafruit_DHT import DHT11, read_retry
import Adafruit_DHT
DHT_SENSOR = DHT11
DHT_PIN = 23


@app.route("/")


def mypage():
    humidity,temp=read_retry(DHT_SENSOR, DHT_PIN)
    return render_template('index.html', humidity = humidity, temperature = temp)
    


if __name__=="__main__":
    app.run(host="0.0.0.0",port=int("2040"), debug=True)



