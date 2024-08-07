import time
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


# strptime - преобразует строку в обьект datetime который уже можно адекватно сравнивать
# strftime - преобразует обратно обьект в строку

def all_dates(date_s, date_e="01.01.2000"):
    if datetime.strptime(date_s, "%d.%m.%Y") < datetime.strptime(date_e, "%d.%m.%Y"):
        date_s, date_e = date_e, date_s
    c_date = datetime.strptime(date_s, "%d.%m.%Y")
    end_date = datetime.strptime(date_e, "%d.%m.%Y")
    if c_date > datetime.strptime(current_date(), "%d.%m.%Y"):
        c_date = datetime.strptime(current_date(), "%d.%m.%Y")
    dates = []
    while c_date >= end_date:
        dates.append(c_date.strftime("%d.%m.%Y"))
        c_date -= timedelta(days=1)
    return dates


def current_date():
    date = time.strftime("%x").split("/")
    date[0], date[1], date[2] = date[1], date[0], time.strftime("%Y")
    date = (".").join(date)
    return date


def convert_num(cursor):
    return list(map(lambda x: [x[0], x[1], x[2], float(x[3]), x[4]], cursor.fetchall()))


def convert_year(date1, date2):
    tmp1 = datetime.strftime(datetime.strptime(date1, "%Y"), "%d.%m.%Y")
    tmp2 = datetime.strftime(datetime.strptime(date2, "%Y") - timedelta(days=1), "%d.%m.%Y")
    return [tmp1, tmp2]


def check_the_date(date):
    data = date.split("-")
    try:
        for i in data:
            if datetime.strptime(i, "%d.%m.%Y") < datetime.strptime("01.01.2000", "%d.%m.%Y"):
                return None
    except ValueError:
        try:
            for i in data:
                a = datetime.strptime(i, "%Y")
                if a < datetime.strptime("01.01.2000", "%d.%m.%Y"):
                    return None
        except ValueError:
            return None
        else:
            if len(data) == 2:
                return 4
            return 3
    else:
        if len(data) == 2:
            return 2
        return 1


def create_graph(data, buf):
    for tmp in data:
        plt.plot([x[4] for x in tmp], [round(y[3] / y[2], 3) for y in tmp], label=tmp[0][0], marker='o')
    plt.legend()
    plt.title("Курс выбранной валюты / выбранных валют")
    plt.xlabel("число")
    plt.ylabel("цена в руб за ед")
    plt.grid(True)
    plt.savefig(buf, format='png')
    plt.close()



