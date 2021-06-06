import json
import ast
import os
import uuid
from prettytable import PrettyTable
import datetime
import requests

current_user_id = 0
user_voucher_list = []
BASE = "http://127.0.0.1:5000/"

#Utility function to print the vouchers table and returns the selected voucher_id
def select_voucher():
  print('\n')
  myTable = PrettyTable(["voucher_id", "voucher_code", "voucher_description", "voucher_start_time", "voucher_expiry_time", "voucher_count"])
  response = requests.get(BASE + "admin/vouchers")
  vouchers = response.json()

  for voucher_id, voucher_info in vouchers.items():
        myTable.add_row([voucher_id, voucher_info['voucher_code'], voucher_info['voucher_description'], voucher_info['voucher_start_time'], voucher_info['voucher_expiry_time'], voucher_info['voucher_count'] ])
  print(myTable)

  print('\n')

  voucher_id = input(f'Enter the voucher id: ')
  return int(voucher_id)

#Utility function to print the users table and returns the selected user_id
def select_user():
  print('\n')
  myTable = PrettyTable(["user_id", "user_name"])
  response = requests.get(BASE + "user")
  users = response.json()

  for user_id, user_info in users.items():
        myTable.add_row([user_id, user_info['user_name']])

  print(myTable)

  user_id = input(f'Enter the user id: ')
  return int(user_id)


def get_user():
    user_name = input(f'Enter you user name: ')
    response = requests.get(BASE + "user")
    users = response.json()
    is_error = True
    global current_user_id
    for user_id, user_info in users.items():
        if user_info['user_name'] == user_name:
            current_user_id = user_id
            print(current_user_id)
            print('Welcome to the system')
            is_error = False
            break

    if is_error:
        print("You are not registered to the system, Please login with correct name")
        exit()


#Function to add voucher(Only admin has acces to add vouchers)
def add_voucher():
  add_voucher = 'Y'

  while add_voucher == 'Y':

    #This will store the voucher inputs from admin
    vouchers_list = [{ "voucher_code": "", "voucher_description": "", "voucher_start_time": "", "voucher_expiry_time": "", "voucher_count": ""  }]

    #Generating random voucher_id using python uuid module
    voucher_id = uuid.uuid1().int
 
    #Taking inputs from admin
    vouchers_list[0]['voucher_code'] = input(f'Enter Voucher Code: ')
    vouchers_list[0]['voucher_description'] = input(f'Enter Voucher Description: ')
    vouchers_list[0]['voucher_start_time']  = input(f'Enter Voucher Start Time in YYYY-MM-DD: ')
    vouchers_list[0]['voucher_expiry_time']  = input(f'Enter Voucher Expiry Time in YYYY-MM-DD: ')
    vouchers_list[0]['voucher_count'] = input(f'Enter Voucher Count: ')

    print('\n')
    
    #Sending Put request to server
    response = requests.put(BASE + "admin/voucher/" + str(voucher_id) , vouchers_list[0])
    print(response.json())
    
    print('\n')
    add_voucher = input(f'Add another voucher?Y/N: ').upper()
  
  select_operation()

#This will edit the already existing voucher 
def edit_voucher():
  edit_voucher = 'Y'
  while edit_voucher == 'Y':
    
        voucher_id = select_voucher()

        #This will hold the new values
        vouchers_list = [{ "voucher_code": "", "voucher_description": "", "voucher_start_time": "", "voucher_expiry_time": "", "voucher_count": "" }]

        vouchers_list[0]['voucher_code'] = input(f'Enter New Voucher Code: ')
        vouchers_list[0]['voucher_description'] = input(f'Enter New Voucher Description: ')
        vouchers_list[0]['voucher_start_time']  = input(f'Enter New Voucher Start Time in YYYY-MM-DD: ')
        vouchers_list[0]['voucher_expiry_time']  = input(f'Enter New Voucher Expiry Time in YYYY-MM-DD: ')
        vouchers_list[0]['voucher_count'] = input(f'Enter New Voucher Count :')

        response = requests.patch(BASE + "admin/voucher/" + str(voucher_id) , vouchers_list[0])
        print(response.json())
        print('\n')
        edit_voucher = input(f'Edit another voucher?Y/N: ').upper()
  select_operation()

#This will delete the selected voucher 
def delete_voucher():
  delete_voucher = 'Y'
  while delete_voucher == 'Y':

    #This is the utility function to select voucher to be deleted
    voucher_id = select_voucher()

    response = requests.delete(BASE + "admin/voucher/" + str(voucher_id))
    print(response)
    
    print('\n')
    delete_voucher = input(f'Want to Delete another VoucherY/N: ').upper()
  select_operation()

#This will list all available or going to available vouchers 
def list_voucher():

    #creating the header row of table
    myTable = PrettyTable(["voucher_id","voucher_code", "voucher_description", "voucher_start_time", "voucher_expiry_time", "voucher_count"])

    #Request made to server to get the vouchers list
    response = requests.get(BASE + "admin/vouchers")
    vouchers = response.json()

    #Printing each voucher in different rows of table
    for voucher_id, voucher_info in vouchers.items():
        myTable.add_row([voucher_id, voucher_info['voucher_code'], voucher_info['voucher_description'], voucher_info['voucher_start_time'], voucher_info['voucher_expiry_time'], voucher_info['voucher_count'] ])
    print(myTable)
    print('\n')
    input(f'Press Y to continue: ').upper()
    select_operation()


#This will issue voucher to user
def issue_voucher():
  issue_voucher = 'Y'
  while issue_voucher == 'Y':

      user_id = select_user() 
      voucher_id = select_voucher()

      #This will hold the values of voucher associated to user
      user_voucher_list = [{ "user_id": "", "voucher_id": "", "voucher_used_date": "", "is_used": "" }]

      user_voucher_id = uuid.uuid1().int
      user_voucher_list[0]['user_id'] = user_id
      user_voucher_list[0]['voucher_id'] = voucher_id
      user_voucher_list[0]['voucher_used_date'] = "N/A"
      user_voucher_list[0]['is_used'] = "False"

      response = requests.put(BASE + "/admin/user_voucher/" + str(user_voucher_id) , user_voucher_list[0])
      print(response.json())
     
      print('\n')
      issue_voucher = input(f'Add another voucher?Y/N: ').upper()
  select_operation()

#This will list the associated to user
def list_user_voucher():
  myTable = PrettyTable(["voucher_code", "voucher_description"])
  
  response = requests.get(BASE + "user/user_voucher/"+ str(current_user_id))
  user_voucher = response.json()
  print(user_voucher)

  for voucher_id, voucher_info in user_voucher.items():
        myTable.add_row([voucher_info['voucher_code'], voucher_info['voucher_description'] ])
  print(myTable)

  print('\n')
  
  input(f'Press Y to continue: ').upper()
  select_operation()

#This will apply voucher for users
def apply_voucher():
    voucher_code = input('Enter the voucher code that you want to apply: ')
    voucher_details = [ {"voucher_code" : voucher_code}]
    response = requests.put(BASE + "/user/apply_user_voucher/" + str(current_user_id), voucher_details[0])
    print(response.json())
    select_operation() 

def select_operation():
  
  print('\n')
  if is_admin == 'Y':
    print('Available Operations are:')
    operations = ['Add Voucher', 'Edit Voucher', 'Delete Voucher', 'List Voucher','Issue_Voucher', 'Exit']
    myTable = PrettyTable(["operation_id" , "operation_name" ])
    for i in range(len(operations)):
        myTable.add_row([i+1,  operations[i] ])
    print(myTable)
    
    print('\n')
    selected_admin_operation = input(f'Select the operation_id which you want to perform: ') 
    if selected_admin_operation == '1':
        add_voucher()
    elif selected_admin_operation == '2':
        edit_voucher()
    elif selected_admin_operation == '3':
        delete_voucher()
    elif selected_admin_operation == '4':
        list_voucher()
    elif selected_admin_operation == '5':
        issue_voucher()
    else:
        print('Exited')
  else:

    print('\n')
    print('Available Operations are:')
    operations = ['List Voucher', 'Apply Voucher', 'Exit']
    myTable = PrettyTable(["operation_id" , "operation_name" ])
    for i in range(len(operations)):
        myTable.add_row([i+1,  operations[i] ])
    print(myTable)
    selected_admin_operation = input(f'Select the operation_id which you want to perform: ')
    if selected_admin_operation == '1':
        list_user_voucher()
    elif selected_admin_operation == '2':
        apply_voucher()
    else:
        print('Exited')

print('\n')
is_admin = 'N'
is_admin = input(f'Are you admin user or notY/N: ')

print('\n')
if is_admin == 'N':
    get_user()
else:
    print('Welcome admin to system')

select_operation()

