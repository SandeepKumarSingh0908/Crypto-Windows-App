import requests
import json
from tkinter import *
import sqlite3

#intializing the tkinter
my_application = Tk()
my_application.title("Crypto Portfolio")
my_application.iconbitmap("app_icon.ico")

# Establishing the connection with database

con = sqlite3.connect("Crypto.db")
cur = con.cursor()

#Creating table and inserting data
cur.execute("CREATE TABLE IF NOT EXISTS coins(id INTEGER PRIMARY KEY, symbol TEXT, quantity INTEGER, amount_invested REAL)")

#inserting data
# cur.execute("INSERT INTO coins VALUES(2,'ETH', 200, 2000)")
# cur.execute("INSERT INTO coins VALUES(3,'USDT', 200, 100)")
# cur.execute("INSERT INTO coins VALUES(4,'DOT', 200, 5)")
# cur.execute("INSERT INTO coins VALUES(5,'XRP', 200, 0.5)")
# con.commit()

def refresh_application():
    for items in my_application.winfo_children():
        items.destroy()

    header()
    load_application()

def load_application():
    api_data = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=300&convert=USD&CMC_PRO_API_KEY=7b82824b-e3a1-4bbf-8ffd-e07baa841639")
    json_format = json.loads(api_data.content)

    # Marking red and green depends on profit and loss
    def mark(amount):
        if (amount < 0):
            return "red"
        else:
            return "green"

    # Adding coin into database
    def add_coin():
        cur.execute("INSERT INTO coins(symbol,quantity,amount_invested) VALUES(?,?,?)", (symbol_data.get(), quantity_data.get(), Amount_Invested_data.get()))
        con.commit()
        refresh_application()

    # Updating the value
    def update_coin():
        cur.execute("UPDATE coins SET symbol=?, quantity=?, amount_invested=? WHERE id=?", (symbol_update.get(), quantity_update.get(), amount_invested_update.get(),id_update.get()))
        con.commit()
        refresh_application()

    def delete_coin():
        cur.execute("DELETE FROM coins WHERE id=?", (id_delete.get(),))
        con.commit()
        refresh_application()

    # Fetching data from database
    cur.execute("SELECT * FROM coins")
    data = cur.fetchall()

    #  Calculating the required values
    final_pl = 0
    row_number = 1;
    total_current_value = 0
    total_amount_invested = 0
    for i in range(300):
        for coin in data:
            if(coin[1] == json_format["data"][i]["symbol"]):
                amount_invested = coin[2]*coin[3]
                total_amount_invested += amount_invested
                current_value = coin[2]*json_format["data"][i]["quote"]["USD"]["price"]
                total_current_value += current_value
                pl_per_coin = json_format["data"][i]["quote"]["USD"]["price"] - coin[3]
                total_pl_coin = pl_per_coin*coin[2]
                final_pl += total_pl_coin

                coin_id = Label(my_application, text=coin[0], bg="#F3F4F6", fg="black",font="lato 12", padx="2", pady="2", borderwidth=2, relief="groove")
                coin_id.grid(row=row_number, column=0, sticky=N + S + E + W)


                coin_symbol = Label(my_application, text=json_format["data"][i]["symbol"], bg="#F3F4F6", fg="black", font="lato 12", padx="2", pady="2", borderwidth=2, relief="groove")
                coin_symbol.grid(row=row_number, column=1, sticky=N + S + E + W)

                Current_Price = Label(my_application, text="${0:.2f}".format(json_format["data"][i]["quote"]["USD"]["price"]), bg="#F3F4F6", fg="black",font="lato 12", padx="2", pady="2", borderwidth=2, relief="groove")
                Current_Price.grid(row=row_number, column=2, sticky=N + S + E + W)

                Quantity = Label(my_application, text=coin[2], bg="#F3F4F6", fg="black",font="lato 12", padx="2", pady="2", borderwidth=2, relief="groove")
                Quantity.grid(row=row_number, column=3, sticky=N + S + E + W)

                Amount_Invested = Label(my_application, text="${0:.2f}".format(amount_invested), bg="#F3F4F6", fg="black",font="lato 12", padx="2", pady="2", borderwidth=2, relief="groove")
                Amount_Invested.grid(row=row_number, column=4, sticky=N + S + E + W)

                Current_Value = Label(my_application, text="${0:.2f}".format(current_value), bg="#F3F4F6", fg="black",font="lato 12", padx="2", pady="2", borderwidth=2, relief="groove")
                Current_Value.grid(row=row_number, column=5, sticky=N + S + E + W)

                pl_percoin = Label(my_application, text="${0:.2f}".format(pl_per_coin), bg="#F3F4F6", fg=mark(float("{0:.2f}".format(pl_per_coin))), font="lato 12", padx="2", pady="2", borderwidth=2, relief="groove")
                pl_percoin.grid(row=row_number, column=6, sticky=N + S + E + W)

                total_plcoin = Label(my_application, text="${0:.2f}".format(total_pl_coin), bg="#F3F4F6", fg=mark(float("{0:.2f}".format(total_pl_coin))),font="lato 12", padx="2", pady="2", borderwidth=2, relief="groove")
                total_plcoin.grid(row=row_number, column=7, sticky=N + S + E + W)

                row_number+=1

    #Taking data
    symbol_data = Entry(my_application,borderwidth=2, relief="groove")
    symbol_data.grid(row= row_number+1, column=1)

    Amount_Invested_data = Entry(my_application, borderwidth=2, relief="groove")
    Amount_Invested_data.grid(row=row_number + 1, column=2)

    quantity_data = Entry(my_application, borderwidth=2, relief="groove")
    quantity_data.grid(row=row_number + 1, column=3)

    Add = Button(my_application, text="Add Coin", bg="#008CBA", fg="white", command=add_coin, font="lato 12",padx="2", pady="2", borderwidth=2, relief="groove")
    Add.grid(row=row_number + 1, column=4, sticky=N + S + E + W)

    # Updating data
    id_update = Entry(my_application, borderwidth=2, relief="groove")
    id_update.grid(row=row_number + 2, column=0)

    symbol_update = Entry(my_application, borderwidth=2, relief="groove")
    symbol_update.grid(row=row_number + 2, column=1)

    amount_invested_update = Entry(my_application, borderwidth=2, relief="groove")
    amount_invested_update.grid(row=row_number + 2, column=2)

    quantity_update = Entry(my_application, borderwidth=2, relief="groove")
    quantity_update.grid(row=row_number + 2, column=3)

    update = Button(my_application, text="Update Coin", bg="#008CBA", fg="white", command=update_coin, font="lato 12", padx="2",pady="2", borderwidth=2, relief="groove")
    update.grid(row=row_number + 2, column=4, sticky=N + S + E + W)

    #Deleting data
    id_delete = Entry(my_application, borderwidth=2, relief="groove")
    id_delete.grid(row=row_number + 3, column=0)

    delete = Button(my_application, text="Delete Coin", bg="#008CBA", fg="white", command=delete_coin, font="lato 12",padx="2", pady="2", borderwidth=2, relief="groove")
    delete.grid(row=row_number + 3, column=4, sticky=N + S + E + W)

    totalcv = Label(my_application, text="${0:.2f}".format(total_current_value), bg="#F3F4F6", fg="black", font="lato 12",padx="2", pady="2", borderwidth=2, relief="groove")
    totalcv.grid(row=row_number, column=5, sticky=N + S + E + W)

    totalAmntInv = Label(my_application, text="${0:.2f}".format(total_amount_invested), bg="#F3F4F6", fg="black", font="lato 12",padx="2", pady="2", borderwidth=2, relief="groove")
    totalAmntInv.grid(row=row_number, column=4, sticky=N + S + E + W)


    totalpl = Label(my_application, text="${0:.2f}".format(final_pl), bg="#F3F4F6", fg=mark(float("{0:.2f}".format(final_pl))), font="lato 12",padx="2", pady="2", borderwidth=2, relief="groove")
    totalpl.grid(row=row_number, column=7, sticky=N + S + E + W)

    # Emptying the data
    json_format = ""

    refresh = Button(my_application, text="Refresh", bg="#008CBA",fg="white", command= refresh_application,font="lato 12",padx="2", pady="2", borderwidth=2, relief="groove")
    refresh.grid(row=row_number+1, column=7, sticky=N + S + E + W)


# Adding header to my GUI
def header():
    Coin_id = Label(my_application, text="Coin Id", bg="#D35400", fg="white", font="lato 12 bold", padx="5", pady="5",borderwidth=2, relief="groove")
    Coin_id.grid(row=0, column=0, sticky=N + S + E + W)

    name = Label(my_application, text="Coin Name", bg="#D35400", fg="white", font="lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    name.grid(row=0, column=1, sticky=N+S+E+W)

    name = Label(my_application, text="Price", bg="#D35400", fg="white", font="lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    name.grid(row=0, column=2, sticky=N+S+E+W)

    name = Label(my_application, text="Quantity Owned", bg="#D35400", fg="white", font="lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    name.grid(row=0, column=3, sticky=N+S+E+W)

    name = Label(my_application, text="Total Amount Invested", bg="#D35400", fg="white", font="lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    name.grid(row=0, column=4,sticky=N+S+E+W)

    name = Label(my_application, text="Current Value", bg="#D35400", fg="white", font="lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    name.grid(row=0, column=5, sticky=N+S+E+W)

    name = Label(my_application, text="P/L per coin", bg="#D35400", fg="white", font="lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    name.grid(row=0, column=6, sticky=N+S+E+W)

    name = Label(my_application, text="Total P/L with coin", bg="#D35400", fg="white", font="lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    name.grid(row=0, column=7, sticky=N+S+E+W)


header()
load_application()
my_application.mainloop()
cur.close()
con.close()