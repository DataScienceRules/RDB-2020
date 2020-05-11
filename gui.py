import sqlite3
import time
import datetime
import os
import csv
from tkinter import *
from tkinter import filedialog, messagebox, ttk, font
from venv.data_generator import generate_data
from matplotlib import pyplot as plt
import matplotlib.dates as md
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy
from venv.plotting import gantt_s, gantt_k, gantt_v
#from createDB import cursor

def gui():
    root = Tk()
    root.title("Zemědělské stroje - GUI")
    root.geometry("500x500")

    nb = ttk.Notebook(root)
    nb.grid(row=1, column=0)

    tab1 = Frame(nb)
    nb.add(tab1, text="Zakladni info")

    tab2 = Frame(nb)
    nb.add(tab2, text="Gantt chart")

    tab3 = Frame(nb)
    nb.add(tab3, text="Jizdni data")

    tab4 = Frame(nb)
    nb.add(tab4, text="Dotazy")

    tab5 = Frame(nb)
    nb.add(tab5, text="Filtry")
    
    def graph():
        prices = numpy.random.normal(2000, 200, 1000)
        plt.hist(prices, 50)
        plt.show()

    def gantt_chart(s=None, v=None, k=None):
        connection = sqlite3.connect('zemedelske_stroje.db')
        cursor = connection.cursor()
        #print(str(seriove_cislo))

        def prepare_for_gantt(pocet_stroju):
            vins = []
            od = []
            do = []
            konfigs = []
            serias = []
            for one in pocet_stroju:
                vins.append(one[1])
                konfigs.append(one[2])
                od.append(datetime.datetime.fromtimestamp(one[3]))
                do.append(datetime.datetime.fromtimestamp(one[4]))
                serias.append(one[0])
            return (vins, od, do, konfigs, serias)

        if s is not None:
            pocet_stroju = cursor.execute("select * from Kombinace where seriove_cislo=:s", {"s": s, "ber": "ber"}).fetchall()
            gantt_s(*prepare_for_gantt(pocet_stroju))
        if v is not None:
            pocet_stroju = cursor.execute("select * from Kombinace where vin=:v",
                                          {"v": v, "ber": "ber"}).fetchall()
            gantt_v(*prepare_for_gantt(pocet_stroju))
        if k is not None:
            pocet_stroju = cursor.execute("select * from Kombinace where konfig_id=:k",
                                          {"k": k, "ber": "ber"}).fetchall()
            gantt_k(*prepare_for_gantt(pocet_stroju))
        print(pocet_stroju)

        connection.commit()
        connection.close()

    def plot_operational_data(ser_cislo, konfig, stroj, vodorovna, svisla):
        connection = sqlite3.connect('zemedelske_stroje.db')
        cursor = connection.cursor()



        data = cursor.execute("select * from Zaznamy "
                                "inner join Kombinace on Zaznamy.seriove_cislo=Kombinace.seriove_cislo "
                              "where Zaznamy.seriove_cislo = '88855662024772572239' and Kombinace.konfig_id = 'A3M16'").fetchall()

        dotaz = cursor.execute("select z.cas, Data_.atribut, Data_.bit_val, Data_.float_val from Zaznamy z "
                               "join "
                               "(select * from Kombinace where seriove_cislo =:ser and vin =:vin and konfig_id =:konf)a "
                               "on (z.seriove_cislo=a.seriove_cislo) "
                               "join Data_ "
                               "on (z.zaznam_id=Data_.zaznam_id) "
                               "where a.od <= z.cas and a.do >= z.cas", {"ser": ser_cislo, "vin": stroj, "konf": konfig}).fetchall()

        rychlost = []
        napeti = []
        akc = []
        bocni = []
        tenA = []
        tenB = []
        ora = []
        seje = []
        cas = []

        print(dotaz)

        for one in dotaz:
            cas.append(one[0])
            if one[1] == 'speed':
                rychlost.append(one[3])
            if one[1] == 'napeti':
                napeti.append(one[3])
            if one[1] == 'akcelerace':
                akc.append(one[3])
            if one[1] == 'bocni_pretizeni':
                bocni.append(one[3])
            if one[1] == 'tenzometr_a':
                tenA.append(one[3])
            if one[1] == 'tenzometr_b':
                tenB.append(one[3])
            if one[1] == 'ora':
                ora.append(one[2])
            if one[1] == 'seje':
                seje.append(one[2])
        connection.commit()
        connection.close()
        X = 0
        Y = 0
        if vodorovna == "rychlost":
            X = rychlost
        if vodorovna == "napeti":
            X = napeti
        if vodorovna == "akcelerace":
            X = akc
        if vodorovna == "bocni_pretizeni":
            X = bocni
        if vodorovna == "tenzometr_a":
            X = tenA
        if vodorovna == "tenzometr_b":
            X = tenB
        if vodorovna == "ora":
            X = ora
        if vodorovna == "seje":
            X = seje
        if vodorovna == "cas":
            X = list(set(cas))

            
        if svisla == "rychlost":
            Y = rychlost
        if svisla == "napeti":
            Y = napeti
        if svisla == "akcelerace":
            Y = akc
        if svisla == "bocni_pretizeni":
            Y = bocni
        if svisla == "tenzometr_a":
            Y = tenA
        if svisla == "tenzometr_b":
            Y = tenB
        if svisla == "ora":
            Y = ora
        if svisla == "seje":
            Y = seje
        if svisla == "cas":
            Y = list(set(cas))

        if svisla == "cas":
            X = [x for _, x in sorted(zip(Y, X))]
        if vodorovna == "cas":
            Y = [y for _, y in sorted(zip(X, Y))]
        print(len(X))
        print(len(Y))
        plt.plot(X, Y, '.')
        plt.show()

    def average_filter(promenna, od, do):
        connection = sqlite3.connect('zemedelske_stroje.db')
        cursor = connection.cursor()

        if do == ".." and od == "..":
            dotaz = cursor.execute(
                "select avg(Data_.float_val) as prumer, a.vin, a.seriove_cislo from Zaznamy z join (select * from"
                " Kombinace)a on (z.seriove_cislo=a.seriove_cislo) join Data_ on"
                " (z.zaznam_id=Data_.zaznam_id) "
                "where a.od <= z.cas and a.do >= z.cas and Data_.atribut =:promenna group by a.vin, a.seriove_cislo order by prumer desc",
                {"promenna": promenna}).fetchall()

        elif do != ".." and od != "..":
            od = time.mktime(datetime.datetime.strptime(od, "%d.%m.%Y").timetuple())
            do = time.mktime(datetime.datetime.strptime(do, "%d.%m.%Y").timetuple())

            dotaz = cursor.execute("select avg(Data_.float_val) as prumer, a.vin, a.seriove_cislo from Zaznamy z join (select * from"
                                   " Kombinace)a on (z.seriove_cislo=a.seriove_cislo) join Data_ on"
                                   " (z.zaznam_id=Data_.zaznam_id) "
                                   "where a.od <= z.cas and a.do >= z.cas and z.cas <=:doc and z.cas >=:odc and"
                                   " Data_.atribut =:promenna group by a.vin, a.seriove_cislo order by prumer desc",
                                   {"odc": od, "doc": do, "promenna":promenna}).fetchall()


        print_filter_output(dotaz)
        connection.commit()
        connection.close()
    def basic_info():
        connection = sqlite3.connect('zemedelske_stroje.db')
        cursor = connection.cursor()

        pocet_stroju = cursor.execute("select count(*) from Stroj").fetchone()[0]
        pocet_konfiguraci = cursor.execute("select count(*) from Konfigurace").fetchone()[0]
        pocet_jednotek = cursor.execute("select count(*) from Jednotka").fetchone()[0]
        pocet_zaznamu = cursor.execute("select count(*) from Zaznamy").fetchone()[0]

        connection.commit()
        connection.close()
        return [pocet_stroju, pocet_konfiguraci, pocet_jednotek, pocet_zaznamu]

    def ser_cisla(konfig=None, vin=None):
        connection = sqlite3.connect('zemedelske_stroje.db')
        cursor = connection.cursor()
        if konfig is None and vin is None:
            ser_cisla = cursor.execute("select * from Jednotka").fetchall()
        elif konfig is not None and vin is not None:
            ser_cisla = cursor.execute("select distinct seriove_cislo from Kombinace where konfig_id=:konf and vin=:vin", {"konf": konfig, "vin": vin}).fetchall()
        elif konfig is None and vin is not None:
            ser_cisla = cursor.execute("select distinct seriove_cislo from Kombinace where vin=:vin", {"vin": vin}).fetchall()
        elif konfig is not None and vin is None:
            ser_cisla = cursor.execute("select distinct seriove_cislo from Kombinace where konfig_id=:konf", {"konf": konfig}).fetchall()

        connection.commit()
        connection.close()
        return ser_cisla

    def konfigy(ser=None):
        connection = sqlite3.connect('zemedelske_stroje.db')
        cursor = connection.cursor()
        if ser is None:
            konfigy = cursor.execute("select * from Konfigurace").fetchall()
        elif ser is not None:
            konfigy = cursor.execute("select distinct konfig_id from Kombinace where seriove_cislo=:ser", {"ser":ser}).fetchall()

        connection.commit()
        connection.close()
        return konfigy

    def viny(ser=None, konf=None):
        connection = sqlite3.connect('zemedelske_stroje.db')
        cursor = connection.cursor()

        viny = cursor.execute("select * from Stroj").fetchall()

        connection.commit()
        connection.close()
        return viny

    def kombinace(vin=None):
        connection = sqlite3.connect('zemedelske_stroje.db')
        cursor = connection.cursor()

        komb = cursor.execute("select distinct seriove_cislo from Kombinace").fetchall()

        connection.commit()
        connection.close()
        return komb

    def find_kombinace(s=None, v=None, k=None):
        connection = sqlite3.connect('zemedelske_stroje.db')
        cursor = connection.cursor()
        if s is not None:
            komb = cursor.execute("select distinct seriove_cislo from Kombinace where seriove_cislo like ?", (s+'%',)).fetchall()
            updatevalss(komb)
        if v is not None:
            komb = cursor.execute("select distinct vin from Kombinace where vin like ?", (v+'%',)).fetchall()
            updatevalsv(komb)
        if k is not None:
            komb = cursor.execute("select distinct konfig_id from Kombinace where konfig_id like ?", (k+'%',)).fetchall()
            updatevalsk(komb)




        connection.commit()
        connection.close()

        return komb

    def find_kombinace_for_drives(ser=None, kon=None, vin=None):
        connection = sqlite3.connect('zemedelske_stroje.db')
        cursor = connection.cursor()
        if ser != '' and kon == '' and vin == '':
            komb = cursor.execute("select distinct seriove_cislo, vin, konfig_id from Kombinace where seriove_cislo like ?", (ser+'%',)).fetchall()
        if ser == '' and kon != '' and vin == '':
            komb = cursor.execute("select distinct seriove_cislo, vin, konfig_id from Kombinace where konfig_id like ?", (kon+'%',)).fetchall()
        if ser == '' and kon == '' and vin != '':
            komb = cursor.execute("select distinct seriove_cislo, vin, konfig_id from Kombinace where vin like ?", (vin+'%',)).fetchall()

        if ser != '' and kon != '' and vin == '':
            komb = cursor.execute("select distinct seriove_cislo, vin, konfig_id from Kombinace where seriove_cislo like ? and konfig_id like ?", (ser+'%', '%'+kon+'%')).fetchall()
        if ser != '' and kon == '' and vin != '':
            komb = cursor.execute("select distinct seriove_cislo, vin, konfig_id from Kombinace where seriove_cislo like ? and vin like ?", (ser+'%', '%'+vin+'%')).fetchall()
        if ser == '' and kon != '' and vin != '':
            komb = cursor.execute("select distinct seriove_cislo, vin, konfig_id from Kombinace where konfig_id like ? and vin like ?", (kon+'%', '%'+vin+'%')).fetchall()

        if ser != '' and kon != '' and vin != '':
            komb = cursor.execute("select seriove_cislo, vin, konfig_id from Kombinace where seriove_cislo like ? and vin like ? and konfig_id like ?", (ser+'%', '%'+kon+'%', '%'+vin+'%')).fetchall()

        connection.commit()
        connection.close()
        sers = []
        kons = []
        vins =[]
        for one in komb:
            sers.append(one[0])
            vins.append(one[1])
            kons.append(one[2])
        updatecomboxes(list(set(sers)), list(set(kons)), list(set(vins)))
        print(komb)

        return komb

    def run_query(dotaz):
        connection = sqlite3.connect('zemedelske_stroje.db')
        cursor = connection.cursor()

        result = cursor.execute(dotaz).fetchall()

        connection.commit()
        connection.close()
        print_output(result)

    #zalozka jedna
    plot_button = Button(tab1, text="Zobrazit", command=graph)
    plot_button.grid(row=3, column=0)

    searchentry = Entry(tab1, width=30)
    searchentry.grid(row=0, column=1, padx=20)

    searchentry2 = Entry(tab1, width=30)
    searchentry2.grid(row=1, column=1, padx=20)

    searchentry3 = Entry(tab1, width=30)
    searchentry3.grid(row=2, column=1, padx=20)

    firstlabel = Label(tab1, text="VIN")
    firstlabel.grid(row=0, column=0)

    firstlabel = Label(tab1, text="Seriove cislo")
    firstlabel.grid(row=1, column=0)

    firstlabel = Label(tab1, text="Konfigurace")
    firstlabel.grid(row=2, column=0)

    b_info = basic_info()

    firstlabel = Label(tab1, text="Pocet stroju")
    firstlabel.grid(row=4, column=0)

    firstlabel = Label(tab1, text="Pocet konfiguraci")
    firstlabel.grid(row=5, column=0)

    firstlabel = Label(tab1, text="Pocet jednotek")
    firstlabel.grid(row=6, column=0)

    firstlabel = Label(tab1, text="Pocet zaznamu")
    firstlabel.grid(row=7, column=0)

    value1 = Label(tab1, text=str(b_info[0]))
    value1.grid(row=4, column=1)

    value2 = Label(tab1, text=str(b_info[1]))
    value2.grid(row=5, column=1)

    value3 = Label(tab1, text=str(b_info[2]))
    value3.grid(row=6, column=1)

    value4 = Label(tab1, text=str(b_info[3]))
    value4.grid(row=7, column=1)

    #zalozka gantt chart
    searchl = Label(tab2, text="Hledej")
    searchl.grid(row=0, column=0)

    searchs = Entry(tab2)
    searchs.grid(row=0, column=1)

    search_button = Button(tab2, text="Hledej", command=lambda: find_kombinace(s=searchs.get()))
    search_button.grid(row=0, column=2)

    firstlabel = Label(tab2, text="Seriove cislo")
    firstlabel.grid(row=1, column=0)

    cbs = ttk.Combobox(tab2, values=kombinace())
    cbs.grid(row=1, column=1)
    values = ["jedna", "dva"]
    def updatevalss(values):
        cbs['values'] = values

    plot_button = Button(tab2, text="Zobrazit", command=lambda : gantt_chart(s=cbs.get()))
    plot_button.grid(row=3, column=0)

    searchl = Label(tab2, text="Hledej")
    searchl.grid(row=4, column=0)

    searchv = Entry(tab2)
    searchv.grid(row=4, column=1)

    search_button = Button(tab2, text="Hledej", command=lambda: find_kombinace(v=searchv.get()))
    search_button.grid(row=4, column=2)

    firstlabel = Label(tab2, text="VIN")
    firstlabel.grid(row=5, column=0)

    cbv = ttk.Combobox(tab2, values=kombinace())
    cbv.grid(row=5, column=1)
    values = ["jedna", "dva"]
    def updatevalsv(values):
        cbv['values'] = values

    plot_button = Button(tab2, text="Zobrazit", command=lambda : gantt_chart(v=cbv.get()))
    plot_button.grid(row=6, column=0)

    searchl = Label(tab2, text="Hledej")
    searchl.grid(row=7, column=0)

    searchk = Entry(tab2)
    searchk.grid(row=7, column=1)

    search_button = Button(tab2, text="Hledej", command=lambda: find_kombinace(k=searchk.get()))
    search_button.grid(row=7, column=2)

    firstlabel = Label(tab2, text="Konfigurace")
    firstlabel.grid(row=8, column=0)

    cbk = ttk.Combobox(tab2, values=kombinace())
    cbk.grid(row=8, column=1)
    values = ["jedna", "dva"]
    def updatevalsk(values):
        cbk['values'] = values

    plot_button = Button(tab2, text="Zobrazit", command=lambda : gantt_chart(k=cbk.get()))
    plot_button.grid(row=9, column=0)

    #zalozka jizdni data
    firstlabel = Label(tab3, text="Seriove cislo")
    firstlabel.grid(row=0, column=0)

    cb1 = ttk.Combobox(tab3, values=kombinace())
    cb1.grid(row=0, column=1)
    cb1.bind("<<ComboboxSelected>>", (konfigy(cb1.get())))
    cb1.current(0)

    firstlabel = Label(tab3, text="Konfigurace")
    firstlabel.grid(row=1, column=0)

    cb2 = ttk.Combobox(tab3, values=konfigy())
    cb2.grid(row=1, column=1)
    cb2.current(7)

    firstlabel = Label(tab3, text="VIN")
    firstlabel.grid(row=2, column=0)

    cb3 = ttk.Combobox(tab3, values=viny())
    cb3.grid(row=2, column=1)
    cb3.current(0)

    search1 = Entry(tab3)
    search1.grid(row=0, column=2)

    search2 = Entry(tab3)
    search2.grid(row=1, column=2)

    search3 = Entry(tab3)
    search3.grid(row=2, column=2)

    search_button2 = Button(tab3, text="Hledej", command=lambda: find_kombinace_for_drives(search1.get(), search2.get(), search3.get()))
    search_button2.grid(row=1, column=3)

    def updatecomboxes(ser, kon, vin):
        cb1['values'] = ser
        cb2['values'] = kon
        cb3['values'] = vin

    vodolabel = Label(tab3, text="Vodorovna osa")
    vodolabel.grid(row=5, column=0)

    vodolabel = Label(tab3, text="Svisla osa")
    vodolabel.grid(row=5, column=1)

    g1vodo = StringVar()
    R1 = Radiobutton(tab3, text="Rychlost", variable=g1vodo, value="rychlost")
    R2 = Radiobutton(tab3, text="Napeti", variable=g1vodo, value="napeti")
    R3 = Radiobutton(tab3, text="Akcelerace", variable=g1vodo, value="akcelerace")
    R4 = Radiobutton(tab3, text="Bocni pretizeni", variable=g1vodo, value="bocni_pretizeni")
    R5 = Radiobutton(tab3, text="Tenzometr A", variable=g1vodo, value="tenzometr_a")
    R6 = Radiobutton(tab3, text="Tenzometr B", variable=g1vodo, value="tenzometr_b")
    R7 = Radiobutton(tab3, text="Ora", variable=g1vodo, value="ora")
    R8 = Radiobutton(tab3, text="Seje", variable=g1vodo, value="seje")
    R18 = Radiobutton(tab3, text="Cas", variable=g1vodo, value="cas")
    g1hor = StringVar()
    R9 = Radiobutton(tab3, text="Rychlost", variable=g1hor, value="rychlost")
    R10 = Radiobutton(tab3, text="Napeti", variable=g1hor, value="napeti")
    R11 = Radiobutton(tab3, text="Akcelerace", variable=g1hor, value="akcelerace")
    R12 = Radiobutton(tab3, text="Bocni pretizeni", variable=g1hor, value="bocni_pretizeni")
    R13 = Radiobutton(tab3, text="Tenzometr A", variable=g1hor, value="tenzometr_a")
    R14 = Radiobutton(tab3, text="Tenzometr B", variable=g1hor, value="tenzometr_b")
    R15 = Radiobutton(tab3, text="Ora", variable=g1hor, value="ora")
    R16 = Radiobutton(tab3, text="Seje", variable=g1hor, value="seje")
    R17 = Radiobutton(tab3, text="Cas", variable=g1hor, value="cas")

    R1.grid(row=6, column=0)
    R2.grid(row=7, column=0)
    R3.grid(row=8, column=0)
    R4.grid(row=9, column=0)
    R5.grid(row=10, column=0)
    R6.grid(row=11, column=0)
    R7.grid(row=12, column=0)
    R8.grid(row=13, column=0)
    R18.grid(row=14, column=0)

    R9.grid(row=6, column=1)
    R10.grid(row=7, column=1)
    R11.grid(row=8, column=1)
    R12.grid(row=9, column=1)
    R13.grid(row=10, column=1)
    R14.grid(row=11, column=1)
    R15.grid(row=12, column=1)
    R16.grid(row=13, column=1)
    R17.grid(row=14, column=1)

    plot_button = Button(tab3, text="Zobrazit", command=lambda: plot_operational_data(cb1.get(), cb2.get(), cb3.get(), g1vodo.get(), g1hor.get()))
    plot_button.grid(row=15, column=0)

    #zalozka dotazy

    oknonadotaz = Text(tab4, height=10)
    oknonadotaz.grid(row=0, column=0)

    dotazbutton = Button(tab4, text="Spustit", command=lambda: run_query(oknonadotaz.get("1.0", END)))
    dotazbutton.grid(row=1, column=0)

    dotazvyzstup = Text(tab4, height=5)
    dotazvyzstup.grid(row=2, column=0)
    def print_output(result):
        dotazvyzstup.delete("1.0", END)
        dotazvyzstup.insert("1.0", result)

    #zalozka prumery

    prlabel = Label(tab5, text="Prumer z promenne")
    prlabel.grid(row=0, column=0)

    promenne = ["speed", "akcelerace", "napeti", "bocni_pretizeni", "tenzometr_a", "tenzometr_b", "ora", "seje"]
    cbpr = ttk.Combobox(tab5, values=promenne)
    cbpr.grid(row=0, column=1)
    cbpr.current(0)

    pr1label = Label(tab5, text="V casovem intervalu")
    pr1label.grid(row=1, column=0)

    pr2label = Label(tab5, text="Od")
    pr2label.grid(row=1, column=1)

    pr3label = Label(tab5, text="den/mesic/rok")
    pr3label.grid(row=2, column=1)

    pr4label = Label(tab5, text="den/mesic/rok")
    pr4label.grid(row=4, column=1)

    day1 = Entry(tab5, width=2)
    day1.grid(row=2, column=2)

    month1 = Entry(tab5, width=2)
    month1.grid(row=2, column=3)

    year1 = Entry(tab5, width=4)
    year1.grid(row=2, column=4)

    pr3label = Label(tab5, text="Do")
    pr3label.grid(row=3, column=1)

    day2 = Entry(tab5, width=2)
    day2.grid(row=4, column=2)

    month2 = Entry(tab5, width=2)
    month2.grid(row=4, column=3)

    year2 = Entry(tab5, width=4)
    year2.grid(row=4, column=4)

    prbutton = Button(tab5, text="Zobraz", command=lambda : average_filter(cbpr.get(),
                    (day1.get() + "." + month1.get() + "." + year1.get()), (day2.get() + "." + month2.get() + "." + year2.get())))
    prbutton.grid(row=6, column=0)

    filtrvyzstup = Text(tab5, height=5)
    filtrvyzstup.grid(row=8, column=4)

    def print_filter_output(result):
        filtrvyzstup.delete("1.0", END)
        filtrvyzstup.insert("1.0", result)

    root.mainloop()
    

'''
#queries
pocet_stroju = cursor.execute("select count(*) from Stroj").fetchone()
pocet_konfiguraci = cursor.execute("select count(*) from Konfigurace").fetchone()
pocet_jednotek = cursor.execute("select count(*) from Jednotka").fetchone()
pocet_zaznamu = cursor.execute("select count(*) from Zaznamy").fetchone()

#najdi rychlosti, akcelerace stroje s konkretni jednotkou v casovem intervalu pouzij LAG
jizda = cursor.execute("select * from Zaznamy")
'''