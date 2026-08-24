stock = {}
import time 
try:
    with open(r"C:\Users\Hello\Desktop\AUR-Training-26\task_2\subtask_1\stock.txt", "r") as f:
        for line in f:
            key, value = line.split(",")
            stock[key.lower()] = int(value)

    print(stock)

except Exception as e:
    with open(r"C:\Users\Hello\Desktop\AUR-Training-26\task_2\subtask_1\stock.txt", "r") as f:
       for item in stock:
          f.write(item +","+str(stock[item])+"\n")


name=list(stock.keys())
def savestock():
   f=open()
def showstock():
   for i in range(len(name)):
        print(i+1,name[i],stock[name[i]])
def addstock():
    showstock()
    item=input("\nEnter the stock name or ID: ")
    if item.isdigit():
     item_id=int(item)
     if 1 <= item_id <= len(name):
      item = name[item_id - 1]
     else:
       print("Invalid ID")
       return
       
    else:
     item=item.lower()
    try:
      amount = int(input("Enter how much to add to the stock: "))
    
      if amount < 0:
        print("Invalid amount")
        return
        
    
    except ValueError:
      print("Invalid amount")
      return
      
    if item in stock:
      stock[item]=stock[item]+amount
    else:
     stock[item]=amount
    savestock()
    print("Stock updated successfully!")
    print(item, stock[item])

def removesrock():
    showstock()
    item=input("\nEnter the stock name or ID: ")
    if item.isdigit():
     item_id=int(item)
     if 1 <= item_id <= len(name):
       item = name[item_id - 1]
     else:
      print("Invalid ID")
      return
    else:
      item=item.lower()
    try:
     amount = int(input("Enter how much to remove from the stock: "))
     if amount < 0:
      print("Invalid amount")
      return
    except ValueError:
      print("Invalid amount")
      return
    if item in stock:
      if stock[item]-amount>=0:
         stock[item]=stock[item]-amount
         savestock()
         print("Stock updated successfully!")
         print(item, stock[item])
      else:
         print("Amount Of Items Exceed Amount of Available Items")
    else:
               print("Invalid Item")


while(True):
       print("enter 1 to add stock\nenter 2 to remove stock\nenter 3 to show stock’s contents\nenter 4 to exit the program")
       choice=int(input("Enter Your Choice: "))
       if choice ==1:     
           addstock()    
       elif choice == 2:
           removesrock()
       elif choice == 3:
           showstock()
       elif choice==4:
           print("Existing...")
           time.sleep(2)
           print("ThankYou!,See You Later")
           break
       else: 
           print("Invalid Input")
