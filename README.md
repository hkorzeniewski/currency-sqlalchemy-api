# currency-api

# API Documentation

## Introduction
This document provides detailed information on the RESTful API endpoints for managing currency data. The API allows users to retrieve various financial data related to currencies, including average rates, maximum and minimum rates, date ranges, and more.

## Base URL
The base URL for the API is `/api/v1`.

## Endpoints

### 1. Get All Currencies
#### Endpoint
`GET /api/v1/currencies`

#### Description
Retrieve a list of all available currencies.

#### Request
- Method: GET

#### Response
- Status Code: 200 OK
- Content: JSON array containing currency data.

### 2. Get Currency Data by Code
#### Endpoint
`GET /api/v1/currencies/select_one`

#### Description
Retrieve financial data for a specific currency code.

#### Request
- Method: GET
- Query Parameters:
  - `currency_code` (optional): Currency code (default: "eur_pln").

#### Response
- Status Code: 200 OK
- Content: JSON object containing financial data for the specified currency code.

### 3. Get Financial Data for Multiple Currencies
#### Endpoint
`GET /api/v1/currencies/select_many`

#### Description
Retrieve financial data for multiple currency codes.

#### Request
- Method: GET
- Query Parameters:
  - `selected_columns` (required): List of currency codes to retrieve data for.

#### Response
- Status Code: 200 OK
- Content: JSON array containing financial data for the specified currency codes.

### 4. Save Financial Data for Multiple Currencies to CSV
#### Endpoint
`GET /api/v1/currencies/select_many/save_to_csv`

#### Description
Retrieve financial data for multiple currency codes and save it to a CSV file.

#### Request
- Method: GET
- Query Parameters:
  - `selected_columns` (required): List of currency codes to retrieve data for.

#### Response
- Status Code: 200 OK
- Content: JSON object with a success message indicating that the CSV file has been saved.

### 5. Get Average Currency Rate
#### Endpoint
`GET /api/v1/currencies/{currency_code}/average`

#### Description
Retrieve the average rate for a specific currency.

#### Request
- Method: GET
- Path Parameters:
  - `currency_code` (optional): Currency code (default: "eur_pln").

#### Response
- Status Code: 200 OK
- Content: JSON object containing the average rate for the specified currency.

### 6. Get Maximum Currency Rate
#### Endpoint
`GET /api/v1/currencies/{currency_code}/maximum`

#### Description
Retrieve the maximum rate for a specific currency.

#### Request
- Method: GET
- Path Parameters:
  - `currency_code` (optional): Currency code (default: "eur_pln").

#### Response
- Status Code: 200 OK
- Content: JSON object containing the maximum rate for the specified currency.

### 7. Get Minimum Currency Rate
#### Endpoint
`GET /api/v1/currencies/{currency_code}/minimum`

#### Description
Retrieve the minimum rate for a specific currency.

#### Request
- Method: GET
- Path Parameters:
  - `currency_code` (optional): Currency code (default: "eur_pln").

#### Response
- Status Code: 200 OK
- Content: JSON object containing the minimum rate for the specified currency.

### 8. Get Currency Rate in Date Range
#### Endpoint
`GET /api/v1/currencies/{currency_code}/date-range`

#### Description
Retrieve financial data for a specific currency within a specified date range.

#### Request
- Method: GET
- Path Parameters:
  - `currency_code` (optional): Currency code (default: "eur_pln").
- Query Parameters:
  - `start_date` (required): Start date of the date range.
  - `end_date` (required): End date of the date range.

#### Response
- Status Code: 200 OK
- Content: JSON array containing financial data for the specified currency within the specified date range.

### Error Handling
The API may return the following error responses:

- 404 Not Found: Data not found.
- 422 Unprocessable Entity: Invalid input or missing required parameters.

### Notes
- The date format for `start_date` and `end_date` should be in the format "YYYY-MM-DD".
- Currency codes should be valid and adhere to the `CurrencyCodeEnum` enumeration.

### Examples
#### Example: Get All Currencies
```http
GET /api/v1/currencies
```

#### Example: Get Currency Data by Code
```http
GET /api/v1/currencies/select_one?currency_code=usd_eur
```

#### Example: Get Financial Data for Multiple Currencies
```http
GET /api/v1/currencies/select_many?selected_columns=usd_eur,gbp_usd
```

#### Example: Save Financial Data for Multiple Currencies to CSV
```http
GET /api/v1/currencies/select_many/save_to_csv?selected_columns=usd_eur,gbp_usd
```

#### Example: Get Average Currency Rate
```http
GET /api/v1/currencies/usd_eur/average
```

#### Example: Get Maximum Currency Rate
```http
GET /api/v1/currencies/usd_eur/maximum
```

#### Example: Get Minimum Currency Rate
```http
GET /api/v1/currencies/usd_eur/minimum
```

#### Example: Get Currency Rate in Date Range
```http
GET /api/v1/currencies/usd_eur/date-range?start_date=2023-01-01&end_date=2023-12-31
```

### Conclusion
This API documentation provides comprehensive information on the available endpoints, request parameters, and expected responses. Users can leverage these endpoints to retrieve various financial data related to currencies.
