from unittest.mock import mock_open, patch

from app.currency.utils import (
    convert_data_to_list,
    generate_csv_string_from_dict,
    is_valid_date_format,
    make_data_to_insert,
    save_all_currencies_to_csv_file,
    save_new_line_to_csv_file,
    save_specific_currencies_to_csv_file,
)


def test_convert_data_to_list():
    data = [{"mid": 1}, {"mid": 2}, {"mid": 3}]
    result = convert_data_to_list(data)
    assert result == [1, 2, 3]


def test_generate_csv_string_from_dict():
    data = {"column1": "value1", "column2": "value2", "column3": "value3"}
    list_of_columns = ["column1", "column2", "column3"]
    result = generate_csv_string_from_dict(data, list_of_columns)
    assert result == "value1,value2,value3"


def test_make_data_to_insert():
    eur_pln = [1, 2, 3]
    usd_pln = [4, 5, 6]
    chf_pln = [7, 8, 9]
    eur_usd = [10, 11, 12]
    chf_usd = [13, 14, 15]
    rate_dates = ["2022-01-01", "2022-01-02", "2022-01-03"]
    result = make_data_to_insert(eur_pln, usd_pln, chf_pln, eur_usd, chf_usd, rate_dates)
    assert len(result) == 3
    assert result[0]["eur_pln"] == 1
    assert result[0]["usd_pln"] == 4
    assert result[0]["chf_pln"] == 7
    assert result[0]["eur_usd"] == 10
    assert result[0]["chf_usd"] == 13
    assert result[0]["rate_date"] == "2022-01-01"


@patch("builtins.open", new_callable=mock_open)
def test_save_all_currencies_to_csv_file(mock_file):
    currencies = [
        {"eur_pln": 1, "usd_pln": 4, "chf_pln": 7, "eur_usd": 10, "chf_usd": 13, "rate_date": "2022-01-01"},
        {"eur_pln": 2, "usd_pln": 5, "chf_pln": 8, "eur_usd": 11, "chf_usd": 14, "rate_date": "2022-01-02"},
        {"eur_pln": 3, "usd_pln": 6, "chf_pln": 9, "eur_usd": 12, "chf_usd": 15, "rate_date": "2022-01-03"},
    ]
    save_all_currencies_to_csv_file(currencies)
    mock_file.assert_called_once_with("files/all_currency_data.csv", "w")


@patch("builtins.open", new_callable=mock_open)
def test_save_specific_currencies_to_csv_file(mock_file):
    currencies = [
        {"eur_pln": 1, "usd_pln": 4, "chf_pln": 7, "eur_usd": 10, "chf_usd": 13, "rate_date": "2022-01-01"},
        {"eur_pln": 2, "usd_pln": 5, "chf_pln": 8, "eur_usd": 11, "chf_usd": 14, "rate_date": "2022-01-02"},
        {"eur_pln": 3, "usd_pln": 6, "chf_pln": 9, "eur_usd": 12, "chf_usd": 15, "rate_date": "2022-01-03"},
    ]
    columns = ["eur_pln", "usd_pln", "chf_pln", "eur_usd", "chf_usd", "rate_date"]
    filename = "eur_pln_usd_pln"
    save_specific_currencies_to_csv_file(currencies, columns, filename)
    mock_file.assert_called_once_with("files/eur_pln_usd_pln_currency_data.csv", "w")


@patch("builtins.open", new_callable=mock_open)
def test_save_new_line_to_csv_file(mock_file):
    data = {"eur_pln": 1, "usd_pln": 4, "chf_pln": 7, "eur_usd": 10, "chf_usd": 13, "rate_date": "2022-01-01"}
    filename = "all_currency_data.csv"
    save_new_line_to_csv_file(data, filename)
    mock_file.assert_called_once_with("files/all_currency_data.csv", mode="a", newline="")


def test_is_valid_date_format_with_valid_dates():
    start_date = "2023-01-01"
    end_date = "2023-12-31"
    result, error = is_valid_date_format(start_date, end_date)
    assert result == True
    assert error is None


def test_is_valid_date_format_with_invalid_start_date():
    start_date = "2023-01-32"  # Invalid day
    end_date = "2023-12-31"
    result, error = is_valid_date_format(start_date, end_date)
    assert result == False
    assert error == "unconverted data remains: 2"


def test_is_valid_date_format_with_invalid_end_date():
    start_date = "2023-01-01"
    end_date = "2023-13-01"  # Invalid month
    result, error = is_valid_date_format(start_date, end_date)
    assert result == False
    assert error == "time data '2023-13-01' does not match format '%Y-%m-%d'"
