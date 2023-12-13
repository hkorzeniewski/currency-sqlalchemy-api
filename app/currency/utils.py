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
