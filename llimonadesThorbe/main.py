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


a = LemonTree()
a.mostrar_menu_inicio()
a.mostrar_menu_login()