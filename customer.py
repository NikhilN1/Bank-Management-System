import cx_Oracle
class customer:
    def __init__(self,cus_id,c_fname,c_lname,line1,line2,pincode,city,state,password):
        self.cus_id = cus_id
        self.cus_fname = c_fname
        self.cus_lname = c_lname
        self.password = password
        self.line1 = line1
        self.line2 = line2
        self.pincode = pincode
        self.city = city
        self.state = state
    
    def verifyPass(self,cpass):
        if(self.password == cpass):
            return True
        else:
            return False

    def signUp(self):
        con = cx_Oracle.connect('mbank/bank987@127.0.0.1/XE')
        cur = con.cursor()
        cust_id = 0
        cur.execute("SELECT cust_id FROM customer_details")
        results = cur.fetchall()
        #print(results)
        print(cur.rowcount)
        if(int(cur.rowcount)>0):
            for row in results:
                cust_id = row[0]
        if(int(cust_id)==0):
            self.cus_id = 1
            cur.execute(""" insert into customer_details values(:cust_id, :cust_fname, :cust_lname, :cust_password, :cust_addr1, :cust_addr2, :cust_pincode, :cust_city, :cust_state
             )""",(self.cus_id,self.cus_fname,self.cus_lname,self.password,self.line1,self.line2,self.pincode,self.city,self.state))
        else:
            self.cus_id = int(cust_id) + 1
            cur.execute(""" insert into customer_details values(:cust_id, :cust_fname, :cust_lname, :cust_password, :cust_addr1, :cust_addr2, :cust_pincode, :cust_city, :cust_state
             )""",(self.cus_id,self.cus_fname,self.cus_lname,self.password,self.line1,self.line2,self.pincode,self.city,self.state))
        con.commit()
        con.close()
        print("customer id : ",self.cus_id)
        return  self.cus_id

    def changeAddress(self):
        print('inside address change',self.cus_id)
        Address_line1 = input("Enter Your Address line 1 : ")
        Address_line2 = input("Enter Your Address line 2 : ")
        City = input("Enter your city : ")
        Pincode = int(input("Enter Pincode : "))
        
        con = cx_Oracle.connect('mbank/bank987@127.0.0.1/XE')
        cur = con.cursor()
        cur.execute(""" update customer_details set cust_addr1=:cust_addr1,cust_addr2=:cust_addr2, cust_pincode=:cust_pincode, cust_city=:cust_city where cust_id =:cust_id""",(Address_line1,Address_line2,Pincode,City,self.cus_id))   
        if(int(cur.rowcount)>0):
            print("<< Successfully Updated >>")
        else:
            print("<< Oops..!! Problem in address update >>")
        con.commit()
        con.close()
 
    
