from flask import Flask, jsonify
from flask_cors import CORS

# initialize a flask application (app)
app = Flask(__name__)
CORS(app, supports_credentials=True, origins='*')  # Allow all origins (*)

# ... your existing Flask

# add an api endpoint to flask app
@app.route('/api/yash')
def get_yash():
    # start a list, to be used like a information database
    InfoDb = []

    # add a row to list, an Info record
    InfoDb.append({
        "FirstName": "Yash",
        "LastName": "Parikh",
        "DOB": "July 31",
        "Residence": "Antartica",
        "Email": "yashp51875@stu.powayusd.com",
        "Owns_Cars": ["2024-McLaren-W1-HotWheels"]
    })

    return jsonify(InfoDb)

@app.route('/api/anvay')
def get_anvay():
    # start a list, to be used like a information database
    InfoDb = []

    # add a row to list, an Info record
    InfoDb.append({
        "FirstName": "Anvay",
        "LastName": "Vahia",
        "DOB": "January 29",
        "Residence": "North Pole",
        "Email": "anvayv22800@stu.powayusd.com",
        "Owns_Cars": ["2023 Tesla Model Y", "2022 Hyundai Palisade"]
    })
    
    return jsonify(InfoDb)

# add an api endpoint to flask app
@app.route('/api/manas')
def get_manas():
    # start a list, to be used like a information database
    InfoDb = []

    # add a row to list, an Info record
    InfoDb.append({
        "FirstName": "Manas",
        "LastName": "Goel",
        "DOB": "July 12",
        "Residence": "San Diego",
        "Email": "manas.g67038@stu.powayusd.com",
        "Owns_Cars": ["2024-Model S Plaid", "2024-Mercedes", "2023-Model X", "2024-Mercedes"]
    })


# add an api endpoint to flask app
@app.route('/api/adi')
def get_adi():
    # start a list, to be used like a information database
    InfoDb = []

    # add a row to list, an Info record
    InfoDb.append({
        "FirstName": "Aditya",
        "LastName": "Katre",
        "DOB": "January 19",
        "Residence": "North Carolina",
        "Email": "adityak21664@stu.powayusd.com",
        "Owns_Cars": ["2022 Tesla Model Y Long Range", "2018 BMW 328i"]
    })
    
    return jsonify(InfoDb)

@app.route('/api/mihir')
def get_mihir():
    # start a list, to be used like a information database
    InfoDb = []

    # add a row to list, an Info record
    InfoDb.append({
        "FirstName": "Mihir",
        "LastName": "Bapat",
        "DOB": "May 26",
        "Residence": "Shrewsbury United Kingdom",
        "Email": "mihirb59967@stu.powayusd.com",
        "Owns_Cars": ["All of the above"]
    })
    
    return jsonify(InfoDb)

# add an HTML endpoint to flask app
@app.route('/')
def say_hello():
    html_content = """
    <html>
    <head>
        <title>Hellox</title>
    </head>
    <body>
        <h2>Hello, World!</h2>
    </body>
    </html>
    """
    return html_content

if __name__ == '__main__':
    # starts flask server on default port, http://127.0.0.1:3003
    app.run(port=3333)