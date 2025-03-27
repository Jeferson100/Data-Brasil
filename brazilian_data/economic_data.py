#!/usr/bin/env python
import sys
import pandas as pd
from datetime import datetime
import warnings
import pickle
import os
from dotenv import load_dotenv, find_dotenv
from typing import Optional, Dict

#sys.path.append("..")
from .economic_data_process import (
    tratando_dados_bcb,
    tratando_dados_ibge_link,
    tratando_dados_ibge_codigos,
    tratatando_dados_ipeadata,
    tratando_dados_ibge_link_producao_agricola,
    tratando_dados_ibge_link_colum_brazil,
)
from fredapi import Fred
from .configuracao_apis.api_fred import set_fred_api_key

warnings.filterwarnings("ignore")

DATA_INICIO = "2000-01-01"

variaveis_banco_central_padrao = {
    "selic": 4189,
    "IPCA-EX2": 27838,
    "IPCA-EX3": 27839,
    "IPCA-MS": 4466,
    "IPCA-MA": 11426,
    "IPCA-EX0": 11427,
    "IPCA-EX1": 16121,
    "IPCA-DP": 16122,
    "cambio": 3698,
    "pib_mensal": 4380,
    "igp_m": 189,
    "igp_di": 190,
    "m1": 27788,
    "m2": 27810,
    "m3": 27813,
    "m4": 27815,
    "estoque_caged": 28763,
    "saldo_bc": 22707,
    "vendas_auto": 7384,
    "divida_liquida_spc": 4513,
}

variaveis_ibge_padrao = {
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

codigos_ipeadata_padrao = {
    "taja_juros_ltn": "ANBIMA12_TJTLN1212",
    "imposto_renda": "SRF12_IR12",
    "ibovespa": "ANBIMA12_IBVSP12",
    "consumo_energia": "ELETRO12_CEET12",
    "brent_fob": "EIA366_PBRENT366",
}

indicadores_ibge_link_padrao = {
    "pib": "https://sidra.ibge.gov.br/geratabela?format=xlsx&name=tabela5932.xlsx&terr=N&rank=-&query=t/5932/n1/all/v/6564/p/all/c11255/90707/d/v6564%201/l/v,p,t%2Bc11255&verUFs=false&verComplementos2=false&verComplementos1=false&omitirIndentacao=false&abreviarRotulos=false&exibirNotas=false&agruparNoCabecalho=false",
    "despesas_publica": "https://sidra.ibge.gov.br/geratabela?format=xlsx&name=tabela5932.xlsx&terr=N&rank=-&query=t/5932/n1/all/v/6561/p/all/c11255/93405/d/v6561%201/l/v,p%2Bc11255,t",
    "capital_fixo": "https://sidra.ibge.gov.br/geratabela?format=xlsx&name=tabela5932.xlsx&terr=N&rank=-&query=t/5932/n1/all/v/6561/p/all/c11255/93406/d/v6561%201/l/v,p%2Bc11255,t",
    "producao_industrial_manufatureira": "https://sidra.ibge.gov.br/geratabela?format=xlsx&name=tabela8158.xlsx&terr=N&rank=-&query=t/8158/n1/all/v/11599/p/all/c543/129278/d/v11599%205/l/v,p%2Bc543,t",
    "soja": "https://sidra.ibge.gov.br/geratabela?format=xlsx&name=tabela6588.xlsx&terr=N&rank=-&query=t/6588/n1/all/v/35/p/all/c48/0,39443/l/v,p%2Bc48,t",
    "milho_1": "https://sidra.ibge.gov.br/geratabela?format=xlsx&name=tabela6588.xlsx&terr=N&rank=-&query=t/6588/n1/all/v/35/p/all/c48/0,39441/l/v,p%2Bc48,t",
    "milho_2": "https://sidra.ibge.gov.br/geratabela?format=xlsx&name=tabela6588.xlsx&terr=N&rank=-&query=t/6588/n1/all/v/35/p/all/c48/0,39442/l/v,p%2Bc48,t",
}


codigos_fred_padrao = {
    "nasdaq100": "NASDAQ100",
    "taxa_cambio_efetiva": "RBBRBIS",
    "cboe_nasdaq": "VXNCLS",
    "taxa_juros_interbancaria": "IRSTCI01BRM156N",
    "atividade_economica_eua": "USPHCI",
    "indice_confianca_manufatura": "BSCICP03BRM665S",
    "indice_confianca_exportadores": "BSXRLV02BRM086S",
    "indice_tendencia_emprego": "BRABREMFT02STSAM",
    "indice_confianca_consumidor": "CSCICP03BRM665S",
    "capacidade_instalada": "BSCURT02BRM160S",
}


class EconomicData:
    def __init__(
        self,
        codes_banco_central: Optional[Dict[str, int]] = None,
        codes_ibge: Optional[Dict[str, dict]] = None,
        codes_ibge_link: Optional[Dict[str, str]] = None,
        codes_ipeadata: Optional[Dict[str, str]] = None,
        codes_fred: Optional[Dict[str, str]] = None,
        start_date: Optional[str] = None,
    ) -> None:
        self.codes_banco_central = codes_banco_central or variaveis_banco_central_padrao
        self.codes_ibge = codes_ibge or variaveis_ibge_padrao
        self.codes_ibge_link = codes_ibge_link or indicadores_ibge_link_padrao
        self.codes_ipeadata = codes_ipeadata or codigos_ipeadata_padrao
        self.codes_fred = codes_fred or codigos_fred_padrao
        self.start_date = start_date or DATA_INICIO

        """
        Initialize the EconomicData class with optional parameters.

        :param codes_banco_central: Dictionary of Banco Central codes.
        :param codes_ibge: Dictionary of IBGE codes.
        :param codes_ibge_link: Dictionary of IBGE links.
        :param codes_ipeadata: Dictionary of IPEADATA codes.
        :param codes_fred: Dictionary of FRED codes.
        :param start_date: Start date for data fetching.
        """

    def fetch_data_for_code(self, link: str, column: str) -> pd.DataFrame:
        """
        Fetch data from IBGE link for a specific column.

        :param link: URL link to fetch data from.
        :param column: Column name to fetch data for.
        :return: Data fetched from the specified link and column.
        """
        return tratando_dados_ibge_link(coluna=column, link=link)

    def data_index(self) -> pd.DataFrame:
        """
        Generate a DataFrame with a date range starting from start_date.

        :return: DataFrame with a date range as index.
        """
        data_index = pd.date_range(
            start=self.start_date, end=datetime.today().strftime("%Y-%m-%d"), freq="MS"
        )
        return pd.DataFrame(index=data_index)

    def datas_banco_central(
        self,
        save: bool = False,
        directory: Optional[str] = None,
        data_format: Optional[str] = None,
    ) -> pd.DataFrame:
        """
        Fetch data from Banco Central and handle exceptions.

        :param save: Boolean indicating whether to save the data.
        :param diretory: Directory where the data will be saved.
        :param data_format: Format in which to save the data ('csv', 'excel', 'json', 'pickle').
        :return: DataFrame with Banco Central data if not saving.
        """
        dados = pd.DataFrame()
        if data_format is None:
            data_format = "csv"
        for nome, codigo in self.codes_banco_central.items():
            try:
                dados[nome] = tratando_dados_bcb(
                    codigo_bcb_tratado={nome: codigo},
                    data_inicio_tratada=self.start_date,
                )[nome]
                if dados[nome].dtype == "object":
                    dados[nome] = pd.to_numeric(dados[nome], errors="coerce")
            except ValueError:
                print(
                    f"Error collecting data for variable {nome}. Please check if the code {codigo} is active at https://www3.bcb.gov.br/sgspub/localizarseries/localizarSeries.do?method=prepararTelaLocalizarSeries"
                )
        if save:
            self.save_datas(dados, directory, data_format)
            return dados
        else:
            return dados

    def datas_ibge(
        self,
        save: bool = False,
        directory: Optional[str] = None,
        data_format: Optional[str] = None,
    ) -> pd.DataFrame:
        """
        Fetch IBGE data and handle exceptions.

        :param save: Boolean indicating whether to save the data.
        :param diretory: Directory where the data will be saved.
        :param data_format: Format in which to save the data ('csv', 'excel', 'json', 'pickle').
        :return: DataFrame with IBGE data if not saving.
        """
        if data_format is None:
            data_format = "csv"
        dic_ibge = self.data_index()
        for key, valor in self.codes_ibge.items():
            try:
                dic_ibge[key] = tratando_dados_ibge_codigos(
                    codigos=valor, period="all"
                )["Valor"]
            except ValueError:
                print(
                    f"Error collecting data for variable {key}. Please check if the code {valor} is active at https://sidra.ibge.gov.br/home/pms/brasil."
                )
        if save:
            self.save_datas(dic_ibge, directory, data_format)
            return dic_ibge
        else:
            return dic_ibge

    def datas_ibge_link(
        self,
        save: bool = False,
        directory: Optional[str] = None,
        data_format: Optional[str] = None,
    ) -> pd.DataFrame:
        """
        Fetch data from IBGE links and handle exceptions.

        :param save: Boolean indicating whether to save the data.
        :param diretory: Directory where the data will be saved.
        :param data_format: Format in which to save the data ('csv', 'excel', 'json', 'pickle').
        :return: DataFrame with IBGE link data if not saving.
        """
        if data_format is None:
            data_format = "csv"
        dic_ibge_link = self.data_index()
        for key, link in self.codes_ibge_link.items():
            try:
                dic_ibge_link[key] = self.fetch_data_for_code(link, key)

            except KeyError:
                dic_ibge_link[key] = tratando_dados_ibge_link_producao_agricola(
                    link, key
                )

            except ValueError:
                print(
                    f"Error collecting data for variable {key}. Please check if the link {link} is active at https://sidra.ibge.gov.br/home/pms/brasil."
                )
            try:
                if key not in dic_ibge_link.columns or bool(
                    dic_ibge_link[key].isnull().all()
                ):
                    dic_ibge_link[key] = tratando_dados_ibge_link_colum_brazil(
                        key, link
                    )
            except ValueError:
                print(
                    f"Error collecting data for variable {key}. Please check if the link {link} is active at https://sidra.ibge.gov.br/home/pms/brasil."
                )
        if save:
            self.save_datas(dic_ibge_link, directory, data_format)
            return dic_ibge_link
        else:
            return dic_ibge_link

    def datas_ipeadata(
        self,
        salve: bool = False,
        directory: Optional[str] = None,
        data_format: Optional[str] = None,
    ) -> pd.DataFrame:
        """
        Fetch IPEADATA data and handle exceptions.

        :param save: Boolean indicating whether to save the data.
        :param diretory: Directory where the data will be saved.
        :param data_format: Format in which to save the data ('csv', 'excel', 'json', 'pickle').
        :return: DataFrame with IPEADATA data if not saving.
        """
        if data_format is None:
            data_format = "csv"
        dic_ipeadata = self.data_index()
        for nome, codigo in self.codes_ipeadata.items():
            try:
                dic_ipeadata[nome] = tratatando_dados_ipeadata(
                    codigo_ipeadata={nome: codigo}, data=self.start_date
                )
            except ValueError:
                print(
                    f"Error collecting data for variable {codigo}. Please check if the code {codigo} is active: http://www.ipeadata.gov.br/Default.aspx"
                )
            except KeyError:
                print(
                    f"Error collecting data for variable {codigo}. Please check if the code {codigo} is active: http://www.ipeadata.gov.br/Default.aspx"
                )
        try:
            if (
                "caged_antigo" in dic_ipeadata.columns
                and "caged_novo" in dic_ipeadata.columns
            ):
                dic_ipeadata["caged_junto"] = pd.concat(
                    [
                        dic_ipeadata.caged_antigo.dropna(),
                        dic_ipeadata.caged_novo.dropna(),
                    ]
                )
                dic_ipeadata = dic_ipeadata.drop(["caged_antigo", "caged_novo"], axis=1)
        except ValueError:
            print(
                "Error in join of variable caged old and new. Please check if the code at http://www.ipeadata.gov.br/Default.aspx"
            )
        if salve:
            self.save_datas(dic_ipeadata, directory, data_format)
            return dic_ipeadata
        else:
            return dic_ipeadata

    def datas_fred(
        self,
        save: bool = False,
        directory: Optional[str] = None,
        data_format: Optional[str] = None,
    ) -> pd.DataFrame:
        """
        Fetch data from FRED and handle exceptions.

        :param save: Boolean indicating whether to save the data.
        :param diretory: Directory where the data will be saved.
        :param data_format: Format in which to save the data ('csv', 'excel', 'json', 'pickle').
        :return: DataFrame with FRED data if not saving.
        """
        if data_format is None:
            data_format = "csv"
        dic_fred = self.data_index()

        dotenv_path = find_dotenv()
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)
        api_key = os.getenv("FRED_API_KEY")
        if not api_key:
            set_fred_api_key()
            sys.exit(
                "FRED API key successfully saved. Exiting the script. Run the script again to collect the data."
            )
        fred = Fred(api_key=api_key)
        if fred:
            for key, codes in self.codes_fred.items():
                try:
                    dic_fred[key] = fred.get_series(codes)
                except ValueError:
                    print(
                        f"Error collecting data for variable {key}. Please check if the code {codes} is active at https://fred.stlouisfed.org/."
                    )
        else:
            print(
                "Please, check if your API key is valid correctly at https://fred.stlouisfed.org."
            )

        if save:
            self.save_datas(dic_fred, directory, data_format)
            return dic_fred
        else:
            return dic_fred

    def datas_brazil(
        self,
        datas_bcb: bool = True,
        datas_ibge_codigos: bool = True,
        datas_ibge_link: bool = True,
        datas_ipeadata: bool = True,
        datas_fred: bool = False,
        missing_data: bool = True,
        fill_method: Optional[str] = None,
        save: bool = False,
        directory: Optional[str] = None,
        data_format: Optional[str] = None,
    ) -> pd.DataFrame:
        """
        Fetch all data based on specified options.

        :param datas_bcb: Boolean indicating whether to fetch Banco Central data.
        :param datas_ibge_codigos: Boolean indicating whether to fetch IBGE data by codes.
        :param datas_inflation_expectations: Boolean indicating whether to fetch inflation expectations data.
        :param datas_ibge_link: Boolean indicating whether to fetch IBGE data by links.
        :param datas_ipeadata: Boolean indicating whether to fetch IPEADATA data.
        :param datas_fred: Boolean indicating whether to fetch FRED data.
        :param missing_data: Boolean indicating whether to handle missing data.
        :param fill_method: Method to handle missing data ('ffill' or 'bfill').
        :param save: Boolean indicating whether to save the data.
        :param directory: Directory where the data will be saved.
        :param data_format: Format in which to save the data ('csv', 'excel', 'json', 'pickle').
        :return: DataFrame with all requested data if not saving.
        """
        if fill_method is None:
            fill_method = "ffill"

        if data_format is None:
            data_format = "csv"

        dados = self.data_index()

        if datas_bcb:
            banco_central_df = self.datas_banco_central()
            if banco_central_df is not None:
                dados = dados.join(banco_central_df)
        if datas_ibge_codigos:
            ibge_df = self.datas_ibge()
            if ibge_df is not None:
                dados = dados.join(ibge_df)
        if datas_ibge_link:
            ibge_link_df = self.datas_ibge_link()
            if ibge_link_df is not None:
                dados = dados.join(ibge_link_df)
        if datas_ipeadata:
            ipeadata_df = self.datas_ipeadata()
            if ipeadata_df is not None:
                dados = dados.join(ipeadata_df)
        if datas_fred:
            fred_df = self.datas_fred()
            if fred_df is not None:
                dados = dados.join(fred_df)
        if missing_data:
            if fill_method == "ffill":
                dados = dados.ffill()
                dados = dados.bfill()
        if save:
            self.save_datas(dados, directory, data_format)
            return dados
        else:
            return dados

    def save_datas(
        self,
        dados: pd.DataFrame,
        diretory: Optional[str] = None,
        data_format: Optional[str] = "csv",
    ) -> None:
        """
        Save the data to the specified directory and format.

        :param dados: DataFrame to be saved.
        :param diretory: Directory where the data will be saved.
        :param data_format: Format in which to save the data ('csv', 'excel', 'json', 'pickle').
        """
        if not diretory:
            raise ValueError("Diretory not specified.")
        if data_format == "csv":
            dados.to_csv(diretory)
        elif data_format == "excel":
            dados.to_excel(f"{diretory}.xlsx")
        elif data_format == "json":
            dados.to_json(f"{diretory}.json")
        elif data_format == "pickle":
            with open(f"{diretory}.pkl", "wb") as f:
                pickle.dump(dados, f)
        else:
            raise ValueError("Format of file not supported.")

    def help(self) -> None:
        """
        Print out information about the available methods and their usage.
        """
        help_text = """
        EconomicData Class Help:

        Methods:

        - data_index():
            Generate a DataFrame with a date range starting from start_date.

        - datas_banco_central(save=None, diretory=None, data_format=None):
            Fetch data from Banco Central and handle exceptions.
            
            Link for verification Time Series: https://www3.bcb.gov.br/sgspub/localizarseries/localizarSeries.do?method=prepararTelaLocalizarSeries  
            
            Input codes: 
                - The Banco Central codes should be a dictionary with the column name that the `datas_banco_central` function will recognize as the column name and the series code. Example: {"selic": 4189}
                
            
        - datas_ibge(save=False, diretory=None, data_format=None):
        
            Fetch IBGE data and handle exceptions.
            
            Link for verification Time Series: https://sidra.ibge.gov.br/home/ipca/brasil
            
            Input codes:
            
                The `ibge_codes` input should be a dictionary where each key represents the name of a variable (e.g., "ipca"), which the function will use as the column name. The value associated with each key should be another dictionary containing the following fields:

                - `"codigo"`: An integer representing the code of the data series to be collected. This code is specific to the variable and identifies the series in the IBGE database.

                - `"territorial_level"`: A string indicating the territorial level of the data, such as "1" for Brazil, "2" for regions, "3" for states, etc.

                - `"ibge_territorial_code"`: A code defining the specific geographical area of the data. The value `"all"` indicates that data for all areas corresponding to the territorial level should be collected.

                - `"variable"`: A string or number that identifies the specific variable within the data series. This may represent a specific category or indicator to be collected.
                
                Example:
                    ibge_codes = {"ipca": {"codigo": 4330, "territorial_level": "1", "ibge_territorial_code": "all", "variable": "1"}}

        - datas_ibge_link(save=None, diretory=None, data_format=None):
        
            Fetch data from IBGE links and handle exceptions.
            
            Link for verification Time Series: https://sidra.ibge.gov.br/home/pms/brasil
            
            Input codes:
                The `codes ibge link` input should be a dictionary where each key represents the name of an economic indicator or specific variable (e.g., "pib", "soja"), which the function will use as the column name. 
                The value associated with each key is a URL that points to an Excel file available on the IBGE website, containing the data corresponding to that indicator.
                These URLs are dynamically generated from the IBGE SIDRA system and can be used to download the tables directly. Each link contains specific parameters defining the selection of variables, 
                periods, and territorial levels relevant to the query.

                Example: 
                    {"pib": "https://sidra.ibge.gov.br/geratabela?format=xlsx&name=tabela5932.xlsx&terr=N&rank=-&query=t/5932/n1/all/v/6564/p/all/c11255/90707/d/v6564%201/l/v,p,t%2Bc11255&verUFs=false&verComplementos2=false&verComplementos1=false&omitirIndentacao=false&abreviarRotulos=false&exibirNotas=false&agruparNoCabecalho=false",}
                

        - datas_ipeadata(save=None, diretory=None, data_format=None):
            Fetch IPEADATA data and handle exceptions.
            
            Link for verification Time Series: http://www.ipeadata.gov.br/Default.aspx
            
            Input codes:
                The `IPEADATA codes` should be a dictionary with the column name that the `datas_ipeadata` function will recognize as the column name and the series code.

                Example: {"taja_juros_ltn": "ANBIMA12_TJTLN1212",}

        - datas_fred(save=None, diretory=None, data_format=None):
            Fetch data from FRED and handle exceptions.
            
            Link for verification Time Series: https://fred.stlouisfed.org./
            
            Input codes:
                The `FRED codes` should be a dictionary with the column name that the `datas_fred` function will recognize as the column name and the series code.

                Example: {"nasdaq100": "NASDAQ100",}

        - datas_brazil(
            datas_bcb=True,
            datas_ibge_codigos=True,
            datas_inflation_expectations=True,
            datas_ibge_link=True,
            datas_ipeadata=True,
            datas_fred=False,
            missing_data=True,
            fill_method="ffill",
            save=None,
            directory=None,
            data_format=None
        ):
            Fetch all data based on specified options.

        - save_datas(dados, diretory=None, data_format="csv"):
            Save the data to the specified directory and format.
        """
        print(help_text)
