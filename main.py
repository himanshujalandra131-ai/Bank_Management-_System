import json
import random
import string
from pathlib import Path

class Bank:

    database='data.json'
    data=[]

    try:

        if Path(database).exists():

            with open(database) as fs:

                data=json.loads(fs.read())
        else:
             print("No such file exist")
    except Exception as err:

        print(f"An error Occured of {err}")

    @classmethod
    def __update(cls):
        with open(cls.database,'w') as fs:
            fs.write(json.dumps(Bank.data))

    @classmethod
    def __acountgenerater(cls):
        alpha= random.choices(string.ascii_letters,k=3)
        digit= random.choices(string.digits, k=3)
        spchar= random.choices("@#$%^&*",k=1)

        id=alpha+digit+spchar

        random.shuffle(id)

        return "".join(id)

    def creatAccount(self):
        info={
            "name": input("Tell your name:-"),
            "age":int(input("Tell your age:-")),
            "email":input("Enter your email:-"),
            "pin":int(input("Enter your 4 digit pin code")),
            "acNo":Bank.__acountgenerater(),
            "balace":0

        }
        if info['age']<18 or len(str(info['pin'])) !=4:
            print("Sorry your are not able to creat Account")
        else:
            print("Your Account is created succssfully!")
        for i in info:
            print(f"{i}: {info[i]}")

        print("please note down your Account number")
        Bank.data.append(info)
        Bank.__update()


    def depositemoney(self):
        accountnumber=input("Enter your account number:- ")
        pin=int(input("Enter your Pin code:- "))

        userdetail=[i for i in Bank.data if i['acNo']==accountnumber and i['pin']==pin]

        if userdetail==False:
            print("Sorry Account is not Found")
        else:
            diposite=int(input("How much money you want to diposite:- "))
            if diposite > 10000 and diposite < 0:
                print("Sorry this amount of diposite is not allow")

            else:
                userdetail[0]['balace']+=diposite

                Bank.__update()

                print("Amount diposited successfully!")

    def withdrawmoney(self):
        accountnum=input("Enter your Account number:- ")
        pin=int(input("Enter your pin number:- "))
        userdata=[i for i in Bank.data if i['acNo']==accountnum and i['pin']==pin]

        if userdata==False:
            print("Sorry User not found")
        else:

            amount=int(input("How much money you want to withraw:- "))
            if userdata[0]['balace'] < amount :
                print("YOu can't Withdraw this much amount")
            else:
                userdata[0]['balace']-=amount
                Bank.__update()
                print("Withdraw successfully! ")
    def Udetail(self):
        accountnum = input("Tell your acount number:- ")
        pin = int(input("Tell your Pin code:- "))

        userdetail = [i for i in Bank.data if i['acNo']==accountnum and i['pin']==pin]

        print("Your detail is \n \n")
        for i in userdetail[0]:
            print(f"{i} : {userdetail[0][i]}")

    def updatedetail(self):
        accountnum = input("Tell your acount number:- ")
        pin = int(input("Tell your Pin code:- "))
        
        userdetail = [i for i in Bank.data if i['acNo']==accountnum and i['pin']==pin]

        if userdetail == False:
            print("No such account found ")
        else:
            print("You cannot change your , Age, Account Number, Balance")
            print("Fill the details for change or leave it emplty if no change")

            newdata = {
                "name": input("ENter your name name:- "),
                "email":input("tell your email if you dont want so spik to enter:- "),
                "pin":input("tell your new pin code and code must be 4 digit only:- ")

            }
            if newdata['name']=="":
                newdata["name"]=userdetail[0]['name']
            if newdata['email']=="":
                newdata["email"]=userdetail[0]['email']
            if newdata['pin']=="":
                newdata["pin"]=userdetail[0]['pin']

            newdata['age']=userdetail[0]['age']
            newdata['acNo']=userdetail[0]['acNo']
            newdata['balace']=userdetail[0]['balace']

            if type(newdata["pin"])== str:
                newdata["pin"]= int(newdata["pin"])

            for i in newdata:
                if newdata[i]==userdetail[0][i]:
                    continue
                else:
                    userdetail[0][i]=newdata[i]
            Bank.__update()
            print("Detail Updated successfully !")

    def deletingacc(self):
         accountnum = input("Tell your acount number:- ")
         pin = int(input("Tell your Pin code:- "))
                
         userdetail = [i for i in Bank.data if i['acNo']==accountnum and i['pin']==pin]
        
         if userdetail == False:
                    print("No such account found ")
         else:
             check=input("Press y if you want delete your account and press n :- ")
             if check=="n" or check=="N":
                 print("Passed")
             else:
                 index=Bank.data.index(userdetail[0])
                 Bank.data.pop(index)

                 Bank.__update()
             print("Deleted Successfully! ")

        



user=Bank()

print("Press 1 for Creating Account")
print("Press 2 for Depositing money in your Account")
print("Press 3 for Withdrawing money to your  Account")
print("Press 4 for Detailing  Account")
print("Press 5 for Detail updating  Account")
print("Press 6 for Deleting Account")

check = int(input("Please tell a number:- "))

if check==1:
    user.creatAccount()

if check==2:
    user.depositemoney()

if check==3:
    user.withdrawmoney()

if  check==4:
    user.Udetail()

if check==5:
    user.updatedetail()

if check==6:
    user.deletingacc()