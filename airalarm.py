import tkinter.messagebox
from tkinter import *
from tkinter import ttk
import datetime
import requests
import pygame
from PIL import Image
from pystray import MenuItem
import pystray

def ComboChange(event):
    global city
    city = regions_list.get()
    city = "_".join("".join(city.split("-")).split(" "))

def AlarmNotification(event):
    global alarmNotification, SirenaPlayed, SirenaNowPlaying, MusicPlaying
    pygame.mixer.music.stop()
    SirenaPlayed = False
    SirenaNowPlaying = False
    MusicPlaying = False
    if alarmNotification == 0:
        alarmNotification = 1
        try:
            app.destroy()
        except:
            pass
        enableAlarm.config(background="lime", text="Сповіщення ввімкнені")
        timeAlarm1.config(state="disabled")
        timeAlarm2.config(state="disabled")
        regions_list.config(state="disabled")
        minuteCheckBox.config(state="disabled")
        ConfigTimeAlarm.config(state="disabled")

    else:
        alarmNotification = 0
        enableAlarm.config(background="pink", text="Сповіщення вимкнені")
        timeAlarm1.config(state="normal")
        timeAlarm2.config(state="normal")
        regions_list.config(state="read")
        minuteCheckBox.config(state="normal")
        ConfigTimeAlarm.config(state="normal")

def IsAlarm(City):
    try:
        CitiesWithAlarm = requests.get("https://alarmmap.online/assets/json/_alarms/siren.json").json()
        for i in CitiesWithAlarm:
            if i["district"] == City:
                return True
        return False
    except:
        pass # Помилка сервера

def NowInSec():
    return int((datetime.datetime.now() - datetime.datetime(1, 1, 1, 0, 0)).total_seconds())

def GetTime(entr1, entr2):
    global t1, t2
    try:
        t1 = int(float(entr1.get())) if int(float(entr1.get())) == float(entr1.get()) else float(entr1.get())
        t2 = int(float(entr2.get())) if int(float(entr2.get())) == float(entr2.get()) else float(entr2.get())
        timeAlarm1.config(text=f"Оголошення - {t1} секунд\n Відбій - {t2} секунд")
        app.destroy()
    except:
        but.config(text="Помилка")
        root.after(400, lambda : but.config(text="Зберегти"))

def ChangeTimeAlarm():
    global app, but
    app = Tk()
    app.geometry("300x100")
    app.title("Змінення часу тривоги")
    app.iconbitmap("airalarm.ico")
    app.resizable(0, 0)
    app.update()
    x = app.winfo_screenwidth() / 2 - app.winfo_reqwidth() / 2
    y = app.winfo_screenheight() / 2 - app.winfo_reqheight() / 2
    app.wm_geometry("+%d+%d" % (x, y))

    frame = Frame(app)
    frame.grid(pady=10,padx=10)
    lb1 = Label(frame, text="Оголошення: ", font="Arial 12")
    lb1.grid(row=0, column=0)
    lb2 = Label(frame, text="Відбій: ", font="Arial 12")
    lb2.grid(row=1, column=0)
    but = Button(frame, text="Зберегти", font="Arial 12", command=lambda: GetTime(entr1, entr2))
    but.grid()

    entr1 = Entry(frame, width=8)
    entr1.grid(row=0, column=1)
    entr2 = Entry(frame, width=8)
    entr2.grid(row=1, column=1)

    app.mainloop()

root = Tk()
root.geometry("490x370")
root.title("Повітряна тривога (коледж) v.2.0")
root.iconbitmap("airalarm.ico")
root.resizable(0,0)
pygame.init()

#with open("locations_list/regions.txt", "r", encoding="utf-8") as f:
#    regions = sorted(eval(f.read()))

regions = ["-", "Автономна Республіка Крим", "Вінницька область", "Волинська область", "Дніпропетровська область",
           "Донецька область", "Житомирська область", "Закарпатська область", "Запорізька область", "Івано-Франківська область",
           "Кіровоградська область", "Луганська область", "Львівська область", "Миколаївська область", "Одеська область",
           "Полтавська область", "Рівненська область", "Сумська область", "Тернопільська область", "Харківська область",
           "Хмельницька область", "Черкаська область", "Чернівецька область", "Чернігівська область", "Херсонська область", 
           "Київська область"]

r = IntVar()
r.set(1)
c = IntVar()
c.set(1)
alarmNotification = 0
city = "-"
SirenaPlayed = False
SirenaNowPlaying = False
MusicPlaying = False
t1 = 134
t2 = 89
end = 0

def SirenaPlay(link, sec=1):
    global SirenaNowPlaying, end
    pygame.mixer.music.stop()
    pygame.mixer.music.load(link)
    pygame.mixer.music.play(9**9)
    SirenaNowPlaying = True
    end = NowInSec() + sec

def MusicOff():
    global MusicPlaying
    MusicPlaying = False

def Refresh():
    global SirenaNowPlaying, SirenaPlayed, end, MusicPlaying
    if alarmNotification:
        Is_Alarm = IsAlarm(city)
        if Is_Alarm and r.get() == 1 and not SirenaPlayed and not SirenaNowPlaying:
            SirenaPlay("Sound/start_sirena.mp3", int(t1))
        elif not Is_Alarm and r.get() == 1 and SirenaPlayed and not SirenaNowPlaying:
            SirenaPlay("Sound/stop_sirena.mp3", int(t2))
        elif Is_Alarm and not SirenaNowPlaying and r.get() == 2:
            SirenaPlay("Sound/sirena.mp3")
        if SirenaNowPlaying and r.get() == 1 and NowInSec() > end:
            pygame.mixer.music.stop()
            SirenaNowPlaying = False
            SirenaPlayed = not SirenaPlayed
        elif not Is_Alarm and SirenaNowPlaying and r.get() == 2:
            SirenaNowPlaying = False
            pygame.mixer.music.stop()
            SirenaPlayed = False
        if datetime.datetime.now().hour == 9 and datetime.datetime.now().minute == 0 and not MusicPlaying and not SirenaNowPlaying and c.get() == 1:
            MusicPlaying = True
            pygame.mixer.music.stop()
            pygame.mixer.music.load("Sound/hvilina.mp3")
            pygame.mixer.music.play()
            pygame.mixer.music.queue("Sound/gimn.mp3")
            root.after(61000, MusicOff)

    root.after(1000, Refresh)


locFrame = Frame(root)
alarmFrame = Frame(root)
locFrame.grid(row=0, column=0, padx=10, pady=10, sticky="W")
alarmFrame.grid(row=1, column=0, padx=10, pady=10, sticky="W")

lb_region = Label(locFrame, text="Область", font="Impact 14")
lb_space1 = Label(alarmFrame, text=" ", font="Arial 10")
lb_timeAlarm = Label(alarmFrame, text="Довжина сповіщення", font="Impact 16")
lb_space2 = Label(alarmFrame, text=" ", font="Arial 10")
lb_additionalFunc = Label(alarmFrame, text="Додаткові функції", font="Impact 16")
lb_copyright = Label(root, text="© 2022, Last-Arkhangel")
lb_region.grid(row=0, column=0, sticky="W", padx=5)
lb_space1.grid(row=1, column=0, sticky="W", padx=5)
lb_timeAlarm.grid(row=2, column=0, sticky="W", padx=5)
lb_space2.grid(row=5, column=0, sticky="W", padx=5)
lb_additionalFunc.grid(row=6, column=0, sticky="W", padx=5)
lb_copyright.place(relx=0.02,rely=0.98,anchor="sw")

regions_list = ttk.Combobox(locFrame, state="readonly", width=len(max(regions, key=len)), font="Arial 14", values=regions)
regions_list.grid(row=0, column=1, sticky="W", padx=5)
regions_list.current(0)

enableAlarm = Button(alarmFrame, background="pink", text="Сповіщення вимкнені", font="Arial 14")
ConfigTimeAlarm = Button(alarmFrame, text="Змінити час тривоги", font="Arial 10", command=ChangeTimeAlarm)
ConfigTimeAlarm.grid(row=3, column=1, sticky="W", padx=5)
enableAlarm.grid(row=0, column=0, sticky="W", padx=5)

timeAlarm1 = Radiobutton(alarmFrame, variable=r, value=1, text=f"Оголошення - {t1} секунд\n Відбій - {t2} секунд", font="Arial 14")
timeAlarm2 = Radiobutton(alarmFrame, variable=r, value=2, text="Від початку до кінця", font="Arial 14")
minuteCheckBox = Checkbutton(alarmFrame, variable=c, text="Хвилина мовчання і гімн України", font="Arial 14")
timeAlarm1.grid(row=3, column=0, sticky="W", padx=5)
timeAlarm2.grid(row=4, column=0, sticky="W", padx=5)
minuteCheckBox.grid(row=7, column=0, sticky="W", padx=5)

regions_list.bind("<<ComboboxSelected>>", ComboChange)
enableAlarm.bind("<Button-1>", AlarmNotification)

def quit_win():
	root.destroy()

ConfigQuit = Button(alarmFrame, text="Вихід", font="Arial 10", command=quit_win)
ConfigQuit.grid(row=8, column=1, sticky="es", padx=5)


def quit_window(icon):
	icon.stop()
	root.destroy()

def show_window(icon):
	icon.stop()
	root.after(0, root.deiconify())

def hide_window():
	root.withdraw()
	image = Image.open('airalarm.ico')
	menu = (MenuItem('Розгорнути', show_window), MenuItem('Вихід', quit_window))
	icon = pystray.Icon("Повітряна тривога", image, 'Повітряна тривога (коледж) v.2.0', menu)
	icon.run()

Refresh()
root.protocol('WM_DELETE_WINDOW', hide_window)
root.mainloop()