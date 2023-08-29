import psycopg2
import datetime as dt
db = psycopg2.connect(host = 'localhost',user = 'postgres',password='',port = 5432,database = 'ATM')
hema = db.cursor()

hema.execute('''create table if not exists bankdetails(
account_no varchar,
acc_holder varchar,
debit_pin varchar,
balance float);
''');
db.commit()

hema.execute('''insert into bankdetails(account_no, acc_holder, debit_pin, balance)
values 
('1234567890','hemalatha','1234',250000),
('2345678901','aswin','2234',100000),
('3456789012','sivagami','3234',50000),
('4567890123','ashutosh','4234',60000),
('5678901234','sarvesh','5234',70000),
('6789012345','harish','6234',80000);''')
db.commit()"""

hema.execute('''create table if not exists bankoper(
account_no varchar,
acc_holder varchar,
prevbal float,
amount float,
currentbal float,
dateoftxn varchar);''')
db.commit()

while True:
    print("____________________________Welcome to ABC Bank____________________________")
    ac_num = input("Enter your account number: ")
    pin = input("Enter your pin: ")
    loop_start = dt.datetime.now()
    while True:
        hema.execute("SELECT * FROM bankdetails WHERE account_no = %s", (ac_num,))
        data = hema.fetchone()
        if data[0] == ac_num and data[2] == pin:
            current_loop = dt.datetime.now()
            if (int(loop_start.minute) + 1) <= int(current_loop.minute):
                print("Connection timed out")
                break
            else:
                oper = input("Select\n\t1 Balance Details\n\t2 Cash Withdrawal\n\t3 Ministatement\n\t4 Password Change\n\t5 Clear\n")
                if oper =="1":
                    print("Balance is ",data[3])
                if oper =="2":
                    amount = float(input("Enter the amount to be withdrawn:\t"))
                    if data[3] >= amount:
                        print("Cash successfully withdrawn")
                        now = dt.datetime.now()
                        curr_bal =float(data[3] - amount)
                        hema.execute("insert into bankoper values(%s,%s,%s,%s,%s,%s)",(ac_num,data[1],str(data[3]),str(curr_bal),str(amount),now))
                        db.commit()
                        hema.execute("UPDATE bankdetails SET balance = %s WHERE account_no = %s", (curr_bal, ac_num))
                        db.commit()
                    else:
                        print("Insufficient balance \nUnable to process your request")
                if oper =="3":
                    print ("Ministatement Generation")
                    print("Date_of_txn\t\t\tDescription\tTxn_amount\tBalance_in_cr")
                    hema.execute("SELECT * FROM bankoper WHERE account_no = %s ORDER BY dateoftxn DESC LIMIT 7",(ac_num,))
                    output = hema.fetchall()
                    history  = []         
                    for i in output:
                        history.append(i)
                    history = history[::-1]
                    for i in range(len(history)):
                        print(f"{history[i][5]}\tCash Wdl\t{history[i][4]}\t\t{history[i][3]}")
                if oper =="4":
                    pin = input("Enter your Current pin: ")
                    if data[2] == pin:
                        new_pin = input("Enter your new pin: ")
                        confirm_new_pin = input("Confirm your new pin: ")
                        hema.execute("UPDATE bankdetails SET debit_pin = %s WHERE account_no = %s", (new_pin, ac_num))
                        db.commit()
                        pin = new_pin
                        print("Password Changed Successfully")
                    else:
                        print("Incorrect Pin kindly retry")
                        break

                if oper == "5":
                    break
        else:
            print("Invalid Credentials try again")
            break
