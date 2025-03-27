
<img src="https://raw.githubusercontent.com/Jeferson100/Data-Brasil/main/imagens/logo_bandeira_verde.png" alt="Logo Data Brasil" width="600" height="500" />

[![Test Actions Python](https://github.com/Jeferson100/Data-Brasil/actions/workflows/test_python.yml/badge.svg)](https://github.com/Jeferson100/Data-Brasil/actions/workflows/test_python.yml)
[![Collect Data](https://github.com/Jeferson100/Data-Brasil/actions/workflows/datas.yml/badge.svg)](https://github.com/Jeferson100/Data-Brasil/actions/workflows/datas.yml)
[![PyPI version](https://badge.fury.io/py/brazilian-data.svg)](https://badge.fury.io/py/brazilian-data)
[![](https://github.com/Jeferson100/Data-Brasil/actions/workflows/test.yml/badge.svg)](https://github.com/Jeferson100/Data-Brasil/actions/workflows/test.yml)
[![GitHub](https://img.shields.io/github/license/Jeferson100/Data-Brasil)](https://github.com/Jeferson100/Data-Brasil/blob/main/LICENSE)
[![GitHub Logo](https://img.shields.io/github/last-commit/Jeferson100/Data-Brasil?style=)](https://github.com/Jeferson100/Data-Brasil)
[![GitHub](https://img.shields.io/github/repo-size/Jeferson100/Data-Brasil?style=flat-square)](https://github.com/Jeferson100/Data-Brasil)
![Downloads](https://img.shields.io/pypi/dm/brazilian-data)


## Links do projeto

[![GitHub Logo](https://img.shields.io/badge/GitHub-black?style=flat&logo=github)](https://github.com/Jeferson100/Data-Brasil)


## GitHub Statistics

[![GitHub](https://img.shields.io/github/stars/Jeferson100/Data-Brasil?style=social)](https://github.com/Jeferson100/Data-Brasil)
[![Forks](https://img.shields.io/github/forks/Jeferson100/Data-Brasil)](https://github.com/Jeferson100/Data-Brasil/network)
[![Issues](https://img.shields.io/github/issues/Jeferson100/Data-Brasil)](https://github.com/Jeferson100/Data-Brasil/issues)
[![Pull Requests](https://img.shields.io/github/issues-pr/Jeferson100/Data-Brasil)](https://github.com/Jeferson100/Data-Brasil)



# Brazilian Data

This repository is part of the development of a Python package designed for collecting data from Brazilian sources. It retrieves data from institutions such as the `Banco Central do Brasil`, `IBGE`, `IPEA`, and `FRED`.
To search for series from the sources, use the following websites.

- [Banco Central](https://www3.bcb.gov.br/sgspub/localizarseries/localizarSeries.do?method=prepararTelaLocalizarSeries)
- [IBGE](https://sidra.ibge.gov.br/home/ipca/brasil)
- [IPEA](http://www.ipeadata.gov.br/Default.aspx)
- [FRED](https://fred.stlouisfed.org/)


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
pip install brazilian-data
```
## How to import

```python
from brazilian_data import EconomicData
```

# EconomicData Class Documentation (Version sync)

## Overview
The `EconomicData` class is designed to facilitate the fetching, processing, and saving of economic data from various sources such as Banco Central, IBGE, IPEADATA, and FRED.For examples, see [economic_data_examples.ipynb](https://github.com/Jeferson100/Data-Brasil/blob/main/examples/economic_data_examples.ipynb).

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

For collecting data from different sources, you can use the `datas_brazil` method:

```python
## Import the `EconomicData` class
from brazilian_data import EconomicData

## Define parameters that will be used in the `datas_brazil` method
DATA_INICIO = "2000-01-01"

data_bcb = True
data_ibge = True
data_ibge_link = True
data_ipeadata = True
data_fred = False

## Initialize the `EconomicData` class
economic_brazil = EconomicData(codes_banco_central=variaveis_banco_central, 
                                 codes_ibge=variaveis_ibge, 
                                 codes_ipeadata=codigos_ipeadata, 
                                 codes_ibge_link=indicadores_ibge_link,
                                 start_date=DATA_INICIO)

## Call the `datas_brazil` method
dados = economic_brazil.datas_brazil(datas_bcb= data_bcb,
                                     datas_ibge_codigos=data_ibge, 
                                     datas_ibge_link=data_ibge_link, 
                                     datas_ipeadata=data_ipeadata,
                                     missing_data=True)
```
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

## Import the `EconomicData` class
from brazilian_data import EconomicData

## Define parameters that will be used in the `datas_brazil` method
data_bcb = True
data_ibge = True
data_ibge_link = True
data_ipeadata = True
data_fred = False

## Initialize the `EconomicData` class
economic_brazil = EconomicData(codes_banco_central=variaveis_banco_central, 
                                 codes_ibge=variaveis_ibge, 
                                 codes_ipeadata=codigos_ipeadata, 
                                 codes_ibge_link=indicadores_ibge_link,
                                 start_date=DATA_INICIO)

## Call the `datas_brazil` method
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

With the parameter `save=True`, you can download data. Define the `directory` parameter to save the file. If you don't define the `directory` parameter, an error will be returned. You can save in four formats: `csv`, `json`, `pickle`, and `excel`.

```python
## Import the `EconomicData` class
from brazilian_data import EconomicData

## Define parameters that will be used in the `datas_brazil` method
data_bcb = True
data_ibge = True
data_ibge_link = True
data_ipeadata = True
data_fred = False

## Initialize the `EconomicData` class
economic_brazil = EconomicData(codes_banco_central=variaveis_banco_central, 
                                 codes_ibge=variaveis_ibge, 
                                 codes_ipeadata=codigos_ipeadata, 
                                 codes_ibge_link=indicadores_ibge_link,
                                 start_date=DATA_INICIO)

## Call the `datas_brazil` method
dados = economic_brazil.datas_brazil(datas_bcb= data_bcb,
                                     datas_ibge_codigos=data_ibge, 
                                     datas_ibge_link=data_ibge_link, 
                                     datas_ipeadata=data_ipeadata,
                                     save=True,
                                     directory="../dados/economicos_brazil",
                                     data_format="csv")
```
This parameter will not return a dataframe, only the saved file. This parameter can be used for other methods in the class.

### Method `datas_banco_central`

If you want to download the data from the Banco Central, you can use the method `datas_banco_central`.

```python
## Imported library
from brazilian_data import EconomicData

## define the start date
DATA_INICIO = "2000-01-01"

## define the dictionary of codes
variaveis_banco_central= {
    "selic": 4189,
    "cambio": 3698,
    "pib_mensal": 4380,
    "igp_m": 189,
    "igp_di": 190,
    "m1": 27788,
}

## define a new object
economic_brazil = EconomicData(codes_banco_central=variaveis_banco_central, 
                                start_date=DATA_INICIO)

## download the data
dados = economic_brazil.datas_banco_central()
```	
```python
dados.head()
```
<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>selic</th>
      <th>pib_mensal</th>
      <th>igp_m</th>
      <th>igp_di</th>
      <th>m1</th>
    </tr>
    <tr>
      <th>Date</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2000-01-01</th>
      <td>18.94</td>
      <td>92576.6</td>
      <td>1.24</td>
      <td>1.02</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2000-02-01</th>
      <td>18.87</td>
      <td>91770.4</td>
      <td>0.35</td>
      <td>0.19</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2000-03-01</th>
      <td>18.85</td>
      <td>92579.9</td>
      <td>0.15</td>
      <td>0.18</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2000-04-01</th>
      <td>18.62</td>
      <td>91376.2</td>
      <td>0.23</td>
      <td>0.13</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2000-05-01</th>
      <td>18.51</td>
      <td>98727.0</td>
      <td>0.31</td>
      <td>0.67</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>

### Method `datas_ibge`

If you want to download the data from the IBGE, you can use the method `datas_ibge`.

```python
## Imported library
from brazilian_data import EconomicData

## define the start date
DATA_INICIO = "2010-01-01"

## define the dictionary of codes
variaveis_ibge = {
    "ipca": {
        "codigo": 1737,
        "territorial_level": "1",
        "ibge_territorial_code": "all",
        "variable": "63",
    },
    "custo_m2": {
        "codigo": 2296,
        "territorial_level": "1",
        "ibge_territorial_code": "all",
        "variable": "1198",
    },
    "pesquisa_industrial_mensal": {
        "codigo": 8159,
        "territorial_level": "1",
        "ibge_territorial_code": "all",
        "variable": "11599",
    },
    "pmc_volume": {
        "codigo": 8186,
        "territorial_level": "1",
        "ibge_territorial_code": "all",
        "variable": "11709",
    },
}

## define a new object
economic_brazil = EconomicData(codes_ibge=variaveis_ibge, start_date=DATA_INICIO)

## download the data
dados = economic_brazil.datas_ibge()
```

```python
dados.head()
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>ipca</th>
      <th>custo_m2</th>
      <th>pesquisa_industrial_mensal</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2010-01-01</th>
      <td>0.75</td>
      <td>NaN</td>
      <td>91.20876</td>
    </tr>
    <tr>
      <th>2010-02-01</th>
      <td>0.78</td>
      <td>NaN</td>
      <td>88.95149</td>
    </tr>
    <tr>
      <th>2010-03-01</th>
      <td>0.52</td>
      <td>NaN</td>
      <td>105.07767</td>
    </tr>
    <tr>
      <th>2010-04-01</th>
      <td>0.57</td>
      <td>NaN</td>
      <td>99.30561</td>
    </tr>
    <tr>
      <th>2010-05-01</th>
      <td>0.43</td>
      <td>NaN</td>
      <td>104.27978</td>
    </tr>
  </tbody>
</table>
</div>

### Method `datas_ibge_link`

Some codes in `codes_ibge` do not work, resulting in errors and no files being returned. To address this, `codes_ibge_link` was created, where you obtain the link to the file from the [IBGE](https://sidra.ibge.gov.br/home/pms/brasil). A example of how to get the link is shown [here](https://github.com/Jeferson100/Data-Brasil/blob/main/imagens/example_link.md).

```python
## Imported library
from brazilian_data import EconomicData

## define the start date
DATA_INICIO = "2010-01-01"

## define the dictionary of codes
indicadores_ibge_link = {
    "capital_fixo": "https://sidra.ibge.gov.br/geratabela?format=xlsx&name=tabela5932.xlsx&terr=N&rank=-&query=t/5932/n1/all/v/6561/p/all/c11255/93406/d/v6561%201/l/v,p%2Bc11255,t",
    "producao_industrial_manufatureira": "https://sidra.ibge.gov.br/geratabela?format=xlsx&name=tabela8158.xlsx&terr=N&rank=-&query=t/8158/n1/all/v/11599/p/all/c543/129278/d/v11599%205/l/v,p%2Bc543,t",
    "soja": "https://sidra.ibge.gov.br/geratabela?format=xlsx&name=tabela6588.xlsx&terr=N&rank=-&query=t/6588/n1/all/v/35/p/all/c48/0,39443/l/v,p%2Bc48,t",
    "milho_1": "https://sidra.ibge.gov.br/geratabela?format=xlsx&name=tabela6588.xlsx&terr=N&rank=-&query=t/6588/n1/all/v/35/p/all/c48/0,39441/l/v,p%2Bc48,t",
    "milho_2": "https://sidra.ibge.gov.br/geratabela?format=xlsx&name=tabela6588.xlsx&terr=N&rank=-&query=t/6588/n1/all/v/35/p/all/c48/0,39442/l/v,p%2Bc48,t",
}

## define a new object
economic_brazil = EconomicData(codes_ibge_link=indicadores_ibge_link, 
                     start_date=DATA_INICIO)

## download the data
dados = economic_brazil.datas_ibge_link()
```
```python
dados.head()
```
<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>capital_fixo</th>
      <th>producao_industrial_manufatureira</th>
      <th>soja</th>
      <th>milho_1</th>
      <th>milho_2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2010-01-01</th>
      <td>12.9</td>
      <td>89.55269</td>
      <td>66137344.0</td>
      <td>33424815.0</td>
      <td>17996575.0</td>
    </tr>
    <tr>
      <th>2010-02-01</th>
      <td>12.9</td>
      <td>91.15047</td>
      <td>66941524.0</td>
      <td>33735243.0</td>
      <td>18620733.0</td>
    </tr>
    <tr>
      <th>2010-03-01</th>
      <td>29.0</td>
      <td>114.92197</td>
      <td>67350136.0</td>
      <td>33486684.0</td>
      <td>19095737.0</td>
    </tr>
    <tr>
      <th>2010-04-01</th>
      <td>29.0</td>
      <td>104.58762</td>
      <td>67913643.0</td>
      <td>33830625.0</td>
      <td>19457468.0</td>
    </tr>
    <tr>
      <th>2010-05-01</th>
      <td>29.0</td>
      <td>110.27518</td>
      <td>68131230.0</td>
      <td>33577605.0</td>
      <td>19569483.0</td>
    </tr>
  </tbody>
</table>
</div>

### Method `datas_ipeadata()`

If you want to download data from IPEA, you can use the `datas_ipeadata()` method.

```python	
## Import the `EconomicData` class
from brazilian_data import EconomicData

## Define parameters that will be used in the `datas_brazil` method
DATA_INICIO = "2010-01-01"

codigos_ipeadata= {
    "taja_juros_ltn": "ANBIMA12_TJTLN1212",
    "imposto_renda": "SRF12_IR12",
    "ibovespa": "ANBIMA12_IBVSP12",
    "consumo_energia": "ELETRO12_CEET12",
    "brent_fob": "EIA366_PBRENT366",
}

## define a new object
economic_brazil = EconomicData(codes_ipeadata=codigos_ipeadata, 
                                start_date=DATA_INICIO)

## download the data
dados = economic_brazil.datas_ipeadata()
```
```python
dados.head()
```
<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>taja_juros_ltn</th>
      <th>imposto_renda</th>
      <th>ibovespa</th>
      <th>consumo_energia</th>
      <th>brent_fob</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2010-01-01</th>
      <td>10.454116</td>
      <td>22598.711556</td>
      <td>-4.65</td>
      <td>33360.0</td>
      <td>76.600323</td>
    </tr>
    <tr>
      <th>2010-02-01</th>
      <td>10.525189</td>
      <td>11801.791225</td>
      <td>1.68</td>
      <td>33730.0</td>
      <td>73.642143</td>
    </tr>
    <tr>
      <th>2010-03-01</th>
      <td>10.822181</td>
      <td>15204.637209</td>
      <td>5.82</td>
      <td>35117.0</td>
      <td>78.636452</td>
    </tr>
    <tr>
      <th>2010-04-01</th>
      <td>11.119986</td>
      <td>21267.690569</td>
      <td>-4.04</td>
      <td>35026.0</td>
      <td>84.191667</td>
    </tr>
    <tr>
      <th>2010-05-01</th>
      <td>11.696400</td>
      <td>14772.309694</td>
      <td>-6.64</td>
      <td>34297.0</td>
      <td>77.267742</td>
    </tr>
  </tbody>
</table>
</div>

### Method `datas_fred()`

If you want to download data from FRED, you can use the `datas_fred()` method. On the first use of `datas_fred()`	, a prompt will appear for setting up the FRED API key. To generate the key, follow the steps described [here](https://github.com/Jeferson100/Data-Brasil/blob/main/imagens/example_key_fred.md).

![fred](https://github.com/Jeferson100/Data-Brasil/blob/main/imagens/colocar_senha.png)

After that, you can run the code again and the data will be collected.

```python
## Import the `EconomicData` class
from brazilian_data import EconomicData

## Define parameters that will be used in the `datas_brazil` method
DATA_INICIO = "2010-01-01"

codigos_fred = {
    "nasdaq100": "NASDAQ100",
    "taxa_cambio_efetiva": "RBBRBIS",
    "cboe_nasdaq": "VXNCLS",
    "taxa_juros_interbancaria": "IRSTCI01BRM156N",
    "atividade_economica_eua": "USPHCI",}

## Initialize the `EconomicData` class
economic_brazil = EconomicData(codes_fred=codigos_fred, start_date=DATA_INICIO)

## Download the data
dados = economic_brazil.datas_fred()
```

```python
dados.head()
```
<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>nasdaq100</th>
      <th>taxa_cambio_efetiva</th>
      <th>cboe_nasdaq</th>
      <th>taxa_juros_interbancaria</th>
      <th>atividade_economica_eua</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2010-01-01</th>
      <td>NaN</td>
      <td>160.61</td>
      <td>NaN</td>
      <td>8.75</td>
      <td>97.29</td>
    </tr>
    <tr>
      <th>2010-02-01</th>
      <td>1760.72</td>
      <td>157.74</td>
      <td>24.33</td>
      <td>8.75</td>
      <td>97.37</td>
    </tr>
    <tr>
      <th>2010-03-01</th>
      <td>1846.40</td>
      <td>162.82</td>
      <td>19.59</td>
      <td>8.75</td>
      <td>97.50</td>
    </tr>
    <tr>
      <th>2010-04-01</th>
      <td>1959.56</td>
      <td>166.02</td>
      <td>18.76</td>
      <td>8.80</td>
      <td>97.73</td>
    </tr>
    <tr>
      <th>2010-05-01</th>
      <td>NaN</td>
      <td>165.54</td>
      <td>NaN</td>
      <td>9.50</td>
      <td>98.19</td>
    </tr>
  </tbody>
</table>
</div>


# EconomicDataAsync Class Documentation

## Overview
The `EconomicDataAsync` class is an asynchronous version of `EconomicData`, designed for more efficient data collection using async operations. For examples, see [economic_data_async_examples.ipynb](https://github.com/Jeferson100/Data-Brasil/blob/main/examples/economic_data_async_examples.ipynb).

## Initialization
### `__init__(self, codes_banco_central=None, codes_ibge=None, codes_ibge_link=None, codes_ipeadata=None, codes_fred=None, start_date=None)`

- **Parameters:**
  - `codes_banco_central` (dict): Central Bank codes
  - `codes_ibge` (dict): IBGE codes
  - `codes_ibge_link` (dict): IBGE links
  - `codes_ipeadata` (dict): IPEADATA codes
  - `codes_fred` (dict): FRED codes
  - `start_date` (str): Start date for collection

## Main Methods

### `async def datas_brazil_async(self, **kwargs)`
Asynchronously collects all configured data.

```python
data_bcb = True
data_ibge = True
data_ibge_link = True
data_ipeadata = True
data_fred = False

economic_brazil = EconomicDataAsync(codes_banco_central=variaveis_banco_central, 
                                 codes_ibge=variaveis_ibge, 
                                 codes_ipeadata=codigos_ipeadata, 
                                 codes_ibge_link=indicadores_ibge_link,
                                 start_date=DATA_INICIO)

dados = economic_brazil.datas_brazil_async(datas_bcb= data_bcb,
                                     datas_ibge_codigos=data_ibge, 
                                     datas_ibge_link=data_ibge_link, 
                                     datas_ipeadata=data_ipeadata,
                                     missing_data=True)
```

### `async def datas_banco_central_async(self, save=False, directory=None, data_format="csv")`
Asynchronously collects data from the Central Bank.

```python
DATA_INICIO = "2000-01-01"
variaveis_banco_central= {
    "selic": 4189,
    "cambio": 3698,
    "pib_mensal": 4380,
    "igp_m": 189,
    "igp_di": 190,
    "m1": 27788,
}

economic_brazil = EconomicDataAsync(codes_banco_central=variaveis_banco_central, 
                                start_date=DATA_INICIO)

dados = economic_brazil.datas_banco_central_async()
```

### `async def datas_ibge_async(self, save=False, directory=None, data_format="csv")`
Asynchronously collects data from IBGE.

```python
variaveis_ibge = {
    "ipca": {
        "codigo": 1737,
        "territorial_level": "1",
        "ibge_territorial_code": "all",
        "variable": "63",
    },
    "custo_m2": {
        "codigo": 2296,
        "territorial_level": "1",
        "ibge_territorial_code": "all",
        "variable": "1198",
    },
    "pesquisa_industrial_mensal": {
        "codigo": 8159,
        "territorial_level": "1",
        "ibge_territorial_code": "all",
        "variable": "11599",
    },
    "pmc_volume": {
        "codigo": 8186,
        "territorial_level": "1",
        "ibge_territorial_code": "all",
        "variable": "11709",
    },
}

economic_brazil = EconomicDataAsync(codes_ibge=variaveis_ibge, 
                                start_date=DATA_INICIO)

dados = economic_brazil.datas_ibge_async()
```

### `async def datas_ibge_link_async(self, save=False, directory=None, data_format="csv")`
Asynchronously collects data from IBGE via links.

```python
DATA_INICIO = "2010-01-01"

indicadores_ibge_link = {
    "capital_fixo": "https://sidra.ibge.gov.br/geratabela?format=xlsx&name=tabela5932.xlsx&terr=N&rank=-&query=t/5932/n1/all/v/6561/p/all/c11255/93406/d/v6561%201/l/v,p%2Bc11255,t",
    "producao_industrial_manufatureira": "https://sidra.ibge.gov.br/geratabela?format=xlsx&name=tabela8158.xlsx&terr=N&rank=-&query=t/8158/n1/all/v/11599/p/all/c543/129278/d/v11599%205/l/v,p%2Bc543,t",
    "soja": "https://sidra.ibge.gov.br/geratabela?format=xlsx&name=tabela6588.xlsx&terr=N&rank=-&query=t/6588/n1/all/v/35/p/all/c48/0,39443/l/v,p%2Bc48,t",
    "milho_1": "https://sidra.ibge.gov.br/geratabela?format=xlsx&name=tabela6588.xlsx&terr=N&rank=-&query=t/6588/n1/all/v/35/p/all/c48/0,39441/l/v,p%2Bc48,t",
    "milho_2": "https://sidra.ibge.gov.br/geratabela?format=xlsx&name=tabela6588.xlsx&terr=N&rank=-&query=t/6588/n1/all/v/35/p/all/c48/0,39442/l/v,p%2Bc48,t",
    "pib": "https://sidra.ibge.gov.br/geratabela?format=xlsx&name=tabela5932.xlsx&terr=N&rank=-&query=t/5932/n1/all/v/6564/p/all/c11255/90707/d/v6564%201/l/v,p,t%2Bc11255&verUFs=false&verComplementos2=false&verComplementos1=false&omitirIndentacao=false&abreviarRotulos=false&exibirNotas=false&agruparNoCabecalho=false",
}

economic_brazil = EconomicDataAsync(codes_ibge_link=indicadores_ibge_link, 
                     start_date=DATA_INICIO)

dados = economic_brazil.datas_ibge_link_async()
```

### `async def datas_ipeadata_async(self, save=False, directory=None, data_format="csv")`
Asynchronously collects data from IPEADATA.

```python
DATA_INICIO = "2010-01-01"

codigos_ipeadata= {
    "taja_juros_ltn": "ANBIMA12_TJTLN1212",
    "imposto_renda": "SRF12_IR12",
    "ibovespa": "ANBIMA12_IBVSP12",
    "consumo_energia": "ELETRO12_CEET12",
    "brent_fob": "EIA366_PBRENT366",
}


economic_brazil = EconomicDataAsync(codes_ipeadata=codigos_ipeadata, 
                                start_date=DATA_INICIO)

dados = economic_brazil.datas_ipeadata_async()
```

### `async def datas_fred_async(self, save=False, directory=None, data_format="csv")`
Asynchronously collects data from FRED.

```python
DATA_INICIO = "2010-01-01"
codigos_fred = {
    "nasdaq100": "NASDAQ100",
    "taxa_cambio_efetiva": "RBBRBIS",
    "cboe_nasdaq": "VXNCLS",
    "taxa_juros_interbancaria": "IRSTCI01BRM156N",
    "atividade_economica_eua": "USPHCI",}

economic_brazil = EconomicDataAsync(codes_fred=codigos_fred, start_date=DATA_INICIO)

dados = economic_brazil.datas_fred_async()
```



## Usage Example with Jupyter Notebook

```python
import nest_asyncio
nest_asyncio.apply()

from brazilian_data import EconomicDataAsync

data_bcb = True
data_ibge = True
data_ibge_link = True
data_ipeadata = True
data_fred = False
economic_brazil = EconomicDataAsync(codes_banco_central=variaveis_banco_central, 
                                 codes_ibge=variaveis_ibge, 
                                 codes_ipeadata=codigos_ipeadata, 
                                 codes_ibge_link=indicadores_ibge_link,
                                 start_date=DATA_INICIO)

dados = economic_brazil.datas_brazil_async(datas_bcb= data_bcb,
                                     datas_ibge_codigos=data_ibge, 
                                     datas_ibge_link=data_ibge_link, 
                                     datas_ipeadata=data_ipeadata,
                                     missing_data=True)


```

## Performance Comparison

Using the `%%timeit` magic command in Jupyter Notebook, we compared the execution time between synchronous and asynchronous methods. The results demonstrate significant performance improvements:

### Synchronous Version

```python
%%timeit
economic_brazil = EconomicData(
    codes_banco_central=central_bank_variables, 
    codes_ibge=ibge_variables, 
    codes_ipeadata=ipeadata_codes, 
    codes_ibge_link=ibge_link_indicators,
    start_date=START_DATE
)

data = economic_brazil.datas_brazil(
    datas_bcb=True,
    datas_ibge_codigos=True, 
    datas_ibge_link=True, 
    datas_ipeadata=True,
    missing_data=True
)
```
```bash
1min 18s ± 27.4s per loop (mean ± std. dev. of 7 runs, 1 loop each)
```

### Asynchronous Version
```python
%%timeit
economic_brazil = EconomicDataAsync(
    codes_banco_central=central_bank_variables, 
    codes_ibge=ibge_variables, 
    codes_ipeadata=ipeadata_codes, 
    codes_ibge_link=ibge_link_indicators,
    start_date=START_DATE
)

data = economic_brazil.datas_brazil_async(
    datas_bcb=True,
    datas_ibge_codigos=True, 
    datas_ibge_link=True, 
    datas_ipeadata=True,
    missing_data=True
)
```

```bash
12.6s ± 2.5s per loop (mean ± std. dev. of 7 runs, 1 loop each)
```

### Performance Improvement
- The asynchronous version is approximately **84% faster**
- Average time reduction: 65.4 seconds
- More consistent performance (lower standard deviation)
- Better resource utilization through concurrent operations

## Notes

- Requires Python 3.10+
- Use `nest_asyncio` in Jupyter notebooks
- Compatible with all sources from the sync version

## Contributing

All contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome. 

## License

[MIT License](https://github.com/Jeferson100/Data-Brasil/blob/main/LICENSE)
