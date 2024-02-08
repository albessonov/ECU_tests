import os
print("ECU test shell")
print("type 'all' to run all tests in order")
print("type 'q' to exit")	
while True:
 command = input("Which test would you like to run?(enter number): ")
 match command.split():
    case ["1"]:  
        print("Starting test1")
        os.system('pytest /home/albessonov/tests/test_1.py') 
    case ["2"]:
        print("Starting test2")  
        os.system('pytest /home/albessonov/tests/test_2.py') 
    case ["3"]:
        print("Starting test3")  
        os.system('pytest /home/albessonov/tests/test_3.py') 
    case ["4"]:
        print("Starting test4")
        os.system('sudo -E python3 /home/albessonov/tests/test_4.py') 
    case ["5"]:
        print("Starting test5")  
        os.system('sudo -E python3 /home/albessonov/tests/test_5.py') 
    #case ["6"]:
        #print("Starting test6")  
        #os.system('sudo -E python3 /home/albessonov/tests/test_6.py')''' 
    case ["7"]:
        print("Starting test7")  
        os.system('pytest /home/albessonov/tests/test_7.py')  
    case ["8"]:
        print("Starting test8")  
        os.system('pytest /home/albessonov/tests/test_8.py')
    case ["all"]:
        print("Starting test1") 
        os.system('pytest /home/albessonov/tests/test_1.py') 
        print("Starting test2")
        os.system('pytest /home/albessonov/tests/test_2.py')
        print("Starting test3")  
        os.system('pytest /home/albessonov/tests/test_3.py')
        print("Starting test4") 
        os.system('sudo -E python3 /home/albessonov/tests/test_4.py')
        print("Starting test6")  
        os.system('sudo -E python3 /home/albessonov/tests/test_5.py')
        '''print("Starting test6")  
        os.system('sudo -E python3 /home/albessonov/tests/test_6.py')'''
        print("Starting test7")  
        os.system('pytest /home/albessonov/tests/test_7.py')
        print("Starting test8")  
        os.system('pytest /home/albessonov/tests/test_8.py')  
    case ["q"]:
        exit()                
    case _:  
        print("Unknown command")
