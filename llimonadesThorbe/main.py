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
        print("======== Thorbe Systems ========")
        print("[                               ]")
        print("[     1· Sell                   ]")
        print("[     2· Order                  ]")
        print("[     3· Production             ]")
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
        stored_pwd =micursor.fetchall()
        if pwd == stored_pwd:
            print("iniciado")
            return True
        else:
            print("Datos incorrectos")
            return False


a = LemonTree()
mydb = a.create_connection("localhost", "lemondb")
micursor = mydb.cursor()
micursor.execute("SELECT passwd FROM `users`")
stored_pwd = micursor.fetchall()
for pwd in stored_pwd:
    print(pwd)
