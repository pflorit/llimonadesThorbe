import mysql.connector


class LemonTree:
    def mostrar_menu_login(self):
        print("======== Thorbe Systems ========")
        print("[                              ]")
        print("[     1· Sign in               ]")
        print("[     2· Log in                ]")
        print("[     3· Exit                  ]")
        print("[                              ]")
        print("================================")
        i = int(input("Selet an option (number of list): "))
        return i

    def mostrar_menu_inicio(self):
        print("======== Thorbe  Systems ========")
        print("[                               ]")
        print("[     1· Sell lemonade          ]")
        print("[     2· Order ingredients      ]")
        print("[     3· Make lemonade          ]")
        print("[     4· Accounting             ]")
        print("[     5· Exit                   ]")
        print("[                               ]")
        print("================================")
        i = int(input("Selet an option (number of list): "))
        return i

    def create_connection(self, ip, nombre):
        mydb = mysql.connector.connect(
            host=ip,
            user="root",
            passwd="",
            database=nombre
        )
        return mydb

    def newUser(self, username, pwd, bd):
        micursor = bd.cursor()
        micursor.execute("INSERT INTO `users`(`userName`, `passwd`) VALUES ('{}','{}')".format(username, pwd))
        bd.commit()

    def logIn(self, username, pwd, bd):
        micursor = bd.cursor()
        micursor.execute("SELECT passwd FROM `users` WHERE userName=\"{}\"".format(username))
        stored_pwd = micursor.fetchall()[0]
        if "('{}',)".format(pwd) == str(stored_pwd):
            print("Successfully logged")
            return True
        else:
            print("The password is not correct. Please try again.")
            return False

    def make_lemondae(self, liters, bd):
        li = int(liters);
        micursor = bd.cursor()
        micursor.execute("UPDATE `products` SET `total_amount`=`total_amount`+{} WHERE 1".format(li))
        bd.commit()

    def sell_lemondae(self, liters, bd):
        r = self.remaining(bd)
        li = int(liters)
        if li > r or r == 0:
            print("Sorry, there's only {}L left".format(r))
        else:
            micursor = bd.cursor()
            micursor.execute("UPDATE `products` SET `total_amount`=`total_amount`-{} WHERE 1".format(li))
            bd.commit()
            print("Transaction complete.")

    def remaining(self, bd):
        micursor=bd.cursor()
        micursor.execute("SELECT total_amount FROM `products` WHERE 1")
        remains = str(micursor.fetchall()[0]).replace("(", "")
        remains = remains.replace(",)", "")
        return int(remains)


a = LemonTree()

