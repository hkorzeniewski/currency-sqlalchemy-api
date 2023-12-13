def convert_data_to_list(data: list, parameter: str = "mid"):
    rate_list = []
    for value in data:
        rate_list.append(value[parameter])
    # print(rate_list)
    return rate_list
