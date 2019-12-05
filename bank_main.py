import cx_Oracle
from customer import customer
import datetime
from fileinput import close
now = datetime.datetime.now()
from account import *

#global customer
#global account


def closedAccountHistory():
    con = cx_Oracle.connect('mbank/bank987@127.0.0.1/XE')
    cur = con.cursor()

    cur.execute("SELECT * FROM accounts where status='Deactive' ");
    
    results = cur.fetchall()
    
    if(int(cur.rowcount)>0):
        print("<< List of closed Account History >> ");
        print("acc_no. "+"Status ")
        for row in results:
            acc_no = row[0]
            closed = row[6]
            print(acc_no," ",closed)

    else:
        print("<< No Closed accounts >>")

    con.commit()
    con.close()

def FDReport():
    cust_id = input("Enter Customer_Id : ")
    con = cx_Oracle.connect('mbank/bank987@127.0.0.1/XE')
    cur = con.cursor()
    
    cur.execute("select acc_no,amount,terms from fixed_deposit where cust_id = :cust_id",(cust_id))
    results = cur.fetchall()
    if(int(cur.rowcount)>0):
        print('FD Report for customer : ',cust_id)
        print("acc_no"," ","amount"," ","terms")
        for row in results:
            acc_no = row[0]
            amount = row[1]
            terms = row[2]
            print(acc_no," ",amount," ",terms)
    else:
        print("N.A")
    con.commit()
    con.close()

def  FDReportwithAnotherCustomer():
    cust_id = input("Enter Customer_id : ")
    con = cx_Oracle.connect('mbank/bank987@127.0.0.1/XE')
    cur = con.cursor()
    
    cur.execute("select * from fixed_deposit where amount > (select sum(amount) from fixed_deposit where cust_id =:cust_id)",(cust_id))
    results = cur.fetchall()
    if(int(cur.rowcount)>0):
        print('FD Report with respect to  customer :',cust_id)
        print("customer_no"," ","acc_no"," ","amount"," ","terms")
        for row in results:
            cust_no = row[4]
            acc_no = row[1]
            amount = row[2]
            terms = row[3]
            print(cust_no," ",acc_no," ",amount," ",terms)
    else:
        print("NA")
    con.commit()
    con.close()

def  FDReportwithamount():
    amnt = int(input("Enter Amount : "))
    con = cx_Oracle.connect('mbank/bank987@127.0.0.1/XE')
    cur = con.cursor()
    
    cur.execute("select fd.cust_id,cd.cust_fname,cd.cust_lname,fd.amount from fixed_deposit fd inner join customer_details cd on fd.cust_id=cd.cust_id where fd.amount = :amnt",{"amnt":amnt})
    results = cur.fetchall()
    if(int(cur.rowcount)>0):
        print('FD Report with amount :',amnt)
        print("customer_no"," ","First Name"," ","Last Name"," ","amount")
        for row in results:
            cust_no = row[0]
            fname = row[1]
            lname = row[2]
            amount = row[3]
            print(cust_no," ",fname," ",lname," ",amount)
    else:
        print("NA")
    con.commit()
    con.close()

def loanReport():
    cust_id = input("Enter Customer_id : ")
    con = cx_Oracle.connect('mbank/bank987@127.0.0.1/XE')
    cur = con.cursor()
    
    cur.execute("select acc_no,amount,terms from loan where cust_id = :cust_id",(cust_id))
    results = cur.fetchall()
    if(int(cur.rowcount)>0):
        print('loan Report for customer : ',cust_id)
        print("acc_no"," ","amount"," ","terms")
        for row in results:
            acc_no = row[0]
            amount = row[1]
            terms = row[2]
            print(acc_no," ",amount," ",terms)
    else:
        print("N.A")
    con.commit()
    con.close()

def  loanReportwithAnotherCustomer():
    cust_id = input("Enter Customer_id")
    con = cx_Oracle.connect('mbank/bank987@127.0.0.1/XE')
    cur = con.cursor()
    
    cur.execute("select * from loan where amount > (select sum(amount) from loan where cust_id =:cust_id)",(cust_id))
    results = cur.fetchall()
    if(int(cur.rowcount)>0):
        print('Loan Report with respect to  customer :',cust_id)
        print("customer_no"," ","acc_no"," ","amount"," ","terms")
        for row in results:
            cust_no = row[4]
            acc_no = row[1]
            amount = row[2]
            terms = row[3]
            print(cust_no," ",acc_no," ",amount," ",terms)
    else:
        print("NA")
    con.commit()
    con.close()

def  loanReportwithamount():
    amnt = input("Enter Amount : ")
    con = cx_Oracle.connect('mbank/bank987@127.0.0.1/XE')
    cur = con.cursor()
    
    cur.execute("select l.cust_id, cd.cust_fname,cd.cust_lname,l.amount from loan l inner join customer_details cd on l.cust_id=cd.cust_id where l.amount = :amnt",{"amnt":amnt})
    results = cur.fetchall()
    if(int(cur.rowcount)>0):
        print('Loan Report with amount :',amnt)
        print("customer_no"," ","First Name"," ","Last Name"," ","amount")
        for row in results:
            cust_no = row[0]
            fname = row[1]
            lname = row[2]
            amount = row[3]
            print(cust_no," ",fname," ",lname," ",amount)
    else:
        print("NA")
    con.commit()
    con.close()

def FDLoanReportwithamount():
    con = cx_Oracle.connect('mbank/bank987@127.0.0.1/XE')
    cur = con.cursor()
    
    cur.execute("select cd.cust_id,cd.cust_fname,cd.cust_lname,fd.sum_fixed, l.sum_loan from customer_details cd inner join (select sum(amount) as sum_fixed, cust_id from fixed_deposit group by cust_id) fd on fd.cust_id = cd.cust_id inner join (select sum(amount) as sum_loan, cust_id from loan group by cust_id) l on l.cust_id = cd.cust_id")
    results = cur.fetchall()
    if(int(cur.rowcount)>0):
        print('FD Loan Report with amount ')
        print("customer_no"," ","First Name"," ","Last Name"," ","sum fixed deposit amount"," ","sum loan amount")
        for row in results:
            cust_no = row[0]
            fname = row[1]
            lname = row[2]
            famount = row[3]
            lamount = row[4]
            if(lamount>famount):
                print(cust_no," ",fname," ",lname," ",famount," ",lamount)
    else:
        print("NA")
    con.commit()
    con.close()

def noFDReport():
    con = cx_Oracle.connect('mbank/bank987@127.0.0.1/XE')
    cur = con.cursor()
    
    cur.execute("select cust_id,cust_fname,cust_lname from customer_details where cust_id not in (select distinct(cust_id) from fixed_deposit)")
    results = cur.fetchall()
    if(int(cur.rowcount)>0):
        print('No FD Report')
        print("customer_no"," ","First Name"," ","Last Name")
        for row in results:
            cust_no = row[0]
            fname = row[1]
            lname = row[2]
            
            #if(lamount>famount):
            print(cust_no," ",fname," ",lname)
    else:
        print("NA")
    con.commit()
    con.close()

def noLoanReport():
    con = cx_Oracle.connect('mbank/bank987@127.0.0.1/XE')
    cur = con.cursor()
    
    cur.execute("select cust_id,cust_fname,cust_lname from customer_details where cust_id not in (select distinct(cust_id) from  loan)")
    results = cur.fetchall()
    if(int(cur.rowcount)>0):
        print('No Loan Report')
        print("customer_no"," ","First Name"," ","Last Name")
        for row in results:
            cust_no = row[0]
            fname = row[1]
            lname = row[2]
            
            #if(lamount>famount):
            print(cust_no," ",fname," ",lname)
    else:
        print("NA")
    con.commit()
    con.close()

def noLoanFD():
    con = cx_Oracle.connect('mbank/bank987@127.0.0.1/XE')
    cur = con.cursor()
    
    cur.execute("select cust_id,cust_fname,cust_lname from customer_details where cust_id not in (select distinct(fd.cust_id) from fixed_deposit fd inner join loan on fd.cust_id = loan.cust_id)")
    results = cur.fetchall()
    if(int(cur.rowcount)>0):
        print('No FD Loan Report ')
        print("customer_no"," ","First Name"," ","Last Name")
        for row in results:
            cust_no = row[0]
            fname = row[1]
            lname = row[2]
            
            #if(lamount>famount):
            print(cust_no," ",fname," ",lname)
    else:
        print("NA")
    con.commit()
    con.close()

def signUp():
    print(' << user sign up >> ')
    First_Name = input("Enter First Name : ")
    Last_Name = input("Enter Last Name : ")
    Address_line1 = input("Enter Your Address line 1 : ")
    Address_line2 = input("Enter Your Address line 2 : ")
    City = input("Enter your city : ")
    Pincode = int(input("Enter Pincode : "))
    State = input("Enter state : ")
    while True:
        password = input("Enter password : ")
        if len(password) < 8:
            print("<< password is too short >>")
        else:
            break
    cust = customer("0",First_Name,Last_Name,Address_line1,Address_line2,Pincode,City,State,password)
    cust_id = cust.signUp()
    openAccount(cust_id)
    
def openAccount(cust_id):
    
    print("1.Saving account")
    print("2.Current account")
    print("3.Fixed Deposit account")
    print()
    type = input("Enter your new account type : ")
    if(type=='1'):
        acc = savingaccount(now.strftime("%Y-%m-%d"),'0',0,cust_id,0)
    elif(type=='2'):
        acc = currentaccount(now.strftime("%Y-%m-%d"),'0',5000,cust_id)
    elif(type=='3'):
        terms = 0
        while True:
            terms = int(input("Enter Number of terms : "))
            if terms >= 12:
                break
            else:
                print("<< Minimum Deposit term is 12 >>")
        while True:
            amnt = int(input("Enter Amount : "))
            if amnt >= 0:
                break
            else:
                print("<< Minimum FD balance should be 1000 >>")
        acc = fixedaccount(now.strftime("%Y-%m-%d"),'0',0,cust_id,amnt,terms)
    fix_acc_no = acc.openAccount()
    

def getAccount():
    global acc
    acc_no = input("Enter Account number : ")
    con = cx_Oracle.connect('mbank/bank987@127.0.0.1/XE')
    cur = con.cursor()
    cur.execute("SELECT * FROM account where customer_no=:custid and acc_no=:accno",(cust_id,acc_no))
    results = cur.fetchall()
    if int(cur.rowcount)>0:
        for row in results:
            acc_type = row[1]
            openDt = row[2]
    con.commit()
    con.close()

def check():
    con = cx_Oracle.connect('mbank/bank987@127.0.0.1/XE')
    cur = con.cursor()
    cur.execute("select * from saving_account where acc_no = :acc_no and cust_id = :cust_id",(acc_no,cust_id))
    result = cur.fetchall()
    if int(cur.rowcount)>0:
        con.commit()
        con.close()
        return True
    else:
        con.commit()
        con.close()
        return False


def login():
    global cust
    global cust_id
    global acc
    global loan
    global acc_no
    login_count = 0
    returnvalue  = True
    login = True
    con = cx_Oracle.connect('mbank/bank9874@127.0.0.1/XE')
    cur = con.cursor()
    cur.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD'")
    cust_id = input("Enter Customer_ID : ")
    acc_no = input("Enter Account No.: ")
    while login:
        if login_count > 3:
            cur.execute("update accounts set status='Locked' , closing_date= :closeing_date where acc_no = :acc_no and cust_id=:cust_id",(now.strftime("%Y-%m-%d"),acc_no,cust_id))
            print("account id : "+acc_no+" customer_id : "+cust_id+" is locked ")
            print("<< Please contact branch administrator >>")
            login = False
            
            break
        password = input("Enter Password : ")
        cur.execute("SELECT * FROM customer_details where cust_id=:custid and cust_password=:cust_pass",(cust_id,password))
        results = cur.fetchall()

        if(int(cur.rowcount)>0):
            for row in results:
                f_name = row[1]
                l_name = row[2]
                password = row[3]
                addrline1 = row[4]
                addrline2 = row[5]
                pincode = row[6]
                city = row[7]
                state = row[8]
            
                cust = customer(cust_id,f_name,l_name,addrline1,addrline2,pincode,city,state,password)
            
            login = False
            cur.execute("SELECT * FROM accounts where cust_id=:custid and acc_no = :acc_no",(cust_id,acc_no))
            results = cur.fetchall()
            
            if(int(cur.rowcount)>0):
                for row in results:
                    acc_no = row[0]
                    acc_type = row[1]
                    openedDate = row[2]
                    balance = row[3]
                    closedDate = row[5]
                    status = row[6]
                
                if(status == 'Active'):
                    if(acc_type=='saving'):
                        cur.execute("""SELECT * FROM saving_account where acc_no=:acc_no""",{"acc_no":acc_no})
                        results = cur.fetchall()
                    
                        if(int(cur.rowcount)>0):
                            for row in results:
                                withdrawcount = row[1]
                            acc = savingaccount(openedDate,acc_no,balance,cust_id,withdrawcount)
                    elif(acc_type=='current'):
                        acc = currentaccount(openedDate,acc_no,balance,cust_id)
                    else:
                        acc = fixedaccount(openedDate,acc_no,balance,cust_id,0,0)
                    print("Successfully login ")
                    print("welcome "+f_name+" "+l_name)
                else:
                    print('<< Your account Deactive/Locked >>')
                    print("<< Please contact branch administrator >>")
                    returnvalue = False
        else:
            returnvalue = False
            print('<< wrong user name or password >>')
            login_count +=1
        
        
    con.commit()
    con.close()
    return returnvalue

Quit = 1
while Quit==1:        
    print ("===========================================")
    print("1.Sign UP (New Customer)")
    print("2.Login (Existing Customer)")
    print("3.Admin Sign in")
    print("4.Quit")
    print ("===========================================")
    print()
    ch = input ("Enter your choice : ")
    if ch == '1':
        signUp()
    elif ch == '2':
        if(login()):
            option2 = 1
            while option2 == 1:
                print ("===========================================")
                print("1.Address Change")
                print("2.Open New Account")
                print("3.Money Deposit")
                print("4.Money Withdrawal")
                print("5.Print Statement")
                print("6.Transfer Money")
                print("7.Account Closure")
                print("8.Avail Loan")
                print("0.Customer Logout")
                
                print("==========================================")
                print()
                choice = input ("Enter your choice : ")
                if choice == '1':
                    print("in address change ")
                    cust.changeAddress()
                elif choice == '2':
                    openAccount(cust_id)
                elif choice == '3':
                    amnt = int(input("Enter Deposit Amount : "))
                    acc.deposit(amnt)
                elif choice == '4':
                    
                    con = cx_Oracle.connect('mbank/bank987@127.0.0.1/XE')
                    cur = con.cursor()
                    cur.execute("select acc_type from accounts where acc_no = :acc_no and cust_id = :cust_id",(acc_no,cust_id))
                    results = cur.fetchall()
                    for row in results:
                        if row[0] == 'fixed':
                            print("<< You cannot withdraw money in fixed deposit >>")
                        else:
                            amnt = int(input("Enter Withdraw Amount : "))
                            acc.withdraw(amnt)

                    con.commit()
                    con.close()
                    
                elif choice == '5':
                    acc.printStatement()
                elif choice == '6':
                    amnt = int(input("Enter Transfer Amount : "))
                    acc_no = input("Enter Transfer Account No. : ")
                    acc.transfer(amnt,acc_no)
                elif choice == '7':
                    acc.accountClosure()
                elif choice == '8':
                    
                    if(check()):
                        amnt = int(input("Enter Loan Amount : "))
                        term = int(input("Enter Repayment Term : "))
                        con = cx_Oracle.connect('mbank/bank987@127.0.0.1/XE')
                        cur = con.cursor()
                        cur.execute("select balance from accounts where acc_no = :acc_no and cust_id = :cust_id",(acc_no,cust_id))
                        results = cur.fetchall()
                        for row in results:
                            
                            if(amnt < (2*row[0])):
                                cur.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD'")
                                acc = loan(now.strftime("%Y-%m-%d"),acc_no,0,cust_id,amnt,term)
                                loan_acc = acc.openAccount();
                                print("Loan Account No. : ",loan_acc)
                            else:
                                print("<< Amount request Exceeded >>")
                        con.commit()
                        con.close()
                    else:
                        print("<< current account is not an saving account >>")
                    
                elif choice == '0':
                    print('Successfully logout')
                    option2 = 0    
    elif ch == '3':
        username = input("Enter Username : ")
        upass = input("Enter Password : ")
        if(username=='admin' and upass=='admin'):
            option2 = 1
            while option2 == 1:
                print ("===========================================")
                print("1.Print Closed Account History")
                print("2. FD Report of a customer")
                print("3.FD report of customer vis-a-vis another customer")
                print("4. FD report w.r.t. a particular FD amount")
                print("5. Loan Report of a customer")
                print("6.Loan report of customer vis-a-vis another customer")
                print("7. Loan report w.r.t. a particular Loan amount")
                print("8.Loan - FD Report of Customers")
                print("9.Report of customer who are yet to avail a loan")
                print("10.Report of customer who are yet to open an FD account")
                print("11.Report of customer who neither have a loan nor an FD account with bank")
                print("0.Admin logout")
                print ("===========================================")
                print()
                choice = input ("Enter your choice : ")
                if choice == '1':
                    closedAccountHistory()
                elif choice == '2':
                    FDReport()
                elif choice == '3':
                    FDReportwithAnotherCustomer()
                elif choice == '4':
                    FDReportwithamount()
                elif choice == '5':
                    loanReport()
                elif choice == '6':
                    loanReportwithAnotherCustomer()
                elif choice == '7':
                    loanReportwithamount()
                elif choice == '8':
                    FDLoanReportwithamount()
                elif choice == '9':
                    noLoanReport()
                elif choice == '10':
                    noFDReport()
                elif choice == '11':
                    noLoanFD()
                elif choice == '0':
                    print('Successfully logout')
                    option2 = 0  
        print("Thanks for using this system")               
    elif ch == '4':
        Quit = 0
        print("Thanks for using this system")


