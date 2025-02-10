from flask import Flask, render_template, request
import travelling_time
from selenium import webdriver as webdriver
import datetime
import pytz
import re
import pandas as pd

app = Flask(__name__)

# load the model
import pickle

# Open the pickle file in binary mode
file_path = r"C:\Users\Mayur\Downloads\step 5 - ui of project (1)\step 5 - ui of project\step 5 - ui of project\interface of the project\pickel_model_file_rfr.pkl"
with open(file_path, 'rb') as file:  # Use 'rb' mode for reading binary files
    model = pickle.load(file)

@app.route("/", methods=["GET"])
def root():
    return render_template("index.html")


@app.route("/predict", methods=["GET"])
def predict():
    source = request.args.get('source')
    destination = request.args.get('destination')
    distance=2.5
    avg_travel_time=12
    source_1 = source + "+Boston,+MA,+USA"
    destination_1 = destination + "+Boston,+MA,+USA"
    travel_time = travelling_time.Time_travel(destination_1,
                                              source_1, webdriver)
    travel_time.car_button_click()

    ct = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))


    ts = ct.timestamp()

    y = travel_time.add_time_traveling(ts * 1000)

    # Extract integers from the first element of y
    y_1 = [int(num) for num in re.findall(r'\d+', y[0])]

    # Extract floating-point numbers from the second element of y
    y_2 = re.findall(r'\d+\.\d+', y[1])


    print(y_1)
    print(y_2)
    if len(y_1) == 1:
        avg_travel_time = int(y_1[0])
    elif len(y_1) == 2:
        avg_travel_time = (int(y_1[0]) + int(y_1[1]))/2

    if len(y_2) == 1:
        distance = float(y_2[0])*1.60934
    print(y_2)
    print(source)
    print(destination)

    temp=40.130000
    clouds=0.780000
    pressure=1007.660000
    rain=0.014850
    humidity=0.760000
    wind=6.570000



    cab = str(request.args.get('cab_type'))
    if cab=='Uber':
        cab_type_Lyft=0
        cab_type_Uber=1
    else:
        cab_type_Lyft = 1
        cab_type_Uber = 0


    type = str(request.args.get('type'))
    name_Black=name_BlackSUV = name_Lux = name_LuxBlack = name_LuxBlackXL = name_Lyft = name_LyftXL = name_Shared = name_UberPool = name_UberX = name_UberXL = name_WAV = 0

    if type=='Uber -> Black':
        name_Black=1
    elif type=='Uber -> Black SUV':
        name_BlackSUV = 1
    elif type=='Uber -> Uber Pool':
        name_UberPool = 1
    elif type=='Uber -> Uber X':
        name_UberX=1
    elif type == "Uber -> WAV":
        name_WAV = 1
    elif type == "Lyft -> Shared":
        name_Shared = 1
    elif type == "Lyft -> Lux":
        name_Lux = 1
    elif type == "Lyft -> Lux Black":
        name_LuxBlack = 1
    elif type == "Lyft -> Lux Black XL":
        name_LuxBlackXL = 1
    elif type == "Lyft -> Lyft":
        name_Lyft = 1
    elif type == "Lyft -> Lyft XL":
        name_LyftXL = 1

    surge_multiplier_1_0= surge_multiplier_1_25 = surge_multiplier_1_5= surge_multiplier_1_75 = surge_multiplier_2_0 = surge_multiplier_2_5 = surge_multiplier_3_0 = 0
    surge_multiplier_1_0 = 1

    day = ct.weekday()
    day_0, day_1, day_2, day_3, day_4, day_5, day_6=0,0,0,0,0,0,0
    if day==6:
        day_0=1
    elif day==0:
        day_1=1
    elif day==1:
        day_2=1
    elif day==2:
        day_3=1
    elif day==3:
        day_3=1
    elif day==4:
        day_4=1
    elif day==5:
        day_5=1

    class_hour_0=class_hour_1=class_hour_2=class_hour_3=class_hour_4=class_hour_5=class_hour_6=class_hour_7=0
    hour_now = ct.hour
    if hour_now >= 0 and hour_now <= 3:
        class_hour_0 = 1
    elif hour_now > 3 and hour_now <= 6:
        class_hour_1 = 1
    elif hour_now > 6 and hour_now <= 9:
        class_hour_2 = 1
    elif hour_now > 9 and hour_now <= 12:
        class_hour_3 = 1
    elif hour_now > 12 and hour_now <= 15:
        class_hour_4 = 1
    elif hour_now > 15 and hour_now <= 18:
        class_hour_5 = 1
    elif hour_now > 18 and hour_now <= 21:
        class_hour_6 = 1
    elif hour_now > 21 and hour_now <= 23:
        class_hour_7 = 1

    print(day)
    print(type)
    print(avg_travel_time)
    print(distance)
    print(cab_type_Lyft)
    print(cab_type_Uber)
    print(" ")
    print(ct.hour)
    print(ct.weekday())

    predictions = model.predict([[distance, avg_travel_time, temp, clouds, pressure, rain, humidity, wind,surge_multiplier_1_0, surge_multiplier_1_25,surge_multiplier_1_5, surge_multiplier_1_75, surge_multiplier_2_0,surge_multiplier_2_5, surge_multiplier_3_0 ,cab_type_Lyft,cab_type_Uber,name_Black,name_BlackSUV,name_Lux,name_LuxBlack,name_LuxBlackXL,name_Lyft,name_LyftXL,name_Shared,name_UberPool,name_UberX,name_UberXL,name_WAV,day_0, day_1, day_2, day_3, day_4, day_5, day_6,class_hour_0,class_hour_1,class_hour_2,class_hour_3,class_hour_4,class_hour_5,class_hour_6,class_hour_7]])
    result = f"Your Fare Price Should be Around = {predictions[0]:.2f} $"
    print(result)
    return render_template("result.html", html_result=result)


app.run(port=8080, host="0.0.0.0")




