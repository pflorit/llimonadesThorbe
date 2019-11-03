import mysql.connector


def mostrar_menu_login(bd):
    print("======== Thorbe Systems ========")
    print("[                              ]")
    print("[     1· Sign in               ]")
    print("[     2· Log in                ]")
    print("[     3· Exit                  ]")
    print("[                              ]")
    print("================================")
    i = input("Selet an option (number of list): ")
    if i == "1":
        username = input("Username: ")
        passwd = input("Password: ")
        permited = logIn(username, passwd, bd)
        if permited:
            mostrar_menu_inicio(bd)
        else:
            mostrar_menu_login(bd)

    elif i == "2":
        newUser(bd)
        mostrar_menu_login(bd)

    elif i == "3":
        print("See you later!")
        bd.close()

    else:
        mostrar_menu_login(bd)


def mostrar_menu_inicio(bd):
    print("======== Thorbe  Systems ========")
    print("[                               ]")
    print("[     1· Sell lemonade          ]")
    print("[     2· Order ingredients      ]")
    print("[     3· Make lemonade          ]")
    print("[     4· Accounting             ]")
    print("[     5· Close session          ]")
    print("[     0· Exit                   ]")
    print("[                               ]")
    print("================================")
    i = input("Selet an option (number of list): ")
    if i == "1":
        sell_lemondae(bd)

    elif i == "2":
        order_ingredients(bd)

    elif i == "3":
        make_lemondae(bd)

    elif i == "4":
        see_accounting(bd)

    elif i == "5":
        mostrar_menu_login(bd)

    elif i == "0":
        print("See you later!")
        bd.close()

    else:
        mostrar_menu_inicio(bd)


def create_connection(ip, nombre):
    connection = mysql.connector.connect(
        host=ip,
        user="root",
        passwd="",
        port="3307",
        database=nombre
    )
    return connection


def see_accounting(bd):
    micursor = bd.cursor()
    micursor.execute("SELECT `date`,sum(`losses`)as total_lost, sum(`profit`)as total_won "
                     "from `accounting` group by `date`")
    result = micursor.fetchall()
    for res in result:
        print("~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Date: " + str(res[0]))
        print("~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Expenses: " + str(res[1]) + "€")
        print("Earnings: " + str(res[2]) + "€")
        print()
    mostrar_menu_inicio(bd)


def user_exists(micursor, username):
    micursor.execute("SELECT userName FROM `users`")
    repetido = False
    listUsers = micursor.fetchall()
    for res in listUsers:
        res = str(res).replace("('", "")
        res = res.replace("',)", "")

        if str(res) == str(username):
            print("Sorry, user already registered.")
            repetido = True

    return repetido


def newUser(bd):
    micursor = bd.cursor()
    repetido = True
    while repetido:
        username = input("Insert a username: ")
        repetido = user_exists(micursor, username)

    pwd = input("Insert a password: ")
    micursor.execute("INSERT INTO `users`(`userName`, `passwd`) VALUES ('{}','{}')".format(username, pwd))
    bd.commit()
    print("Welcome to the system {}!".format(username))


def logIn(username, pwd, bd):
    micursor = bd.cursor()
    micursor.execute("SELECT passwd FROM `users` WHERE userName=\"{}\"".format(username))
    stored_pwd = micursor.fetchall()
    if len(stored_pwd) <= 0:
        print("User does not exist.")
        return False
    else:
        stored_pwd = stored_pwd[0]
        if "('{}',)".format(pwd) == str(stored_pwd):
            print("Successfully logged")
            return True
        else:
            print("The password is not correct. Please try again.")
            return False


def make_lemondae(bd):
    liters = int(input("How many litters are you going to produce? "))
    li = int(liters)
    lemons = 4 * li
    water = li
    sugar = 175 * li
    canProduce = remaining_products(bd, lemons, water, sugar)
    if canProduce:
        micursor = bd.cursor()
        micursor.execute("UPDATE `products` SET `total_amount`=`total_amount`+{} WHERE 1".format(li))
        micursor.execute("UPDATE `ingredients` SET `stock`=`stock`-{} WHERE name=\"lemons\"".format(lemons))
        micursor.execute("UPDATE `ingredients` SET `stock`=`stock`-{} WHERE name=\"sugar\"".format(sugar))
        micursor.execute("UPDATE `ingredients` SET `stock`=`stock`-{} WHERE name=\"water\"".format(water))
        bd.commit()
        print("*brrrrr Ding!* Lemonade produced.")
    mostrar_menu_inicio(bd)


def sell_lemondae(bd):
    liters = int(input("How many liters do you want? (4€ per liter)"))
    r = remaining_lemonade(bd)
    li = int(liters)
    money = li * 4
    if li > r or r == 0:
        print("Sorry, there's only {}L left".format(r))
    else:
        micursor = bd.cursor()
        micursor.execute("UPDATE `products` SET `total_amount`=`total_amount`-{} WHERE 1".format(li))
        micursor.execute("INSERT INTO `accounting`(`id`, `profit`, `losses`, `date`) VALUES (NULL,{},NULL,CURRENT_DATE)"
                         .format(money))
        bd.commit()
        print("Transaction complete.")
    mostrar_menu_inicio(bd)


def remaining_lemonade(bd):
    micursor = bd.cursor()
    micursor.execute("SELECT total_amount FROM `products` WHERE 1")
    remains = str(micursor.fetchall()[0]).replace("(", "")
    remains = remains.replace(",)", "")
    return int(remains)


def remaining_products(bd, lemonsNeed, waterNeed, sugarNeed):
    micursor = bd.cursor()
    micursor.execute("SELECT `stock` FROM `ingredients` WHERE name=\"lemons\"")
    lemons = str(micursor.fetchall()[0]).replace("(", "")
    lemons = lemons.replace(",)", "")

    micursor.execute("SELECT `stock` FROM `ingredients` WHERE name=\"water\"")
    water = str(micursor.fetchall()[0]).replace("(", "")
    water = water.replace(",)", "")

    micursor.execute("SELECT `stock` FROM `ingredients` WHERE name=\"sugar\"")
    sugar = str(micursor.fetchall()[0]).replace("(", "")
    sugar = sugar.replace(",)", "")

    if int(lemons) < int(lemonsNeed) or int(water) < int(waterNeed) or int(sugar) < int(sugarNeed):
        print("Sorry, you don't have enough products.")
        print("     Lemons: Need-> {}     Have-> {}".format(lemonsNeed, lemons))
        print("     Water:  Need-> {}L    Have-> {}L".format(waterNeed, water))
        print("     Sugar:  Need-> {}G    Have-> {}G".format(sugarNeed, sugar))
        return False
    else:
        return True


def order_ingredients(bd):
    micursor = bd.cursor()
    lemons = int(input("How many lemons do you want? "))
    sugar = int(input("How many grams of sugar do you want? "))
    water = int(input("How many liters of water do you want? "))
    lemon_price = "{0:.2f}".format((lemons * 0.30))
    water_price = "{0:.2f}".format((water * 0.59))
    sugar_price = "{0:.2f}".format((sugar * 0.07))
    total = float(lemon_price) + float(water_price) + float(sugar_price)
    proceed = create_bill(lemon_price, water_price, sugar_price, total)
    if proceed:
        micursor.execute("UPDATE `ingredients` SET `stock`=`stock`+{} WHERE `name`= \"lemons\"".format(lemons))
        micursor.execute("UPDATE `ingredients` SET `stock`=`stock`+{} WHERE `name`= \"sugar\"".format(sugar))
        micursor.execute("UPDATE `ingredients` SET `stock`=`stock`+{} WHERE `name`= \"water\"".format(water))
        micursor.execute("INSERT INTO `accounting`(`id`, `profit`, `losses`, `date`) VALUES (null,null,{},CURRENT_DATE)"
                         .format(total))
        bd.commit()
    else:
        print("Order canceled")
    mostrar_menu_inicio(bd)


def create_bill(lemons, water, sugar, total):
    print()
    print("======== ORDER ========")
    print("Lemons: " + str(lemons) + "€")
    print("Water: " + str(water) + "€")
    print("Sugar: " + str(sugar) + "€")
    print()
    print("====> Final price: " + str(total) + "€")
    proceed = ""
    while proceed.upper() != "S" or proceed.upper() != "N":
        proceed = input("Do you want to proceed?(S or N)")
        if proceed.upper() == "S":
            return True
        elif proceed.upper() == "N":
            return False


mydb = create_connection("localhost", "lemondb")
mostrar_menu_login(mydb)
