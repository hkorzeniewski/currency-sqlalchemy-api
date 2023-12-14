import csv
from datetime import datetime


def convert_data_to_list(data: list, parameter: str = "mid"):
    rate_list = []
    for value in data:
        rate_list.append(value[parameter])
    # print(rate_list)
    return rate_list


def generate_csv_string_from_dict(data: dict, list_of_columns: list):
    csv_string = ""
    for column in list_of_columns:
        csv_string += f"{data[column]},"
    return csv_string[:-1]


def make_data_to_insert(eur_pln, usd_pln, chf_pln, eur_usd, chf_usd, rate_dates):
    data_to_insert = [
        {
            "eur_pln": eur,
            "usd_pln": usd,
            "chf_pln": chf,
            "eur_usd": eur_usd,
            "chf_usd": chf_usd,
            "rate_date": rate_date,
        }
        for eur, usd, chf, eur_usd, chf_usd, rate_date in zip(eur_pln, usd_pln, chf_pln, eur_usd, chf_usd, rate_dates)
    ]
    return data_to_insert


def save_all_currencies_to_csv_file(currencies: dict, filename: str = "all_currency_data.csv"):
    with open(f"files/{filename}", "w") as f:
        f.write("eur_pln,usd_pln,chf_pln,eur_usd,chf_usd,rate_date\n")
        for currency in currencies:
            f.write(
                f"{currency['eur_pln']},{currency['usd_pln']},{currency['chf_pln']},{currency['eur_usd']},{currency['chf_usd']},{currency['rate_date']}\n"
            )


def save_specific_currencies_to_csv_file(currencies: list, columns: list, filename: str):
    with open(f"files/{filename}_currency_data.csv", "w") as f:
        f.write(f'{",".join(column for column in columns)}\n')
        for currency in currencies:
            f.write(f"{generate_csv_string_from_dict(currency, columns)}\n")


def save_new_line_to_csv_file(data: dict, filename: str):
    with open(f"files/{filename}", mode="a", newline="") as file:
        writer = csv.writer(file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(
            [data["eur_pln"], data["usd_pln"], data["chf_pln"], data["eur_usd"], data["chf_usd"], data["rate_date"]]
        )


def is_valid_date_format(start_date, end_date):
    try:
        datetime.strptime(start_date, "%Y-%m-%d")
        datetime.strptime(end_date, "%Y-%m-%d")
        return True, None
    except ValueError as e:
        return False, str(e)
