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
