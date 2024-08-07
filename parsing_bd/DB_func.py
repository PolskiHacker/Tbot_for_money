import io
import psycopg2
from config_reader import config
from another_func.date_math_im_func import all_dates, current_date, \
    convert_num, check_the_date, convert_year, create_graph
from parsing import parsing_money_info


con = psycopg2.connect(dbname='postgres', user='postgres',
                       password=config.db_password.get_secret_value(),
                       host='localhost')
cursor = con.cursor()


def check():
    dates = all_dates(current_date())
    info = f"""SELECT name, abbreviation, units, r_equivalent, date FROM public.money_info;"""
    cursor.execute(info)
    data = cursor.fetchall()
    if len(data) == 0:
        send_info_to_db(dates)
    else:
        send_info_to_db(dates[:dates.index(data[-1][-1])])


def send_info_to_db(dates):
    for date in dates[::-1]:
        data = parsing_money_info(date)
        for tmp in data:
            inserting = f"""INSERT INTO public.money_info(name, abbreviation, units, r_equivalent, date) VALUES ('{tmp[1]}', '{tmp[0]}', {tmp[2]}, {tmp[3]}, '{tmp[4]}');"""
            cursor.execute(inserting)
        con.commit()


def take_current_day_info(date):
    info = f"""SELECT name, abbreviation, units, r_equivalent, date FROM public.money_info WHERE date='{date}';"""
    cursor.execute(info)
    data = convert_num(cursor)
    text = ''
    for i, j in enumerate(data, start=1):
        if j[2] == 1:
            text += f"{i}) {j[0]}: <b>1</b> единица этой валюты стоит <b>{j[3]}₽</b>\n"
        else:
            text += f"{i}) {j[0]}: <b>{j[2]}</b> единиц этой валюты стоят <b>{j[3]}₽</b>\n"
    return text


def all_names():
    info = "SELECT name FROM public.money_info;"
    cursor.execute(info)
    data = [x[0].lower() for x in sorted(list(set(cursor.fetchall())))]
    return data


def search(data):
    if type(data) == str:
        if data.lower() in all_names():
            name_of_currency, date = data, None
        else:
            name_of_currency, date = None, data
    else:
        name_of_currency, date = data[0], data[1]
    info = "SELECT name, abbreviation, units, r_equivalent, date FROM public.money_info WHERE 1=1"
    if name_of_currency:
        info += f" and name ILIKE '%{name_of_currency}%'"
    if date:
        tmp = check_the_date(date)
        if tmp == 1:
            info += f" and date='{date}'"
        elif tmp == 2:
            temp = date.split("-")
            dates = all_dates(temp[1], temp[0])
            info += " and ("
            for i in dates[::-1]:
                info += f"date='{i}' or "
            info = info[:-4] + ")"
        elif tmp == 3:
            data = convert_year(date, str(int(date) + 1))
            dates = all_dates(data[1], data[0])
            info += " and ("
            for i in dates[::-1]:
                info += f"date='{i}' or "
            info = info[:-4] + ")"
        elif tmp == 4:
            temp = date.split("-")
            data = convert_year(temp[0], str(int(temp[1]) + 1))
            dates = all_dates(data[1], data[0])
            info += " and ("
            for i in dates[::-1]:
                info += f"date='{i}' or "
            info = info[:-4] + ")"
        else:
            return None
    cursor.execute(info)
    return convert_num(cursor)


def check_graph(currency):
    info = "SELECT question, im_data FROM public.graphes WHERE question = %s;"
    cursor.execute(info, (currency.lower(),))
    data = cursor.fetchone()
    if data:
        return data
    return None


def new_graph(currency, data):
    buf = io.BytesIO()
    temp = []
    for tmp in data:
        temp.append(search(tmp))
    create_graph(temp, buf)
    buf.seek(0)
    inserting = "INSERT INTO public.graphes(question, im_data) VALUES (%s, %s)"
    cursor.execute(inserting, (currency.lower(), buf.getvalue()))
    con.commit()
    return buf.getvalue()


if __name__ == "__main__":
    # check()
    #print(search(['Австралийский доллар', '30.07.2024']))
    """print(take_current_day_info('30.07.2024'))"""
    #print(search(['Доллар сша 30.07.2024-03.08.2024']))
    new_graph('Доллар сша', ['Доллар сша'])
    #print(check_graph('Доллар сша 30.07.2024-03.08.2024, евро 30.07.2024-03.08.2024'))
    # print(search('Доллар сша 2024-2025'))
