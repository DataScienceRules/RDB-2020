import random, string


def generate_data():
    stroje = []
    jednotky = []
    konfigurace = []
    kombinace = []
    
    with open("stroje.csv", "w", encoding="utf-8") as machinesfile:
        n = 0
        while n < 100:
            letters = string.ascii_lowercase
            digits = string.digits
            vin = "TMBD"+str("".join(random.choices(digits, k=12)))
            machinesfile.write(vin + "\n")
            stroje.append(vin)
            n += 1
    
    with open("jednotky.csv", "w", encoding="utf-8") as unitsfile:
        n = 0
        while n < 110:
            letters = string.ascii_lowercase
            digits = string.digits
            serial_number = str("".join(random.choices(digits, k=20)))
            unitsfile.write(serial_number + "\n")
            jednotky.append(serial_number)
            n += 1
    
    with open("konfigurace.csv", "w", encoding="utf-8") as konfigs_file:
        n = 0
        while n < 10:
            letters = string.ascii_lowercase
            digits = string.digits
            konfig_id = "A" + str("".join(random.choices(digits, k=1))) + "M" + str("".join(random.sample(digits, 3)))
            konfigs_file.write(konfig_id + "\n")
            konfigurace.append(konfig_id)
            n += 1
    
    with open("kombinace.csv", "w", encoding="utf-8") as kombi_file:
        a = random.choices(stroje, k=150)
        b = random.choices(konfigurace, weights=[10, 16, 1, 1, 1, 2, 4, 12, 8, 5], k=150)
        c = random.choices(jednotky, k=150)
    
        for i, (aa, bb, cc) in enumerate(zip(a, b, c)):
            howmany = []
            for id, k in enumerate(kombinace):
                #dve jednotky ve stejny cas v jednom aute
                if k[0] == aa or k[2] == cc or (k[2] == cc and k[1] == bb) or (k[0] == aa and k[1] == bb) or (k[0] == aa and k[2] == cc) or (k[0] == aa and k[1] == bb and k[2] == cc):
                    howmany.append(k[4])
    
            if len(howmany) == 0:
                od = random.randint(1587971791, 1588171791)
                do = random.randint(1588171792, 1588271791)
            else:
                od = random.randint(max(howmany) + 3600, max(howmany) + 100000)
                do = random.randint(max(howmany) + 100001, max(howmany) + 200000)
    
            kombinace.append([aa, bb, cc, od, do])
            line = str(aa) + "," + str(bb) + "," + str(cc) + "," + str(od) + "," + str(do)  + "\n"
            kombi_file.write(line)
    
    
    with open("zaznamy.csv", "w", encoding="utf-8") as zaznamyfile:
        with open("data.csv", "w", encoding="utf-8") as datafile:
            counter = 1
            for komb in kombinace:
                interval = int((komb[4] - komb[3])/20)
                time = komb[3]

                while time < komb[4]:
                    prodlevy = [random.uniform(10, 60), random.uniform(300,30000)]
                    prodleva = random.choices(prodlevy, weights=[10000, 1], k=1)[0]
                    zaznam = str(komb[2]) + "," + str(time+prodleva) + "\n"
                    zaznamyfile.write(zaznam)
    
                    lat = random.uniform(50.9748, 48.7731)
                    lon = random.uniform(12.4909, 18.6223)
                    if komb[1] == konfigurace[4]:
                        pass
                    elif komb[1] == konfigurace[5]:
                        datafile.write(str(counter) + "," + "lat" + ",," + str(lat) + "\n")
                        datafile.write(str(counter) + "," + "lon" + ",," + str(lon) + "\n")
                    elif komb[1] == konfigurace[2]:
                        ora = random.choices([1,0], weights=[8, 2], k=1)[0]
                        seje = random.choices([1,0], weights=[8, 2], k=1)[0]
                        rychlost = random.uniform(0, 30)
                        datafile.write(str(counter) + "," + "lat" + ",," + str(lat) + "\n")
                        datafile.write(str(counter) + "," + "lon" + ",," + str(lon) + "\n")
                        datafile.write(str(counter) + "," + "speed" + ",," + str(rychlost) + "\n")
                        datafile.write(str(counter) + "," + "ora" + "," + str(ora) + "," + "\n")
                        datafile.write(str(counter) + "," + "seje" + "," + str(seje) + "," + "\n")
                    elif komb[1] == konfigurace[3]:
                        napeti = random.uniform(8.0, 18.0)
                        akcelerace = random.uniform(-0.3, 0.3)
                        rychlost = random.uniform(0.0, 30.0)
                        datafile.write(str(counter) + "," + "lat" + ",," + str(lat) + "\n")
                        datafile.write(str(counter) + "," + "lon" + ",," + str(lon) + "\n")
                        datafile.write(str(counter) + "," + "speed" + ",," + str(rychlost) + "\n")
                        datafile.write(str(counter) + "," + "napeti" + ",," + str(napeti) + "\n")
                        datafile.write(str(counter) + "," + "akcelerace" + ",," + str(akcelerace) + "\n")
                    elif komb[1] == konfigurace[0]:
                        napeti = random.uniform(8.0, 18.0)
                        akcelerace = random.uniform(-0.3, 0.3)
                        tenzometr_a = random.uniform(0.0, 50.0)
                        tenzometr_b = random.uniform(0.0, 50.0)
                        datafile.write(str(counter) + "," + "lat" + ",," + str(lat) + "\n")
                        datafile.write(str(counter) + "," + "lon" + ",," + str(lon) + "\n")
                        datafile.write(str(counter) + "," + "tenzometr_a" + ",," + str(tenzometr_a) + "\n")
                        datafile.write(str(counter) + "," + "tenzometr_b" + ",," + str(tenzometr_b) + "\n")
                        datafile.write(str(counter) + "," + "akcelerace" + ",," + str(akcelerace) + "\n")
                    elif komb[1] == konfigurace[1]:
                        napeti = random.uniform(8.0, 18.0)
                        akcelerace = random.uniform(-0.3, 0.3)
                        rychlost = random.uniform(0.0, 30.0)
                        ora = random.choices([1, 0], weights=[8, 2], k=1)[0]
                        seje = random.choices([1, 0], weights=[8, 2], k=1)[0]
                        datafile.write(str(counter) + "," + "lat" + ",," + str(lat) + "\n")
                        datafile.write(str(counter) + "," + "lon" + ",," + str(lon) + "\n")
                        datafile.write(str(counter) + "," + "speed" + ",," + str(rychlost) + "\n")
                        datafile.write(str(counter) + "," + "napeti" + ",," + str(napeti) + "\n")
                        datafile.write(str(counter) + "," + "akcelerace" + ",," + str(akcelerace) + "\n")
                        datafile.write(str(counter) + "," + "ora" + "," + str(ora) + "," + "\n")
                        datafile.write(str(counter) + "," + "seje" + "," + str(seje) + "," + "\n")
                    elif komb[1] == konfigurace[6]:
                        akcelerace = random.uniform(-0.3, 0.3)
                        rychlost = random.uniform(0.0, 30.0)
                        datafile.write(str(counter) + "," + "lat" + ",," + str(lat) + "\n")
                        datafile.write(str(counter) + "," + "lon" + ",," + str(lon) + "\n")
                        datafile.write(str(counter) + "," + "speed" + ",," + str(rychlost) + "\n")
                        datafile.write(str(counter) + "," + "akcelerace" + ",," + str(akcelerace) + "\n")
                    elif komb[1] == konfigurace[7]:
                        akcelerace = random.uniform(-0.3, 0.3)
                        rychlost = random.uniform(0.0, 30.0)
                        ora = random.choices([1, 0], weights=[8, 2], k=1)[0]
                        seje = random.choices([1, 0], weights=[8, 2], k=1)[0]
                        datafile.write(str(counter) + "," + "lat" + ",," + str(lat) + "\n")
                        datafile.write(str(counter) + "," + "lon" + ",," + str(lon) + "\n")
                        datafile.write(str(counter) + "," + "speed" + ",," + str(rychlost) + "\n")
                        datafile.write(str(counter) + "," + "ora" + "," + str(ora) + "," + "\n")
                        datafile.write(str(counter) + "," + "seje" + "," + str(seje) + "," + "\n")
                        datafile.write(str(counter) + "," + "akcelerace" + ",," + str(akcelerace) + "\n")
                    elif komb[1] == konfigurace[8]:
                        napeti = random.uniform(8.0, 18.0)
                        akcelerace = random.uniform(-0.3, 0.3)
                        rychlost = random.uniform(0.0, 30.0)
                        tenzometr_a = random.uniform(0.0, 50.0)
                        tenzometr_b = random.uniform(0.0, 50.0)
                        datafile.write(str(counter) + "," + "lat" + ",," + str(lat) + "\n")
                        datafile.write(str(counter) + "," + "lon" + ",," + str(lon) + "\n")
                        datafile.write(str(counter) + "," + "speed" + ",," + str(rychlost) + "\n")
                        datafile.write(str(counter) + "," + "napeti" + ",," + str(napeti) + "\n")
                        datafile.write(str(counter) + "," + "akcelerace" + ",," + str(akcelerace) + "\n")
                        datafile.write(str(counter) + "," + "tenzometr_a" + ",," + str(tenzometr_a) + "\n")
                        datafile.write(str(counter) + "," + "tenzometr_b" + ",," + str(tenzometr_b) + "\n")
                    elif komb[1] == konfigurace[9]:
                        napeti = random.uniform(8.0, 18.0)
                        akcelerace = random.uniform(-0.3, 0.3)
                        rychlost = random.uniform(0.0, 30.0)
                        ora = random.choices([1, 0], weights=[8, 2], k=1)[0]
                        seje = random.choices([1, 0], weights=[8, 2], k=1)[0]
                        tenzometr_a = random.uniform(0.0, 50.0)
                        tenzometr_b = random.uniform(0.0, 50.0)
                        bocni_pretizeni = random.uniform(-0.02, 0.02)
                        datafile.write(str(counter) + "," + "lat" + ",," + str(lat) + "\n")
                        datafile.write(str(counter) + "," + "lon" + ",," + str(lon) + "\n")
                        datafile.write(str(counter) + "," + "speed" + ",," + str(rychlost) + "\n")
                        datafile.write(str(counter) + "," + "napeti" + ",," + str(napeti) + "\n")
                        datafile.write(str(counter) + "," + "akcelerace" + ",," + str(akcelerace) + "\n")
                        datafile.write(str(counter) + "," + "bocni_pretizeni" + ",," + str(bocni_pretizeni) + "\n")
                        datafile.write(str(counter) + "," + "tenzometr_a" + ",," + str(tenzometr_a) + "\n")
                        datafile.write(str(counter) + "," + "tenzometr_b" + ",," + str(tenzometr_b) + "\n")
                        datafile.write(str(counter) + "," + "ora" + "," + str(ora) + "," + "\n")
                        datafile.write(str(counter) + "," + "seje" + "," + str(seje) + "," + "\n")
                    
                    counter += 1
                    time += prodleva
    

    

