stock = {}

try:
    with open(r"C:\Users\Hello\Desktop\AUR-Training-26\task_2\subtask_1\stock.txt", "r") as f:
        for line in f:
            key, value = line.split(",")
            stock[key.lower()] = int(value)

    print(stock)

except Exception as e:
    print("Error:", e)

    while(True):
       choice= int(input("enter 1 to add stock\nenter 2 to remove stock\nenter 3 to show stock’s contents\nenter 4 to exit the program"))
       if choice ==1:
           name=list(stock.keys())
           for i in range(len(name)):
               print(i+1,name[i],stock[name[i]])
           item=input("\nEnter the stock name or ID: ")
           if item.isdigit():
               item_id=int(item)
               if 1 <= item_id <= len(name):
                item = name[item_id - 1]
               else:
                print("Invalid ID")
                continue
           else:
               item=item.lower()
           try:
            amount = int(input("Enter how much to add to the stock: "))

            if amount < 0:
                print("Invalid amount")
                continue

           except ValueError:
            print("Invalid amount")
            continue
           if item in stock:
              stock[item]=stock[item]+amount
           else:
              stock[item]=amount

           print("Stock updated successfully!")
           print(item, stock[item])
       elif choice == 2:
           pass
       elif choice == 3:
           pass
       elif choice==4:
           break
       else:
           print("Invalid Input")
