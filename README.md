<img src="imagens/slogan.jpg" alt="imagens" width="300"/>

[![Test Actions](https://github.com/Jeferson100/Data-Brasil/actions/workflows/teste.yml/badge.svg)](https://github.com/Jeferson100/Data-Brasil/actions/workflows/test.yml)
[![Collect Data](https://github.com/Jeferson100/Data-Brasil/actions/workflows/dados.yml/badge.svg)](https://github.com/Jeferson100/Data-Brasil/actions/workflows/datas.yml)

# Brazilian Data

This repository is part of the development of a Python package designed for collecting data from Brazilian sources. It retrieves data from institutions such as the `Banco Central do Brasil`, `IBGE`, `IPEA`, and `FRED`.

## Table of Contents

- [Installation](#installation)
- [How to import](#how-to-import)
- [EconomicData Class Documentation](#economicdata-class-documentation)
- [Brazilian_Data Usage](#brazilian_data-usage)
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

## Brazilian_Data Usage

### Initialization of the class

- **Parameters:** start_date

**The variable start_date defines the initial date for data collection.**

Example:
```python
start_date = "2020-01-01"
```

- **Parameters:** codes_banco_central

**The `codes_banco_central` should be a dictionary with the column name that the `datas_banco_central` function will recognize as the column name and the series code.**

Example:
```python
bcb_codes = {
    "selic": 4189,
    "cambio": 3698,
    "pib_mensal": 4380,
    "igp_m": 189,
    "igp_di": 190,
    "m1": 27788,
}
```

- **Parameters:** codes_ibge

The `codes_ibge` input should be a dictionary where each key represents the name of a variable (e.g., "ipca"), which the function will use as the column name. The value associated with each key should be another dictionary containing the following fields:

- `"codigo"`: An integer representing the code of the data series to be collected. This code is specific to the variable and identifies the series in the IBGE database.

- `"territorial_level"`: A string indicating the territorial level of the data, such as "1" for Brazil, "2" for regions, "3" for states, etc.

- `"ibge_territorial_code"`: A code defining the specific geographical area of the data. The value `"all"` indicates that data for all areas corresponding to the territorial level should be collected.

- `"variable"`: A string or number that identifies the specific variable within the data series. This may represent a specific category or indicator to be collected.

Example:

```python
variaveis_ibge = {
    "ipca": {
        "codigo": 1737,
        "territorial_level": "1",
        "ibge_territorial_code": "all",
        "variable": "63",
    }
}
```

- **Parameters:** codes_ibge_link

The `codes_ibge_link` input should be a dictionary where each key represents the name of an economic indicator or specific variable (e.g., "pib", "soja"), which the function will use as the column name. The value associated with each key is a URL that points to an Excel file available on the IBGE website, containing the data corresponding to that indicator.

These URLs are dynamically generated from the IBGE SIDRA system and can be used to download the tables directly. Each link contains specific parameters defining the selection of variables, periods, and territorial levels relevant to the query.

Example:

```python
    indicadores_ibge_link = {
    "capital_fixo": "https://sidra.ibge.gov.br/geratabela?format=xlsx&name=tabela5932.xlsx&terr=N&rank=-&query=t/5932/n1/all/v/6561/p/all/c11255/93406/d/v6561%201/l/v,p%2Bc11255,t",

    "soja": "https://sidra.ibge.gov.br/geratabela?format=xlsx&name=tabela6588.xlsx&terr=N&rank=-&query=t/6588/n1/all/v/35/p/all/c48/0,39443/l/v,p%2Bc48,t",}
```

These URLs allow for the direct download of the data in Excel format, which can then be processed by your code.

- **Parameters:** codes_ipeadata

**The `codes_ipeadata` should be a dictionary with the column name that the `datas_ipeadata` function will recognize as the column name and the series code.**

```python
codigos_ipeadata= {
    "taja_juros_ltn": "ANBIMA12_TJTLN1212",
    "imposto_renda": "SRF12_IR12",
    "ibovespa": "ANBIMA12_IBVSP12",
    "consumo_energia": "ELETRO12_CEET12",
    "brent_fob": "EIA366_PBRENT366",}
```

- **Parameters:** codes_fred

The `codes fred` should be a dictionary with the column name that the `datas_fred` function will recognize as the column name and the series code.

```python
codigos_fred = {
    "nasdaq100": "NASDAQ100",
    "taxa_cambio_efetiva": "RBBRBIS",
    "cboe_nasdaq": "VXNCLS",
    "taxa_juros_interbancaria": "IRSTCI01BRM156N",
    "atividade_economica_eua": "USPHCI",}
```	

### Method `datas_brazil`

- 1. **Define the variables:** 

```python
DATA_INICIO = "2000-01-01"
data_bcb = True
data_ibge = True
data_ibge_link = True
data_ipeadata = True
data_fred = False
```

- 2. **Create the object.**

```python
economic_brazil = EconomicData(codes_banco_central=variaveis_banco_central, 
                                 codes_ibge=variaveis_ibge, 
                                 codes_ipeadata=codigos_ipeadata, 
                                 codes_ibge_link=indicadores_ibge_link,
                                 start_date=DATA_INICIO)
```	
3. **Collect the data.**

```python	
dados = economic_brazil.datas_brazil(datas_bcb= data_bcb,
                                     datas_ibge_codigos=data_ibge, 
                                     datas_ibge_link=data_ibge_link, 
                                     datas_ipeadata=data_ipeadata,
                                     missing_data=True)
```
Returns a dataframe with the data collected.

```python
dados.head()
```
<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>selic</th>
      <th>cambio</th>
      <th>pib_mensal</th>
      <th>igp_m</th>
      <th>igp_di</th>
      <th>m1</th>
      <th>ipca</th>
      <th>custo_m2</th>
      <th>pesquisa_industrial_mensal</th>
      <th>pib</th>
      <th>...</th>
      <th>capital_fixo</th>
      <th>producao_industrial_manufatureira</th>
      <th>soja</th>
      <th>milho_1</th>
      <th>milho_2</th>
      <th>taja_juros_ltn</th>
      <th>imposto_renda</th>
      <th>ibovespa</th>
      <th>consumo_energia</th>
      <th>brent_fob</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2000-01-01</th>
      <td>18.94</td>
      <td>1.8037</td>
      <td>92576.6</td>
      <td>1.24</td>
      <td>1.02</td>
      <td>79015372.0</td>
      <td>0.62</td>
      <td>5.51</td>
      <td>69.71441</td>
      <td>1.4</td>
      <td>...</td>
      <td>-5.0</td>
      <td>57.43586</td>
      <td>52381672.0</td>
      <td>31477232.0</td>
      <td>10595844.0</td>
      <td>19.465261</td>
      <td>5043.680936</td>
      <td>-4.113276</td>
      <td>25060.0</td>
      <td>25.511000</td>
    </tr>
    <tr>
      <th>2000-02-01</th>
      <td>18.87</td>
      <td>1.7753</td>
      <td>91770.4</td>
      <td>0.35</td>
      <td>0.19</td>
      <td>79015372.0</td>
      <td>0.13</td>
      <td>5.51</td>
      <td>69.71441</td>
      <td>1.4</td>
      <td>...</td>
      <td>-5.0</td>
      <td>57.43586</td>
      <td>52381672.0</td>
      <td>31477232.0</td>
      <td>10595844.0</td>
      <td>19.465261</td>
      <td>4120.602582</td>
      <td>7.761777</td>
      <td>25057.0</td>
      <td>27.775714</td>
    </tr>
    <tr>
      <th>2000-03-01</th>
      <td>18.85</td>
      <td>1.7420</td>
      <td>92579.9</td>
      <td>0.15</td>
      <td>0.18</td>
      <td>79015372.0</td>
      <td>0.22</td>
      <td>5.51</td>
      <td>69.71441</td>
      <td>1.1</td>
      <td>...</td>
      <td>-0.3</td>
      <td>57.43586</td>
      <td>52381672.0</td>
      <td>31477232.0</td>
      <td>10595844.0</td>
      <td>19.465261</td>
      <td>5606.185192</td>
      <td>0.906002</td>
      <td>25662.0</td>
      <td>27.486087</td>
    </tr>
    <tr>
      <th>2000-04-01</th>
      <td>18.62</td>
      <td>1.7682</td>
      <td>91376.2</td>
      <td>0.23</td>
      <td>0.13</td>
      <td>79015372.0</td>
      <td>0.42</td>
      <td>5.51</td>
      <td>69.71441</td>
      <td>1.1</td>
      <td>...</td>
      <td>-0.3</td>
      <td>57.43586</td>
      <td>52381672.0</td>
      <td>31477232.0</td>
      <td>10595844.0</td>
      <td>19.465261</td>
      <td>4634.431697</td>
      <td>-12.811448</td>
      <td>25598.0</td>
      <td>22.764444</td>
    </tr>
    <tr>
      <th>2000-05-01</th>
      <td>18.51</td>
      <td>1.8279</td>
      <td>98727.0</td>
      <td>0.31</td>
      <td>0.67</td>
      <td>79015372.0</td>
      <td>0.01</td>
      <td>5.51</td>
      <td>69.71441</td>
      <td>1.1</td>
      <td>...</td>
      <td>-0.3</td>
      <td>57.43586</td>
      <td>52381672.0</td>
      <td>31477232.0</td>
      <td>10595844.0</td>
      <td>21.681500</td>
      <td>4047.302075</td>
      <td>-3.739461</td>
      <td>25448.0</td>
      <td>27.737619</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 21 columns</p>
</div>

The `missing_data` parameter indicates whether missing values will be replaced using the `ffill` and `bfill` methods. By default, `missing_data` will be True, and missing values will be replaced. If you prefer to keep the missing data, set the `missing_data` parameter to `False`.

```python
data_bcb = True
data_ibge = True
data_ibge_link = True
data_ipeadata = True
data_fred = False

economic_brazil = EconomicData(codes_banco_central=variaveis_banco_central, 
                                 codes_ibge=variaveis_ibge, 
                                 codes_ipeadata=codigos_ipeadata, 
                                 codes_ibge_link=indicadores_ibge_link,
                                 start_date=DATA_INICIO)

dados = economic_brazil.datas_brazil(datas_bcb= data_bcb,
                                     datas_ibge_codigos=data_ibge, 
                                     datas_ibge_link=data_ibge_link, 
                                     datas_ipeadata=data_ipeadata,
                                     missing_data=False)
dados.head()
```
<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>cambio</th>
      <th>pib_mensal</th>
      <th>igp_m</th>
      <th>m1</th>
      <th>ipca</th>
      <th>custo_m2</th>
      <th>pesquisa_industrial_mensal</th>
      <th>pib</th>
      <th>despesas_publica</th>
      <th>capital_fixo</th>
      <th>producao_industrial_manufatureira</th>
      <th>soja</th>
      <th>milho_1</th>
      <th>milho_2</th>
      <th>taja_juros_ltn</th>
      <th>imposto_renda</th>
      <th>ibovespa</th>
      <th>consumo_energia</th>
      <th>brent_fob</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2000-01-01</th>
      <td>1.8037</td>
      <td>92576.6</td>
      <td>1.24</td>
      <td>NaN</td>
      <td>0.62</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.4</td>
      <td>3.9</td>
      <td>-5.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>5043.680936</td>
      <td>-4.113276</td>
      <td>25060.0</td>
      <td>25.511000</td>
    </tr>
    <tr>
      <th>2000-02-01</th>
      <td>1.7753</td>
      <td>91770.4</td>
      <td>0.35</td>
      <td>NaN</td>
      <td>0.13</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.4</td>
      <td>3.9</td>
      <td>-5.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>4120.602582</td>
      <td>7.761777</td>
      <td>25057.0</td>
      <td>27.775714</td>
    </tr>
    <tr>
      <th>2000-03-01</th>
      <td>1.7420</td>
      <td>92579.9</td>
      <td>0.15</td>
      <td>NaN</td>
      <td>0.22</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.1</td>
      <td>3.6</td>
      <td>-0.3</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>5606.185192</td>
      <td>0.906002</td>
      <td>25662.0</td>
      <td>27.486087</td>
    </tr>
    <tr>
      <th>2000-04-01</th>
      <td>1.7682</td>
      <td>91376.2</td>
      <td>0.23</td>
      <td>NaN</td>
      <td>0.42</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.1</td>
      <td>3.6</td>
      <td>-0.3</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>19.465261</td>
      <td>4634.431697</td>
      <td>-12.811448</td>
      <td>25598.0</td>
      <td>22.764444</td>
    </tr>
    <tr>
      <th>2000-05-01</th>
      <td>1.8279</td>
      <td>98727.0</td>
      <td>0.31</td>
      <td>NaN</td>
      <td>0.01</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.1</td>
      <td>3.6</td>
      <td>-0.3</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>21.681500</td>
      <td>4047.302075</td>
      <td>-3.739461</td>
      <td>25448.0</td>
      <td>27.737619</td>
    </tr>
  </tbody>
</table>
</div>






## Contributing

All contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome. 

## License

[MIT License](LICENSE)
