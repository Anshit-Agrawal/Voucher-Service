from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
import datetime

app = Flask(__name__)
api = Api(app)

#Post Request Arguments for adding vouchers
voucher_put_args = reqparse.RequestParser()
voucher_put_args.add_argument("voucher_code", type=str, help="Voucher Code is required", required=True)
voucher_put_args.add_argument("voucher_description", type=str, help="Voucher Description is required", required=True)
voucher_put_args.add_argument("voucher_start_time", type=str, help="Voucher start time is required", required=True)
voucher_put_args.add_argument("voucher_expiry_time", type=str, help="Voucher expiry time is required", required=True)
voucher_put_args.add_argument("voucher_count", type=str, help="Voucher Count is required", required=True)

#Post Request Arguments for adding User related vouchers
user_voucher_put_args = reqparse.RequestParser()
user_voucher_put_args.add_argument("user_id", type=str, help="User Id is required", required=True)
user_voucher_put_args.add_argument("voucher_id", type=str, help="Voucher Id is required", required=True)
user_voucher_put_args.add_argument("voucher_used_date", type=str, help="Voucher Used Date is required", required=True)
user_voucher_put_args.add_argument("is_used", type=str, help="is used is required", required=True)

#Post Request Arguments for applying vouchers through users
apply_user_voucher_args = reqparse.RequestParser()
apply_user_voucher_args.add_argument("voucher_code", type=str, help="Voucher Code is required", required=True)

#Dictionary containing list of vouchers created by admin
vouchers = {}

users = {
        "12342222222122222": {
            "user_name" : "anshit"
            },
        "2345234577777": {
            "user_name" : "shiv"
            }
        }
user_voucher = {}

#Function to abort deleting voucher , if it doesnot exist
def abort_if_voucher_id_not_exist(voucher_id):
    if voucher_id not in vouchers:
        abort(404 , message="Voucher Id is not Valid")

#Function to abort adding voucher , if it already exist 
def abort_adding_voucher_if_already_exists(voucher_code):
    for voucher_id, voucher_info in vouchers.items():
        if voucher_info['voucher_code'] == voucher_code:
            abort(404 , message="Voucher Already Exist. If want to chnage the values then try Edit Voucher Option")

#Function to abort  adding voucher if time is given wrong
def abort_adding_voucher_if_time_is_invalid(voucher_start_time, voucher_expiry_time):
    startTime = datetime.datetime.strptime(voucher_start_time, '%Y-%m-%d')
    expiryTime = datetime.datetime.strptime(voucher_expiry_time, '%Y-%m-%d')
    currentTime=str(datetime.date.today())
    currentTime= datetime.datetime.strptime(currentTime, '%Y-%m-%d')

    if startTime < currentTime or expiryTime < currentTime :
        abort(400 , message="Voucher addition failed as time inputs are invalid")

#Function to abort  adding voucher if count is less than zero
def abort_adding_voucher_if_count_is_less_than_zero(voucher_count):
    
    if int(voucher_count) <= 0:
        abort(400 , message="Voucher Count cannot be less than zero")

#Function to abort issuing voucher to user if he already had it and didnt used
def abort_adding_user_voucher_if_user_already_has(voucher_id , user_id):
    for user_voucher_id, user_voucher_info in user_voucher.items():
        if user_voucher_info['voucher_id'] == voucher_id and user_voucher_info['user_id'] == user_id and user_voucher_info['is_used'] == 'False':
            abort(404 , message="Voucher was already issue to the user")

#The methods present in class are only accesible by admin users
class Voucher(Resource):
    
    #To get the all available vouchers created by admin
    def get(self):
        available_vouchers = {}
        for voucher_id, voucher_info in vouchers.items():

            #Only those vouchers will be return whose count is greater than zero and are not expired
            expiryTime = datetime.datetime.strptime(voucher_info['voucher_expiry_time'], '%Y-%m-%d')
            currentTime=str(datetime.date.today())
            currentTime= datetime.datetime.strptime(currentTime, '%Y-%m-%d')
            
            if  int(voucher_info['voucher_count']) > 0 and expiryTime >= currentTime :
                available_vouchers[voucher_id] = voucher_info
        return available_vouchers, 201
   
    #To store the vouchers created by admin
    def put(self, voucher_id):
        args = voucher_put_args.parse_args()

        abort_adding_voucher_if_already_exists(args['voucher_code'])
        abort_adding_voucher_if_time_is_invalid(args['voucher_start_time'], args['voucher_expiry_time'])
        abort_adding_voucher_if_count_is_zero(args['voucher_count'] )

        vouchers[voucher_id] = args
        return {"message": "Voucher Added Successfully"}, 201
   
    #To delete the voucher based on voucher_id passed
    def delete(self, voucher_id):
        abort_if_voucher_id_not_exist(voucher_id)

        del vouchers[voucher_id]
        return {"message": "Voucher Deleted Successfully"}, 204

    #To edit the already existing voucher
    def patch(self, voucher_id):
        abort_if_voucher_id_not_exist(voucher_id)

        args = voucher_put_args.parse_args()
        
        abort_adding_voucher_if_time_is_invalid(args['voucher_start_time'], args['voucher_expiry_time'])

        vouchers[voucher_id] = args
        return {"message": "Voucher Updated Successfully"}, 201

#Thi will create user related info
class UserVoucher(Resource):

    def get(self, user_id):
        current_user_id = user_id

        current_user_voucher = {}

        #This will store only the vouchers associated to the user
        for user_voucher_id, user_voucher_info in user_voucher.items():
            if user_voucher_info['user_id'] == str(current_user_id) and user_voucher_info['is_used'] == 'False':
                current_voucher_id = int(user_voucher_info['voucher_id'])

                current_user_voucher[current_voucher_id] = vouchers[current_voucher_id]

        #This will filter out the available vouchers
        available_vouchers = {}
        for voucher_id, voucher_info in current_user_voucher.items():

            #Only those vouchers will be return whch are live
            expiryTime = datetime.datetime.strptime(voucher_info['voucher_expiry_time'], '%Y-%m-%d')
            startTime = datetime.datetime.strptime(voucher_info['voucher_start_time'], '%Y-%m-%d')
            currentTime=str(datetime.date.today())
            currentTime= datetime.datetime.strptime(currentTime, '%Y-%m-%d')

            if expiryTime >= currentTime  and startTime <= currentTime :
                available_vouchers[voucher_id] = voucher_info
        return available_vouchers , 200

    #To add user related vouchers
    def put(self, user_voucher_id):
        args = user_voucher_put_args.parse_args()

        abort_adding_user_voucher_if_user_already_has(args['voucher_id'], args['user_id'])

        #Decreasing the vouchers count from voucher table after issuing 
        voucher_id = int(args['voucher_id'])
        if int(vouchers[voucher_id]['voucher_count']) > 0 :
            vouchers[voucher_id]['voucher_count'] = str(int(vouchers[voucher_id]['voucher_count']) - 1 )  

        user_voucher[user_voucher_id] = args
        return {"message": "Voucher Issued to User Successfully"}, 201

#The methods present in class are only accesible by admin users
class User(Resource):

    #To get all the users Registered to system
    def get(self):
        return users

#Th methods present in class are accesible by user
class ApplyUserVoucher(Resource):

    #This will apply voucher through user
    def put(self, user_id):
        args = apply_user_voucher_args.parse_args()
        voucher_code = args['voucher_code']
        voucher_id_get = 0
        for voucher_id, voucher_info in vouchers.items():
            if voucher_info['voucher_code'] == voucher_code:
                expiryTime = datetime.datetime.strptime(voucher_info['voucher_expiry_time'], '%Y-%m-%d')
                startTime = datetime.datetime.strptime(voucher_info['voucher_start_time'], '%Y-%m-%d')
                currentTime=str(datetime.date.today())
                currentTime= datetime.datetime.strptime(currentTime, '%Y-%m-%d')

                if expiryTime >= currentTime  and startTime <= currentTime :
                    voucher_id_get = voucher_id
                break
            else:
                return {"message" : "Voucher Code Not exist"}, 400


        for user_voucher_id, user_voucher_info in user_voucher.items():
             if user_voucher_info['user_id'] == str(user_id) :

                currentTime= datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d')
                if user_voucher_info['voucher_used_date'] != 'N/A':
                    last_used = user_voucher_info['voucher_used_date']
                    if currentTime <= last_used :
                        return {"message" : "Please apply voucher after 24 hours"}, 400


        for user_voucher_id, user_voucher_info in user_voucher.items():
            print(user_voucher_info)
            if user_voucher_info['user_id'] == str(user_id) and user_voucher_info['voucher_id'] == str(voucher_id_get) and user_voucher_info['is_used'] == 'False':          

                user_voucher_info['is_used'] = 'True'
                user_voucher_info['voucher_used_date'] = datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d')
                print(user_voucher_info['voucher_used_date'])
                print(type(user_voucher_info['voucher_used_date']))

                return {"message" : "Voucher Applied Successfully"}, 200
        return {"message" : "Error in Appying Voucher"}, 400


#Route from admin to get all Vouchers 
api.add_resource(Voucher, "/admin/vouchers" ,  endpoint='getAllVoucher' )
#Route to add/delete/edit Voucher created by admin
api.add_resource(Voucher, "/admin/voucher/<int:voucher_id>")

#Route to get all the User details by admin
api.add_resource(User, "/user" ,  endpoint='getAllUser' )

#Route to issue voucher to user by admin
api.add_resource(UserVoucher, "/admin/user_voucher/<int:user_voucher_id>" )
#Route to get the live vouchers associated to user
api.add_resource(UserVoucher, "/user/user_voucher/<int:user_id>", endpoint='getAllUserVoucher' )

#Route to apply voucher through user
api.add_resource(ApplyUserVoucher, "/user/apply_user_voucher/<int:user_id>", endpoint='applyUserVoucher' )

if __name__ == "__main__":
    app.run(debug=True)
