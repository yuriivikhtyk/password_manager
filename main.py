from tkinter import *
from tkinter import messagebox
import random
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '*', '+']


def pass_gen():
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    for char in range(nr_letters):
        password_list.append(random.choice(letters))

    for char in range(nr_symbols):
        password_list += random.choice(symbols)

    for char in range(nr_numbers):
        password_list += random.choice(numbers)

    random.shuffle(password_list)

    password = ""
    for char in password_list:
        password += char
  
    password_field.delete(0, END)
    password_field.insert(0, password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_field.get()
    email = email_field.get()
    password_prov = password_field.get()
    new_data = {
        website:{
        'email': email,
        'password': password_prov
    }}

    if website == '' or email == '' or password_prov == '':
        messagebox.showwarning(title="Warning", message="All fields shoul be fulfilled")
        return None

    is_ok = messagebox.askokcancel(title=website, message=f"These are details provided: {website} | {email} | {password_prov}. Do you want to save this information?")
    if is_ok:
        try:
            with open("data.txt", "r") as data_file:
                data = json.load(data_file)
                data.update(new_data)
            with open("data.txt", "w") as data_file:
                json.dump(data, data_file, indent=4)

        except FileNotFoundError:
            with open("data.txt", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        except json.decoder.JSONDecodeError:
            with open("data.txt", "w") as data_file:
                json.dump(new_data, data_file, indent=4)

        website_field.delete(0, 'end')
        password_field.delete(0, 'end')


def search():
    website = website_field.get()
    if website == '':
        messagebox.showwarning(title="Warning", message="Please firstly enter website name.")
        return None
    try:
        with open("data.txt", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showwarning(title="Warning", message="There is no data saved yet.")
    else:
        if website in data.keys():
            messagebox.showinfo(title=f"Search result for {website}", message=f"Email: {data[website]['email']} | Password: {data[website]['password']}")
        else:
            messagebox.showwarning(title=f"Search results for {website}", message="There is no such website in database")



# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(width=200, height=200, padx=50, pady=50)


canvas = Canvas(width=200, height=200, highlightthickness=0)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=0,row=0, columnspan=2)


website_label = Label(text="Website:")
website_label.grid(column=0, row=1)
email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)


website_field = Entry(width=35)
website_field.grid(column=1, row=2, columnspan=2)
website_field.focus()
email_field = Entry(width=35)
email_field.grid(column=1, row=3, columnspan=2)
email_field.insert(0, "test.email@domain.com")
password_field = Entry(width=35)
password_field.grid(column=1, row=4, columnspan=2)


gen_button = Button(text="Generate Password", width=29, command=pass_gen)
gen_button.grid(column=1, row=5)
add_button = Button(text="Add", width=29, command=save)
add_button.grid(column=1, row=6)
search_button = Button(text="Search", width=29, command=search)
search_button.grid(column=1, row=1)



window.mainloop()