from tkinter import *
from tkinter.font import *
import sqlite3
import os
from subprocess import call
from tkinter import messagebox
import webbrowser

# region datebase
class datebase:
    def __init__(self, db):
        self.__db_name = db
        self.connection = sqlite3.connect(self.__db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS [menu_resturant](
        [ID] INT PRIMARY KEY NOT NULL UNIQUE, 
        [name] NVARCHAR NOT NULL UNIQUE, 
        [price] INT NOT NULL,
        [is_food] BOOL NOT NULL) WITHOUT ROWID;
        """
        )
        self.cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS [menu_receipts](
            [RECEIPT_NUMBER] INT NOT NULL,
            [MENU_ID] INT NOT NULL REFERENCES[menu_resturant]([ID]),
            [PRICE] INT NOT NULL,
            [COUNT] INT NOT NULL );
        """
        )
        self.cursor.execute(
            """     CREATE VIEW IF NOT EXISTS menu_receipts_resturant AS
                    SELECT menu_receipts.RECEIPT_NUMBER ,menu_resturant.name ,
                    menu_receipts.PRICE , menu_receipts.COUNT , (menu_receipts.COUNT * menu_receipts.PRICE) as SUM
                    FROM menu_resturant
                    INNER JOIN menu_receipts ON menu_resturant.ID == menu_receipts.MENU_ID
                    """
        )
        self.connection.commit()
        self.connection.close()

    def insert(self, id, name, price, is_food):
        self.connection = sqlite3.connect(self.__db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            """
        insert into menu_resturant values(? , ? , ?, ?) """,
            (id, name, price, is_food),
        )
        self.connection.commit()
        self.connection.close()

    def get_menu_items(self, is_food):
        self.connection = sqlite3.connect(self.__db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            """SELECT * FROM menu_resturant WHERE is_food = ?""", (is_food,)
        )
        result = self.cursor.fetchall()
        return result

    def get_max_receipt(self):
        self.connection = sqlite3.connect(self.__db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute(" SELECT MAX(RECEIPT_NUMBER) FROM menu_receipts")
        result = self.cursor.fetchall()
        return result

    def get_menu_by_name(self, menu_name):
        self.connection = sqlite3.connect(self.__db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute("SELECT * FROM menu_resturant WHERE name = ?", (menu_name,))
        result = self.cursor.fetchall()
        return result

    def insert_to_receipt(self, RECEIPT_NUMBER, MENU_ID, PRICE, COUNT):
        self.connection = sqlite3.connect(self.__db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            "INSERT INTO menu_receipts VALUES(? , ? ,? ,? )",
            (RECEIPT_NUMBER, MENU_ID, PRICE, COUNT),
        )
        self.connection.commit()
        self.connection.close()

    def grouping_receipts(self, receipts_number, menu_id):
        self.connection = sqlite3.connect(self.__db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            "SELECT * FROM menu_receipts WHERE RECEIPT_NUMBER = ? and MENU_ID = ?",
            (receipts_number, menu_id),
        )
        result = self.cursor.fetchall()
        return result

    def update_count(self, RECEIPT_NUMBER, MENU_ID):
        self.connection = sqlite3.connect(self.__db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            "UPDATE menu_receipts SET COUNT = COUNT + 1 WHERE RECEIPT_NUMBER = ? and MENU_ID = ?",
            (RECEIPT_NUMBER, MENU_ID),
        )
        self.connection.commit()
        self.connection.close()

    def update_count_mines(self, RECEIPT_NUMBER, MENU_ID):
        self.connection = sqlite3.connect(self.__db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            "UPDATE menu_receipts SET COUNT = COUNT - 1 WHERE RECEIPT_NUMBER = ? and MENU_ID = ? AND COUNT > 1",
            (RECEIPT_NUMBER, MENU_ID),
        )
        self.connection.commit()
        self.connection.close()

    def view_table(self, receipts_number):
        self.connection = sqlite3.connect(self.__db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            "SELECT * FROM menu_receipts_resturant WHERE RECEIPT_NUMBER = ? ",
            (receipts_number,),
        )
        result = self.cursor.fetchall()
        return result

    def delet_receipt_row(self, receipt_id, menu_item_id):
        self.connection = sqlite3.connect(self.__db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            "DELETE FROM menu_receipts WHERE RECEIPT_NUMBER = ? and MENU_ID = ?",
            (receipt_id, menu_item_id),
        )
        self.connection.commit()
        self.connection.close()


# endregion
# region all
db = None
if os.path.isfile("resturant.db") == False:
    db = datebase("resturant.db")
    db.insert(1, "خورشت", 200400, True)
    db.insert(2, "خوراک", 200030, True)
    db.insert(3, "کباب", 200200, True)
    db.insert(4, "لوبیا", 10000, True)
    db.insert(5, "خورشت1", 120000, True)
    db.insert(6, "2خورشت", 210000, True)
    db.insert(7, "نوشابه", 210000, False)
    db.insert(8, "دوغ", 210000, False)
else:
    db = datebase("resturant.db")

Window = Tk()
my_font = Font(family="Vazir", size=16)
Window.state("zoomed")
Window.title("برنامه مدیریت رستوران")

Window.grid_columnconfigure(0, weight=2)
Window.grid_columnconfigure(1, weight=3)
Window.grid_rowconfigure(0, weight=1)
pad_x = 5
pad_y = 5
# endregion
# region left_label
# *********************************************لیبل سمت چپ
def insert_to_listbox(receipts):
    box.delete(0, "end")
    receipts_list = db.view_table(receipts)
    for receipt in receipts_list:
        box.insert(0, f"{receipt[1]} {receipt[4]} {receipt[0]}")


label_left = LabelFrame(
    Window, font=my_font, text="غذا و نوشودنی", padx=pad_x, pady=pad_y
)
label_left.grid(row=0, column=0, sticky="nsew", padx=pad_x, pady=pad_y)

# *********************************************رسید
label_left.grid_columnconfigure(0, weight=1)
label_left.grid_rowconfigure(0, weight=1)
label_left.grid_rowconfigure(1, weight=10)
label_left.grid_rowconfigure(2, weight=0)

# *********************************************وزودی تعداد
order_num = Entry(label_left, font=my_font, width=10, justify="center")
order_num.grid(row=0, column=0)
receipt_num = db.get_max_receipt()
if receipt_num[0][0] == None:
    receipt_num = 0
else:
    receipt_num = int(receipt_num[0][0])
receipt_num += 1
order_num.insert(0, receipt_num)


def entry_key(key):
    try:
        receipt_id = int(order_num.get())
        insert_to_listbox(receipt_id)
    except:
        box.delete(0, "end")


order_num.bind("<KeyRelease>", entry_key)

box = Listbox(label_left, font=my_font, width=20)
box.grid(row=1, column=0, sticky="nsew", padx=pad_x, pady=pad_y)
box.configure(justify=RIGHT)

Button_frames = LabelFrame(label_left)
Button_frames.grid(row=2, column=0, sticky="nsew", padx=pad_x, pady=pad_y)
Button_frames.grid_columnconfigure(0, weight=1)
Button_frames.grid_columnconfigure(1, weight=1)
Button_frames.grid_columnconfigure(2, weight=1)
Button_frames.grid_columnconfigure(3, weight=1)


def next_receipt():
    box.delete(0, "end")
    max_rece = db.get_max_receipt()
    if max_rece[0][0] == 0:
        max_rece = 0
    else:
        max_rece = int(max_rece[0][0])
    max_rece += 1
    order_num.delete(0, "end")
    order_num.insert(0, max_rece)


def delet_receipt():
    receipt_id = int(order_num.get())
    menu_item = box.get(ACTIVE)
    result = menu_item.split(" ")[0]
    menu_item_id = db.get_menu_by_name(result)
    result_id = int(menu_item_id[0][0])
    db.delet_receipt_row(receipt_id, result_id)
    insert_to_listbox(receipt_id)


def plus_receipt():
    receipt_id = int(order_num.get())
    menu_item = box.get(ACTIVE)
    result = menu_item.split(" ")[0]
    menu_item_id = db.get_menu_by_name(result)
    result_id = int(menu_item_id[0][0])
    db.update_count(receipt_id, result_id)
    insert_to_listbox(receipt_id)

def mines_receipt():
    receipt_id = int(order_num.get())
    menu_item = box.get(ACTIVE)
    result = menu_item.split(" ")[0]
    menu_item_id = db.get_menu_by_name(result)
    result_id = int(menu_item_id[0][0])
    db.update_count_mines(receipt_id, result_id)
    insert_to_listbox(receipt_id)

button_delet = Button(Button_frames, text="حذف", font=my_font, command=delet_receipt)
button_delet.grid(row=0, column=0, sticky="nsew")
button_add = Button(Button_frames, text="+", font=my_font, command=plus_receipt)
button_add.grid(row=0, column=1, sticky="nsew")
button_new = Button(Button_frames, text="جدید", font=my_font, command=next_receipt)
button_new.grid(row=0, column=2, sticky="nsew")
button_mines = Button(Button_frames, text="-", font=my_font, command=mines_receipt)
button_mines.grid(row=0, column=3, sticky="nsew")
# endregion
# region right_region
# *********************************************لیبل سمت راست
label_right = LabelFrame(
    Window, font=my_font, text="لیست سفارش", padx=pad_x, pady=pad_y
)
label_right.grid(row=0, column=1, sticky="nsew", padx=pad_x, pady=pad_y)

# *********************************************غذا و نوشیدنی
label_right.grid_columnconfigure(0, weight=2)
label_right.grid_columnconfigure(1, weight=3)
label_right.grid_rowconfigure(0, weight=1)

drink_label = LabelFrame(
    label_right, font=my_font, text="نوشیدنی", padx=pad_x, pady=pad_y
)
drink_label.grid(row=0, column=0, sticky="nsew", padx=pad_x, pady=pad_y)

listbox_drinks = Listbox(drink_label, font=my_font, exportselection=False)
listbox_drinks.grid(sticky="nsew")
listbox_drinks.configure(justify=RIGHT)
drink_label.grid_columnconfigure(0, weight=1)
drink_label.grid_rowconfigure(0, weight=1)
drinks = db.get_menu_items(False)
for drink in drinks:
    listbox_drinks.insert("end", drink[1])


def add_drink(event):
    drink_selected = db.get_menu_by_name(listbox_drinks.get(ACTIVE))
    ID_drink = drink_selected[0][0]
    Price_drink = drink_selected[0][2]
    receipts = int(order_num.get())
    result = db.grouping_receipts(receipts, ID_drink)
    if len(result) == 0:
        db.insert_to_receipt(receipts, ID_drink, Price_drink, 1)
    else:
        db.update_count(receipts, ID_drink)
    insert_to_listbox(receipts)


listbox_drinks.bind("<Double-Button>", add_drink)

food_label = LabelFrame(label_right, font=my_font, text="غذا", padx=pad_x, pady=pad_y)
food_label.grid(row=0, column=1, sticky="nsew", padx=pad_x, pady=pad_y)

listbox_foods = Listbox(food_label, font=my_font, exportselection=False)
listbox_foods.grid(sticky="nsew")
listbox_foods.configure(justify=RIGHT)
food_label.grid_columnconfigure(0, weight=1)
food_label.grid_rowconfigure(0, weight=1)
foods = db.get_menu_items(True)
for food in foods:
    listbox_foods.insert("end", food[1])


def add_food(event):
    food_selected = db.get_menu_by_name(listbox_foods.get(ACTIVE))
    ID_food = food_selected[0][0]
    Price_food = food_selected[0][2]
    receipts = int(order_num.get())
    result = db.grouping_receipts(receipts, ID_food)
    if len(result) == 0:
        db.insert_to_receipt(receipts, ID_food, Price_food, 1)
    else:
        db.update_count(receipts, ID_food)
    insert_to_listbox(receipts)


listbox_foods.bind("<Double-Button>", add_food)
# endregion
# region buttons
# *********************************************پیکربندی دکمه
Buttons = LabelFrame(Window, font=my_font, padx=pad_x, pady=pad_y)
Buttons.grid(row=1, column=1, padx=pad_x, pady=pad_y)


def culc_fun():
    call(["calc.exe"])


def message_exit():
    print("exit")
    message_ex = messagebox.askquestion(
        "خروج", "یا میخواهید خارج شوید؟", icon="warning"
    )
    if message_ex == "yes":
        Window.destroy()


def go_website():
    webbrowser.open("https://google.com")


Button_colculate = Button(Buttons, text="محاسبه", command=culc_fun)
Button_colculate.grid(row=0, column=0, sticky="nsew")
Button_ext = Button(Buttons, text="خروج", command=message_exit)
Button_ext.grid(row=0, column=1, sticky="nsew")
Button_web = Button(Buttons, text="وبسایت ما", command=go_website)
Button_web.grid(row=0, column=2, sticky="nsew")
# endregion
Window.mainloop()
