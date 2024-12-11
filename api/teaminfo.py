from flask import Blueprint, jsonify
from flask_restful import Api, Resource # used for REST API building

teaminfo_api = Blueprint('teaminfo_api', __name__,
                   url_prefix='/api')

# API docs https://flask-restful.readthedocs.io/en/latest/
api = Api(teaminfo_api)

class StudentAPI:        
    @staticmethod
    def get_member(name):
        members = {
            "Yash": {
                "FirstName": "Yash",
                "LastName": "Parikh",
                "DOB": "July 31",
                "Residence": "Antartica",
                "Email": "yashp51875@stu.powayusd.com",
                "Owns_Cars": ["2024-McLaren-W1-HotWheels"]
            },
            "Manas": {
                "FirstName": "Manas",
                "LastName": "Goel",
                "DOB": "July 12",
                "Residence": "San Diego",
                "Email": "manasg67038@stu.powayusd.com",
                "Owns_Cars": ["2024-Tesla, 2024-Mercedes"]
            },
            "Mihir": {
                "FirstName": "Mihir",
                "LastName": "Bapat",
                "DOB": "May 26",
                "Residence": "Shrewsbury, UK",
                "Email": "mih@rb59967stu.powayusd.com",
                "Owns_Cars": ["2022 Tesla Model Y"]
            },
            "Adi":  {
                "FirstName": "Adi",
                "LastName": "Katre",
                "DOB": "January 19",
                "Residence": "La La Land",
                "Email": "adityak21664@stu.powayusd.com",
                "Owns_Cars": ["2022 Tesla Model Y", "2018 BMW 328i"]
            },
            "Anvay": {
                "FirstName": "Anvay",
                "LastName": "Vahia",
                "DOB": "January 29",
                "Residence": "North Pole",
                "Email": "anvayv22800@stu.powayusd.com",
                "Owns_Cars": ["2023 Tesla Model Y", "2022 Hyundai Palisade"]
                },
            "Pranav": {
                "FirstName": "Pranav",
                "LastName": "Santhosh",
                "DOB": "May 12",
                "Residence": "California",
                "Email": "pranavs22638@stu.powayusd.com",
                "Owns_Cars": ["2023 Rivian SUV", "2024 Toyota Prius"]
            }
        }
        return members.get(name)

    class _Yash(Resource): 
        def get(self):
            yash_details = StudentAPI.get_member("Yash")
            return jsonify(yash_details)
    class _Adi(Resource): 
        def get(self):
           adi_details = StudentAPI.get_member("Adi")
           return jsonify(adi_details)
    class _Manas(Resource): 
        def get(self):
            manas_details = StudentAPI.get_member("Manas")
            return jsonify(manas_details)
    class _Anvay(Resource): 
        def get(self):
            anvay_details = StudentAPI.get_member("Anvay")
            return jsonify(anvay_details)
    class _Mihir(Resource): 
        def get(self):
            mihir_details = StudentAPI.get_member("Mihir")
            return jsonify(mihir_details)
    class _Pranav(Resource): 
        def get(self):
            pranav_details = StudentAPI.get_member("Pranav")
            return jsonify(pranav_details)
    class _Bulk(Resource):
        def get(self):
            # Use the helper method to get the team member's details
            mihir_details = StudentAPI.get_member("Mihir")
            manas_details = StudentAPI.get_member("Manas")              
            adi_details = StudentAPI.get_member("Adi")
            yash_details = StudentAPI.get_member("Yash")
            anvay_details = StudentAPI.get_member("Anvay")
            pranav_details = StudentAPI.get_member("Pranav")
            return jsonify({"students": [mihir_details, manas_details, adi_details, yash_details, anvay_details,pranav_details]})


    # building RESTapi endpoint
    api.add_resource(_Yash, '/member/yash')          
    api.add_resource(_Adi, '/member/adi')
    api.add_resource(_Manas, '/member/manas')
    api.add_resource(_Mihir, '/member/mihir')
    api.add_resource(_Anvay, '/member/anvay')
    api.add_resource(_Pranav, '/member/pranav')
    api.add_resource(_Bulk, '/members')

    
    