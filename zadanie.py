import smtplib

path = "data.txt"
main_dict = dict()
# print(type(slownik))
Id = 0
with open(path) as file:
    Id = 1
    for obj in file:
        user = f"user{Id}"
        line = obj.rstrip().split(',')
        student_dict = {'email': line[0],
                        'imie': line[1],
                        'nazwisko': line[2],
                        'punkty': line[3],
                        'ocena': line[4],
                        'status': line[5]}

        # line = list(line.split(","))
        # print(type(slownik))
        # print(line)
        main_dict[user] = student_dict
        Id += 1


def save_changes():
    with open("data.txt", 'w') as file:
        for key, val in main_dict.items():
            line = f'{val["email"]},{val["imie"]},{val["nazwisko"]},{val["punkty"]},{val["ocena"]},{val["status"]}\n'
            print(line)
            file.write(line)


for key, val in main_dict.items():
    print(str(key) + ": " + str(val))

    if val["status"] != "GRADED" and val["status"] != "MAILED":
        print(f"{key} do oceny")
        if int(val["punkty"]) <= 50:
            val.update({"ocena": "2"})
            val["status"] = "GRADED"
        elif int(val["punkty"]) in range(51, 60):
            val.update({"ocena": "3"})
            val["status"] = "GRADED"
        elif int(val["punkty"]) in range(61, 70):
            val.update({"ocena": "3.5"})
            val["status"] = "GRADED"
        elif int(val["punkty"]) in range(71, 80):
            val.update({"ocena": "4"})
            val["status"] = "GRADED"
        elif int(val["punkty"]) in range(81, 90):
            val.update({"ocena": "4.5"})
            val["status"] = "GRADED"
        elif int(val["punkty"]) in range(91, 100):
            val.update({"ocena": "5"})
            val["status"] = "GRADED"
        save_changes()

choice = input("Czy chcesz:"
               "\n1. Dodac nowego studenta."
               "\n2. Usunac istniejacego studenta"
               "\n3. Przejsc dalej i wyslac maile o ocenach studentom.\n")

if int(choice) == 1:
    print("Dodawanie nowego studenta. Podaj jego dane: ")
    correct_email = True
    email = ""
    while correct_email:
        email = input("email:")
        for key, val in main_dict.items():
            if val["email"] == email:
                print("Podany email juz istnieje. Podaj inny")
                break
        correct_email = False
    name = input("imie:")
    surname = input("nazwisko:")
    points = input("punkty:")
    mark = input("ocena:")
    status = input("Status (GRADED lub MAILED):")

    user = f"user{Id}"
    student_dict = {'email': email,
                    'imie': name,
                    'nazwisko': surname,
                    'punkty': points,
                    'ocena': mark,
                    'status': status}
    main_dict[user] = student_dict
    Id += 1
    save_changes()
elif int(choice) == 2:
    print("Podaj email studenta którego chcesz usunać:")
    incorrect_email = True
    email = ""
    while incorrect_email:
        email = input("email:")
        user_to_delete = ""
        for key, val in main_dict.items():
            if val["email"] == email:
                user_to_delete = key
                incorrect_email = False
        del main_dict[user_to_delete]
    save_changes()
elif int(choice) == 3:
    from email.mime.text import MIMEText

    for key, val in main_dict.items():
        if val["status"] != "MAILED" and val["status"] == "GRADED":
            msg = MIMEText(f'Ocena stdenta {val["imie"]} {val["nazwisko"]}: {val["ocena"]}'
                           f'\npunkty: {val["punkty"]}/100')
            msg['Subject'] = "Ocena"
            msg["From"] = ""  # podaj email nadawcy
            msg["To"] = ""  # Podaj email odbiorcy
            smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            smtp_server.login("", "")  # podaj: email nadawcy, haslo nawdawcy
            smtp_server.sendmail()  # podaj: email nadawcy, email odbiorcy, msg.as_string()
            smtp_server.quit()
            save_changes()
