import json
import numpy as np
import os
import sys

# Before starting anything we check if our database exists so we can store data if not then make it
def checkFiles():

    path = os.path.dirname(os.path.realpath(__file__))

    if not bool(os.path.isfile(path+"/OperationList.txt")):
        open(path + "/OperationList.txt","w").close()

    if not bool(os.path.isfile(path+"/DomainList.txt")):
        open(path + "/DomainList.txt","w").close()


    if not bool(os.path.isfile(path+"/TypeList.txt")):
        open(path + "/TypeList.txt","w").close()


    if not bool(os.path.isfile(path+"/UserList.txt")):
        open(path + "/UserList.txt","w").close()

    return
        
checkFiles();


# Users
Users = {}

Domain =[]

#Domain
tempD = {}

# Types
Type = {}

# Operation 
Operations = []

# Flag for printing
printFlag = 0;


# DESIGN IS DIVIDED INTO 4 PARTS 

# PART 1- USERS
def loadUsers():
    global Users
    with open ("UserList.txt" , "r+") as f:
        if f.read(1):
            Users = json.load(open("UserList.txt"))
        else:
            return
        
loadUsers();


def loadDomain():
    global Domain
    global tempD
    
    with open ("DomainList.txt" , "r+") as f:
        if f.read(1):
            tempD = json.load(open("DomainList.txt"))
        else:
            return

        
loadDomain();


def loadType():
    global Type

    with open ("TypeList.txt" , "r+") as f:
        if f.read(1):
            Type = json.load(open("TypeList.txt"))
        else:
            return


loadType();



def loadOperations():
    global Operations
    
    with open ("OperationList.txt" , "r+") as f:
        if f.read(1):
            f.seek(0);

            # reading file line by line (Even indexes has permissions(view,delete..) and Odd indexes have domain-type)
            lines = f.readlines();

            permissions = (lines[::2]) 
            domain_type = (lines[1::2])
            
            for i in range(len(permissions)):
                Operations.append([permissions[i].strip(), domain_type[i].strip()])                

        else:
            return
        

loadOperations();





def authenticate(Username, Password):
    global Users
    if Username in Users and Password == Users[Username]:
        if printFlag == 0:
            print("Success")
        return 1
    elif Users.has_key(Username):
        if printFlag == 0:
            print("Error: bad password")
        return 0
    else:
        if printFlag == 0:
            print("Error: no such user")
        return -1
    
    

def addUser(Username, Password):
    
    global Users
    global printFlag
    
    if Username == "":
        print("Error: username missing")
        return

    if bool(Users):
        if Username in Users:
            print("Error: user exists")
            return
            
        printFlag = -1;
        if(authenticate(Username, Password) == 1):
            print("Error: user exists")
            printFlag = 0;
            return
        printFlag = 0;
            

    newUser = {Username:Password}
    Users.update(newUser)
    json.dump(Users, open("UserList.txt",'w'))
    print("Success")
    return
            


# PART 2- DOMAIN

def setDomain(Username, domainName):
    global Domain
    global printFlag

    if not domainName:
        print("Error: missing domain")
        return
    
    if (bool(Users)):
        printFlag = -1;
        if ((authenticate(Username, "----") != 1) and (authenticate(Username, "----") != 0)):
            print("Error: no such user")
            printFlag = 0;
            return
        printFlag = 0;
        
    for i in range(len(Domain)): 
        if Domain[i][0] == domainName:
            print("Found Domain");
            Domain[i].append(Username)
            return
        
    Domain.append([domainName, Username])
    json.dump(Domain, open("DomainList.txt",'w'))
    print("Success");
    return



# setDomain
def temp(Username, domainName): 
    
    global tempD
    global printFlag

    if not domainName:
        print("Error: missing domain")
        return

    
    if (bool(Users)):
        printFlag = -1;
        if ((authenticate(Username, "----") != 1) and (authenticate(Username, "----") != 0)):
            print("Error: no such user")
            printFlag = 0;
            return
        printFlag = 0;


    # check if both domain and key exists IMP

    if tempD.has_key(domainName):
        pp = []
        pp = tempD[domainName]
        pp.append(Username)
        tempD[domainName] = pp
        json.dump(tempD, open("DomainList.txt",'w'))
        print("Success");
        return

    if(Username == "dontadd"):
        Username = "";
    
    pp2 = []
    pp2.append(Username)
    newUser = {domainName:pp2}
    tempD.update(newUser)
    json.dump(tempD, open("DomainList.txt",'w'))
    print("Success");
    return




def domainInfo(domainName):
    global tempD

    if(domainName == ""):
        print("Error: missing domain");
        return
    
    if tempD.has_key(domainName):
        pp = []
        pp = tempD[domainName]
        for i in pp:
            print(i);
        return
    return


    

# PART 3- TYPES
def setType(objectName, typeName):

    if(objectName == "" or typeName == ""):
        print("Error: invalid arguments");
        exit();
        
    
    global Type
    global printFlag

    if not typeName:
        print("Error: missing type")
        return


    if Type.has_key(typeName):
        pp = []
        pp = Type[typeName]
        pp.append(objectName)
        Type[typeName] = pp
        json.dump(Type, open("TypeList.txt",'w'))
        print("Success");
        return


    if(objectName == "dontadd"):
        objectName = "";
        
    pp2 = []
    pp2.append(objectName)
    newUser = {typeName:pp2}
    Type.update(newUser)
    json.dump(Type, open("TypeList.txt",'w'))    
    print("Success");
    return



    
def typeInfo(typeName):
    global Type

    if typeName == "":
        print("Error: invalid argument");
        exit();
    
    if Type.has_key(typeName):
        pp = []
        pp = Type[typeName]
        for i in pp:
            if(i != ""):
                print(i);
            
    return






# PART 4- ACCESS PERMISSIONS

def addAccess(operationName, domain_name, type_name):

    global Type
    global TempD
    
    if domain_name == "":
        print("Error: missing domain");
        exit();

    if type_name == "":
        print("Error: missing type");
        exit();

    if operationName == "":
        print("Error: missing operation");
        exit();
    
    global Operations
    global Type
    global tempD

    if not Type.has_key(type_name):
        setType("dontadd", type_name);

    if not tempD.has_key(domain_name):
        setDomain("dontadd", domain_name);
        
    Operations.append([operationName, domain_name + "-" + type_name])

    with open('OperationList.txt', 'w') as f:
        for i in range(len(Operations)):
            f.write(Operations[i][0] + "\n");
            f.write(Operations[i][1] + "\n");

    print("Success");
    return



def canAccess(operation, user, objectName):

    global tempD
    global Type
    
    
    userPresentInDomains = []

    for key, value in tempD.items():
        if user in value:
            userPresentInDomains.append(key);

    objectsPresentInTypes = []

    for key, value in Type.items():
        if objectName in value:
            objectsPresentInTypes.append(key);

    access = []
    for	i in range(len(userPresentInDomains)):
        for j in range(len(objectsPresentInTypes)):
            access.append( userPresentInDomains[i] + "-" + objectsPresentInTypes[j])
            
            
    for i in range(len(Operations)):
        if (Operations[i][0] == operation):
            for j in range(len(access)):
                if (Operations[i][1] == access[j]):
                    print("Success");
                    return

    print("Error: access denied");
    return

def error():
    print("Error: invalid number of arguments");
    exit();

def runner():

    if(len(sys.argv) < 3):
        print("Error: invalid number of arguments");
        exit();
    elif (len(sys.argv) >= 3):

        if(sys.argv[1] == "AddUser"):
            if(len(sys.argv) != 4):
                error();
                
            addUser(sys.argv[2], sys.argv[3]);
            exit();

        elif (sys.argv[1] == "Authenticate"):
            if(len(sys.argv) != 4):
                error();
            authenticate(sys.argv[2], sys.argv[3]);
            exit();

        elif(sys.argv[1] == "SetDomain"):
            if(len(sys.argv) != 4):
                error();
                
            temp(sys.argv[2], sys.argv[3]);
            exit();

        elif(sys.argv[1] == "DomainInfo"):
            if(len(sys.argv) != 3):
                error();
            domainInfo(sys.argv[2]);
            exit();

        elif(sys.argv[1] == "SetType"):
            if(len(sys.argv) != 4):
                error();
            setType(sys.argv[2], sys.argv[3]);  
            exit();

        elif(sys.argv[1] == "TypeInfo"):
            if(len(sys.argv) != 3):
                error();
            typeInfo(sys.argv[2]);        
            exit();

        elif(sys.argv[1] == "AddAccess"):
            if(len(sys.argv) != 5):
                error();
            addAccess(sys.argv[2], sys.argv[3], sys.argv[4]);
            exit();
            
        elif(sys.argv[1] == "CanAccess"):
            if(len(sys.argv) != 5):
                error();
            canAccess(sys.argv[2], sys.argv[3], sys.argv[4]);
            exit();

        else:
            print("Error: invalid number of arguments");
            exit();


runner();
