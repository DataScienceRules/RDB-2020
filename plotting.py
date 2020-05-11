from matplotlib import pyplot as plt
import matplotlib.dates as md

def gantt_s(vins, od, do, konfigs, serias):
    plt.subplot(211)
    plt.title("Jednotka: " + str(serias[0]))
    plt.ylabel("VIN")
    plt.hlines(vins, od, do, colors="red")
    plt.margins(0.2)
    plt.xticks(rotation=25)
    dtf = md.DateFormatter('%d.%m.')
    ax = plt.gca()
    ax.xaxis.set_major_formatter(dtf)

    plt.subplot(212)
    plt.ylabel("Konfigurace")
    plt.xlabel("Cas")
    plt.hlines(konfigs, od, do, colors="blue")
    plt.margins(0.2)
    plt.xticks(rotation=25)
    dtf = md.DateFormatter('%d.%m.')
    ax = plt.gca()
    ax.xaxis.set_major_formatter(dtf)

    plt.show()

def gantt_v(vins, od, do, konfigs, serias):

    plt.subplot(211)
    plt.title("VIN: " + str(vins[0]))
    plt.ylabel("Jednotka")
    plt.hlines(serias, od, do, colors="red")
    plt.margins(0.2)
    plt.xticks(rotation=25)
    dtf = md.DateFormatter('%d.%m.')
    ax = plt.gca()
    ax.xaxis.set_major_formatter(dtf)

    plt.subplot(212)
    plt.ylabel("Konfigurace")
    plt.xlabel("Cas")
    plt.hlines(konfigs, od, do, colors="blue")
    plt.margins(0.2)
    plt.xticks(rotation=25)
    dtf = md.DateFormatter('%d.%m.')
    ax = plt.gca()
    ax.xaxis.set_major_formatter(dtf)

    plt.show()

def gantt_k(vins, od, do, konfigs, serias):
    plt.subplot(211)
    plt.title("Konfigurace: " + str(konfigs[0]))
    plt.ylabel("VIN")
    plt.hlines(vins, od, do, colors="red")
    plt.margins(0.2)
    plt.xticks(rotation=25)
    dtf = md.DateFormatter('%d.%m.')
    ax = plt.gca()
    ax.xaxis.set_major_formatter(dtf)

    plt.subplot(212)
    plt.ylabel("Jednotka")
    plt.xlabel("Cas")
    plt.hlines(serias, od, do, colors="blue")
    plt.margins(0.2)
    plt.xticks(rotation=25)
    dtf = md.DateFormatter('%d.%m.')
    ax = plt.gca()
    ax.xaxis.set_major_formatter(dtf)

    plt.show()