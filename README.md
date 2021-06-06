# Voucher-Service

This project is created using python with flask as backend server.
It consist of two types of operations:

1) Admin Operations :
    a) Admin can add vouchers with details like voucher_id, voucher_code, voucher_description , voucher_start_time , voucher_expiry_time and voucher_count                                  (Route Used  -/admin/voucher/voucher_id)
           - Here it is validated that the voucher with new added code is already not present,If present then error will be thrown
           - It is also validated that start_time , expiry_time are future times and voucher_code is not zero while adding
      
    b) Admin can delete any voucher created 
           (Route used - /admin/voucher/voucher_id )
           Here it is validated that the voucher that needs to be deleted exist or not
      
    c) Admin can edit any voucher created  
           (Route used - /admin/voucher/voucher_id )
           Here it is validated that voucher that needs to be edited exist or not 
     
    d) Admin can list all the available vouchers  
           (Route used - /admin/vouchers )
           Here it is vaildated that only those vouchers will be displayed which are not expired or there count is not zero
      
    e) Admin can issue unique vouchers to different users at regular interval of time
           (Route used = /admin/user_voucher/user_voucher_id)
           Here it is validated that the voucher is already not assigned to user
           Moreover after issuing voucher, the voucher count is also reduced by 1
     
    f) Admin can list available users 
           (Route used - /admin/user)


2) User Operation:
    a) User can list the available voucher associated to it 
           (Route used - /user/user_voucher/user_id )
           Here it is validated that only thise vouchers are displayed which are associated with this particular use and is not yet used by it
      
    b) User can apply voucher associated to it 
           (Route used  - /user/apply_user_voucher/user_id)
           Here it is validated that only after 24 hrs the voucher can be applied and same voucher cannot be applied multiple times
      
      
      
# How to Run?

Two ways are provided to use the voucher system:

1) By manually installing the dependencies:
   
   a) All the dependencies are present in requirements.txt which can be installed by
          
          pip3 install -r requirements.txt
   
   b) Running the Flask server (at localhost:5000)
           
           python3 voucherServer.py
      
    c) Running the dummy client created
          
          - python3 voucherClient.py
          - Once the client started , a prompt wil come asking whether you are admin or not 
          - If you are admin , press 'Y' to perform admin operations
          - If you are not admin , press 'N' and write your username (currently it is hardcoded with two users anshit and shiv) to perform user operations

NOTE: Since there are python3 dependencies which can affect user workspace, it is recommended to use python's virtualenv to install requirements.txt:
          
          pip3 install virtualenv
          virtualenv -p /usr/bin/python3.6 voucherenv
          source voucherenv/bin/activate 
          pip3 install -r requirements.txt
          To come out from virtualenv : deactivate
      
      
2) Using docker docker container Tar file provided with all installed dependencies:
 
    a) Load the docker tr file to extract the image:
              
        docker load --input voucher_service.tar.gz
      
    b) Run the container in detatched mode( So that falsk server wil keep running)
       
        docker run -d  -t --name voucherDemo -p 5000:80  $imageid 
        NOTE: You can check the $imageid using "docker images"
       
    c) Move inside the container to make use of dummy client:
       
        docker exec -it voucherDemo /bin/bash
        cd /voucher
        python3 voucherClient.py
        - Once the client started , a prompt wil come asking whether you are admin or not 
            - If you are admin , press 'Y' to perform admin operations
            - If you are not admin , press 'N' and write your username (currently it is hardcoded with two users anshit and shiv) to perform user operations

 # Why using this voucher service?
 
 1) The reason for using it because all te validations and logic is provided by the server, and client(front-end) need not perform any operation. Its task is only to querry the server with correct Route , and nothing else.
 
 
 # Limitations:
 
 1) No Database is provided with this, but soon mongodb/postgres will be used
 2) Error/Exception handling is missing, wich will be corected soon
 3) No Frontend is provided as an example, but soon using REactjs, it will be included
 4) No Scaling is added yet, but through Microservices and Kubernetes cluster , it will be added
 5) Optimisation needs to be done


# How to integrae this with Postgres?

1) Vouchers table operation:
    
    a) Creating voucher table:
        
       CREATE TABLE voucher (
       voucher_id serial PRIMARY KEY,
       voucher_code VARCHAR(50) UNIQUE NOT NULL,
       voucher_description VARCHAR(50) NOT NULL,
       voucher_start_time VARCHAR(50) NOT NULL,
       voucher_expiry_time VARCHAR(50) NOT NULL,
       voucher_count INTEGER NOT NULL
        );

    b) Inserting elements in table
      
        INSERT INTO voucher (voucher_code, voucher_description, voucher_start_time, voucher_expiry_time, voucher_count) 
        VALUES ('NETFLIX', 'Get free subscription', '2021-06-06', '2021-09-09', 12);

        INSERT INTO voucher (voucher_code, voucher_description, voucher_start_time, voucher_expiry_time, voucher_count) 
        VALUES ('AMAZON', 'Get free subscription of amazon', '2021-05-05', '2021-05-05', 12);
       
     c) SELECT all elements from table

        SELECT * FROM voucher;
        
     d) SELECT only those elements which are not yet expired and has count > 0

        SELECT * FROM voucher
        WHERE TO_TIMESTAMP(voucher_expiry_time, 'YYYY') <= CURRENT_DATE AND voucher_count > 0;
        
     e) Edit voucher
      
        UPDATE voucher 
        SET voucher_description = 'Get Subscription of Netflix'
        WHERE voucher_id = 1;
       
     f) DELETE voucher
     
        DELETE FROM voucher
        WHERE voucher_code = 'NETFIX'
        
        
2) User Table 

     a) Creating Users table
    
    	  CREATE TABLE Users (
        user_id serial PRIMARY KEY,
        user_name VARCHAR(50) NOT NULL
        );

     b) Get all Users
    
        INSERT INTO Users (user_name) 
        VALUES ('anshit'),('shiv');
      
3) User_voucher Table
    
     a) Creating table
        
        CREATE TABLE uservoucher (
        user_voucher_id serial PRIMARY KEY,
        user_id INTEGER REFERENCES Users(user_id),
        voucher_id INTEGER REFERENCES voucher(voucher_id) ON DELETE CASCADE,
        is_used BOOLEAN ,
        last_used_date VARCHAR(50) NOT NULL
        );

4) Issuee Voucher
   
     a) Adding the user realted voucher in user_voucher table
   
        INSERT INTO uservoucher(* FROM _id, voucher_id , is_used, last_used_date) 
        VALUES (1, 1, FALSE, 'N/A' );
        
     b) Checking whether that voucher to that user is already exist(If it exist then above point will not done)
      
        SELECT * FROM uservoucher
        WHERE user_id = 1 AND voucher_id = 1

     c) Once voucher is issued to user the voucher count of that vouche_id is reduced by 1

        UPDATE voucher 
        SET voucher_count = voucher_count - 1
        WHERE voucher_id = 1

5) List User associated Vouchers (Only available One)
      
        SELECT voucher_code,voucher_description
        FROM uservoucher
        INNER JOIN voucher ON uservoucher.voucher_id = voucher.voucher_id
        WHERE is_used=false AND user_id = 1 AND 
        TO_TIMESTAMP(voucher.voucher_expiry_time,'YYYY') > CURRENT_DATE AND  
        TO_TIMESTAMP(voucher.voucher_start_time, 'YYYY') < CURRENT_DATE 
  
6) Apply Voucher
    
        UPDATE uservoucher 
        SET is_used = true , last_used_date = CAST(CURRENT_DATE AS VARCHAR(50))
        WHERE user_id = 1 AND voucher_id =1

   To check whether the applying voucher is new one or lready used
    
        SELECT is_used FROM uservoucher
        WHERE user_id = 1 AND voucher_id =1

    To check whether user is applying voucher after 24 hrs or not
        
        SELECT last_used_date FROM uservoucher
        WHERE TO_TIMESTAMP(last_used_date, 'YYYY') <= CURRENT_DATE
        
        
