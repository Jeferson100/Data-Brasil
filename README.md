<img src="imagens/slogan.jpg" alt="imagens" width="300"/>


# Brazilian Data

This repository is part of the development of a Python package designed for collecting data from Brazilian sources. It retrieves data from institutions such as the `Banco Central do Brasil`, `IBGE`, `IPEA`, and `FRED`.

## Table of Contents

- [Installation](#installation)
- [How to import](#how-to-import)
- [EconomicData Class Documentation](#economicdata-class-documentation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)


## Installation

To install the package, execute the following command:
```	
pip install brazilian_data
```
## How to import

```python
from brazilian_data import EconomicData
```

# EconomicData Class Documentation

## Overview
The `EconomicData` class is designed to facilitate the fetching, processing, and saving of economic data from various sources such as Banco Central, IBGE, IPEADATA, and FRED.

## Initialization
### `__init__(self, codes_banco_central=None, codes_ibge=None, codes_ibge_link=None, codes_ipeadata=None, codes_fred=None, start_date=None)`
Initializes the `EconomicData` class with optional parameters for data codes and start date.

- **Parameters:**
  - `codes_banco_central` (dict): Dictionary of Banco Central codes.
  - `codes_ibge` (dict): Dictionary of IBGE codes.
  - `codes_ibge_link` (dict): Dictionary of IBGE links.
  - `codes_ipeadata` (dict): Dictionary of IPEADATA codes.
  - `codes_fred` (dict): Dictionary of FRED codes.
  - `start_date` (str): Start date for data fetching.

## Methods

### `fetch_data_for_code(self, link, column)`
Fetches data from an IBGE link for a specific column.

- **Parameters:**
  - `link` (str): URL link to fetch data from.
  - `column` (str): Column name to fetch data for.
- **Returns:** Data fetched from the specified link and column.

### `data_index(self)`
Generates a DataFrame with a date range starting from `start_date`.

- **Returns:** DataFrame with a date range as the index.

### `datas_banco_central(self, save=None, diretory=None, data_format=None)`
Fetches data from Banco Central and handles exceptions.

- **Parameters:**
  - `save` (bool): Whether to save the data.
  - `diretory` (str): Directory where the data will be saved.
  - `data_format` (str): Format to save the data ('csv', 'excel', 'json', 'pickle').
- **Returns:** DataFrame with Banco Central data if not saving.

### `datas_ibge(self, save=False, diretory=None, data_format=None)`
Fetches IBGE data and handles exceptions.

- **Parameters:**
  - `save` (bool): Whether to save the data.
  - `diretory` (str): Directory where the data will be saved.
  - `data_format` (str): Format to save the data ('csv', 'excel', 'json', 'pickle').
- **Returns:** DataFrame with IBGE data if not saving.

### `datas_ibge_link(self, save=None, diretory=None, data_format=None)`
Fetches data from IBGE links and handles exceptions.

- **Parameters:**
  - `save` (bool): Whether to save the data.
  - `diretory` (str): Directory where the data will be saved.
  - `data_format` (str): Format to save the data ('csv', 'excel', 'json', 'pickle').
- **Returns:** DataFrame with IBGE link data if not saving.

### `datas_ipeadata(self, salve=None, diretory=None, data_format=None)`
Fetches IPEADATA data and handles exceptions.

- **Parameters:**
  - `salve` (bool): Whether to save the data.
  - `diretory` (str): Directory where the data will be saved.
  - `data_format` (str): Format to save the data ('csv', 'excel', 'json', 'pickle').
- **Returns:** DataFrame with IPEADATA data if not saving.

### `datas_fred(self, save=None, diretory=None, data_format=None)`
Fetches data from FRED and handles exceptions.

- **Parameters:**
  - `save` (bool): Whether to save the data.
  - `diretory` (str): Directory where the data will be saved.
  - `data_format` (str): Format to save the data ('csv', 'excel', 'json', 'pickle').
- **Returns:** DataFrame with FRED data if not saving.

### `datas_brazil(self, datas_bcb=True, datas_ibge_codigos=True, datas_ibge_link=True, datas_ipeadata=True, datas_fred=False, missing_data=True, fill_method=None, save=None, directory=None, data_format=None)`
Fetches all data based on specified options.

- **Parameters:**
  - `datas_bcb` (bool): Whether to fetch Banco Central data.
  - `datas_ibge_codigos` (bool): Whether to fetch IBGE data by codes.
  - `datas_ibge_link` (bool): Whether to fetch IBGE data by links.
  - `datas_ipeadata` (bool): Whether to fetch IPEADATA data.
  - `datas_fred` (bool): Whether to fetch FRED data.
  - `missing_data` (bool): Whether to handle missing data.
  - `fill_method` (str): Method to handle missing data ('ffill' or 'bfill').
  - `save` (bool): Whether to save the data.
  - `directory` (str): Directory where the data will be saved.
  - `data_format` (str): Format to save the data ('csv', 'excel', 'json', 'pickle').
- **Returns:** DataFrame with all requested data if not saving.

### `save_datas(self, dados, diretory=None, data_format="csv")`
Saves the data to the specified directory and format.

- **Parameters:**
  - `dados` (DataFrame): DataFrame to be saved.
  - `diretory` (str): Directory where the data will be saved.
  - `data_format` (str): Format to save the data ('csv', 'excel', 'json', 'pickle').

### `help(self)`
Prints out information about the available methods and their usage.

- **Usage:** `instance.help()`

## Usage

### Definition of the codes for search



## Contributing

All contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome. 

## License

[MIT License](LICENSE)
