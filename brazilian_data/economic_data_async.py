import sys
import pandas as pd
from datetime import datetime
import warnings
import pickle
import os
from dotenv import load_dotenv
import time
import asyncio
import requests
from requests.exceptions import RequestException


# sys.path.append("..")
from .economic_data_process_async import (
    tratando_dados_bcb_async,
    tratando_dados_expectativas_async,
    tratando_dados_ibge_link_async,
    tratando_dados_ibge_codigos_async,
    tratatando_dados_ipeadata_async,
    tratando_dados_ibge_link_producao_agricola_async,
    tratando_dados_ibge_link_colum_brazil_async,
)
from fredapi import Fred
from .configuracao_apis.api_fred import set_fred_api_key
from typing import Dict, Optional

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

lista_google_trends_padrao = [
    "seguro desemprego",
]

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


class EconomicDataAsync:
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

    async def fetch_data_for_code_async(self, link: str, column: str) -> pd.DataFrame:
        """
        Fetch data from IBGE link for a specific column.

        :param link: URL link to fetch data from.
        :param column: Column name to fetch data for.
        :return: Data fetched from the specified link and column.
        """
        return await tratando_dados_ibge_link_async(coluna=column, link=link)

    def data_index(self) -> pd.DataFrame:
        """
        Generate a DataFrame with a date range starting from start_date.

        :return: DataFrame with a date range as index.
        """
        data_index = pd.date_range(
            start=self.start_date, end=datetime.today().strftime("%Y-%m-%d"), freq="MS"
        )
        return pd.DataFrame(index=data_index)

    async def datas_banco_central(
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

        async def processar_variavel_banco_central(
            nome: str, codigo: int
        ) -> tuple[str, pd.Series]:
            try:
                # Executa a coleta de dados de forma assíncrona
                resultado = await asyncio.to_thread(
                    tratando_dados_bcb_async,
                    codigo_bcb_tratado={nome: codigo},
                    data_inicio_tratada=self.start_date,
                )
                coluna = (await resultado)[nome]

                # Converte para numérico de forma assíncrona, se necessário
                if coluna.dtype == "object":
                    coluna = await asyncio.to_thread(
                        pd.to_numeric, coluna, errors="coerce"
                    )

                return nome, coluna
            except ValueError:
                print(
                    f"Erro na coleta de dados da variável {nome}. Verifique se o código {codigo} está ativo https://www3.bcb.gov.br/sgspub/localizarseries/localizarSeries.do?method=prepararTelaLocalizarSeries"
                )
                return nome, pd.Series(dtype="float64")
            except requests.exceptions.SSLError:
                print(
                    f"Erro SSL na coleta de dados da variável {nome}. https://www3.bcb.gov.br/sgspub/localizarseries/localizarSeries.do?method=prepararTelaLocalizarSeries"
                )
                return nome, pd.Series(dtype="float64")

        # Executa o loop de forma assíncrona para todas as variáveis

        resultados = await asyncio.gather(
            *(
                processar_variavel_banco_central(nome, codigo)
                for nome, codigo in self.codes_banco_central.items()
            )
        )

        # Adiciona os resultados ao DataFrame
        for nome, coluna in resultados:
            dados[nome] = coluna

        # Salva os dados, se necessário
        if save:
            await asyncio.to_thread(self.save_datas, dados, directory, data_format)
        return dados

    def datas_banco_central_async(
        self,
        save: bool = False,
        directory: Optional[str] = None,
        data_format: str = "csv",
    ) -> pd.DataFrame:
        """
        Fuction async to collect data from Banco Central.
        """
        return asyncio.run(
            self.datas_banco_central(
                save=save, directory=directory, data_format=data_format
            )
        )

    async def datas_expectativas_inflacao(
        self,
        save: bool = False,
        directory: Optional[str] = None,
        data_format: str = "csv",
    ) -> pd.DataFrame:
        """
        Function to collect data from expectativas inflação.
        """
        dic_expectativas_inflacao = self.data_index()
        dic_expectativas_inflacao = dic_expectativas_inflacao.join(
            await tratando_dados_expectativas_async()
        )
        if "Mediana" in dic_expectativas_inflacao.columns:
            dic_expectativas_inflacao.rename(
                columns={"Mediana": "ipca_expectativa_focus"}, inplace=True
            )
        if save:
            await asyncio.to_thread(
                self.save_datas, dic_expectativas_inflacao, directory, data_format
            )
        return dic_expectativas_inflacao

    def datas_expectativas_inflacao_async(
        self,
        save: bool = False,
        directory: Optional[str] = None,
        data_format: str = "csv",
    ) -> pd.DataFrame:
        """
        Função síncrona que encapsula a chamada assíncrona para dados_expectativas_inflacao_async.
        """
        return asyncio.run(
            self.datas_expectativas_inflacao(
                save=save, directory=directory, data_format=data_format
            )
        )

    async def datas_ibge(
        self,
        save: bool = False,
        directory: Optional[str] = None,
        data_format: str = "pickle",
    ) -> pd.DataFrame:
        """
        Fetch IBGE data and handle exceptions.

        :param save: Boolean indicating whether to save the data.
        :param diretory: Directory where the data will be saved.
        :param data_format: Format in which to save the data ('csv', 'excel', 'json', 'pickle').
        :return: DataFrame with IBGE data if not saving.
        """
        dic_ibge = self.data_index()

        async def processar_variavel_ibge(
            key: str, valor: Dict
        ) -> tuple[str, pd.Series | None]:
            try:
                if isinstance(valor, dict):
                    # Executa a coleta de dados de forma assíncrona
                    resultado = await tratando_dados_ibge_codigos_async(
                        codigos=valor, period="all"
                    )
                    return key, resultado["Valor"]
                else:
                    print(f"Tipo de valor não suportado para {key}: {type(valor)}")
                    return key, None
            except ValueError:
                print(
                    f"Erro na coleta de dados da variável {key}. Verifique se os códigos {valor} estão ativos em https://sidra.ibge.gov.br/home/pms/brasil."
                )
                return key, None
            except (ConnectionError, RequestException):
                print(
                    f"Erro na coleta de dados da variável {key}. Erro de conexão. Verifique se os códigos {valor} estão ativos em https://sidra.ibge.gov.br/home/pms/brasil."
                )
                return key, None

        # Executa todas as chamadas em paralelo
        resultados = await asyncio.gather(
            *(
                processar_variavel_ibge(key, valor)
                for key, valor in self.codes_ibge.items()
            )
        )

        # Adiciona os resultados ao DataFrame
        for key, valor in resultados:
            if valor is not None:
                dic_ibge[key] = valor

        if save:
            await asyncio.to_thread(self.save_datas, dic_ibge, directory, data_format)
        return dic_ibge

    def datas_ibge_async(
        self,
        save: bool = False,
        directory: Optional[str] = None,
        data_format: str = "pickle",
    ) -> pd.DataFrame:
        """
        Função síncrona que encapsula a chamada assíncrona para dados_ibge_async.
        """
        return asyncio.run(
            self.datas_ibge(save=save, directory=directory, data_format=data_format)
        )

    async def datas_ibge_link(
        self,
        save: bool = False,
        directory: Optional[str] = None,
        data_format: str = "csv",
    ) -> pd.DataFrame:
        dic_ibge_link = self.data_index()

        async def processar_variavel_ibge_link(
            coluna: str, link: str
        ) -> tuple[str, pd.DataFrame | None]:
            try:
                resultado = await self.fetch_data_for_code_async(
                    link=link, column=coluna
                )
                return coluna, resultado
            except KeyError:
                # Segunda tentativa: tratando_dados_ibge_link_producao_agricola_async
                try:
                    # resultado = await asyncio.to_thread(tratando_dados_ibge_link_producao_agricola_async, link, coluna)
                    # resultado = await resultado
                    resultado = await tratando_dados_ibge_link_producao_agricola_async(
                        link, coluna
                    )
                    return coluna, resultado
                except ValueError:
                    print(
                        f"Erro na coleta da variável {coluna}. Verifique se o link está ativo: {link}."
                    )
                    return coluna, None

            except ValueError:
                print(
                    f"Erro na coleta da variável {coluna}. Verifique se o link está ativo: {link}."
                )
                return coluna, None

        # Executa todas as chamadas em paralelo
        resultados = await asyncio.gather(
            *(
                processar_variavel_ibge_link(key, link)
                for key, link in self.codes_ibge_link.items()
            )
        )

        for key, valor in resultados:
            if valor is not None:
                dic_ibge_link[key] = valor
                # Verifica se precisa usar tratando_dados_ibge_link_colum_brazil
                if key not in dic_ibge_link.columns or bool(
                    dic_ibge_link[key].isnull().all()
                ):
                    try:
                        # resultado = await asyncio.to_thread(tratando_dados_ibge_link_colum_brazil_async,key,self.codes_ibge_link[key],)
                        resultado = await tratando_dados_ibge_link_colum_brazil_async(
                            key,
                            self.codes_ibge_link[key],
                        )
                        # resultado = await resultado
                        dic_ibge_link[key] = resultado
                    except ValueError:
                        print(
                            f"Erro na coleta da variável {key}. Verifique se o link está ativo: {self.codes_ibge_link[key]}."
                        )
        if save:
            await asyncio.to_thread(
                self.save_datas, dic_ibge_link, directory, data_format
            )
        return dic_ibge_link

    def datas_ibge_link_async(
        self,
        save: bool = False,
        directory: Optional[str] = None,
        data_format: str = "csv",
    ) -> pd.DataFrame:
        """
        Function that encapsulates the asynchronous call to datas_ibge_link.
        """
        return asyncio.run(
            self.datas_ibge_link(
                save=save, directory=directory, data_format=data_format
            )
        )

    async def datas_ipeadata(
        self,
        save: bool = False,
        directory: Optional[str] = None,
        data_format: str = "csv",
    ) -> pd.DataFrame:
        dic_ipeadata = self.data_index()

        async def processando_variavel_ipeadata(
            nome: str, codigo: str
        ) -> tuple[str, pd.DataFrame | None]:
            try:
                resultado = await tratatando_dados_ipeadata_async(
                    codigo_ipeadata={nome: codigo}, data=self.start_date
                )
                return nome, resultado
            except (KeyError, ValueError) as e:
                print(
                    f"Erro na coleta da variável {nome} (código {codigo}): {str(e)}\n"
                    f"Verifique se o código está ativo em http://www.ipeadata.gov.br/Default.aspx"
                )
                return nome, None

        # Executa todas as chamadas em paralelo
        resultados = await asyncio.gather(
            *(
                processando_variavel_ipeadata(nome, codigo)
                for nome, codigo in self.codes_ipeadata.items()
            )
        )

        for key, valor in resultados:
            if valor is not None:
                dic_ipeadata[key] = valor

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
                "Erro na juncao da variavel caged antigo e novo. Verifique se o codigo esta ativo: http://www.ipeadata.gov.br/Default.aspx"
            )
        if save:
            await asyncio.to_thread(
                self.save_datas, dic_ipeadata, directory, data_format
            )
        return dic_ipeadata

    def datas_ipeadata_async(
        self,
        save: bool = False,
        directory: Optional[str] = None,
        data_format: str = "csv",
    ) -> pd.DataFrame:
        """
        Função síncrona que encapsula a chamada assíncrona para dados_ipeadata_async.
        """
        return asyncio.run(
            self.datas_ipeadata(save=save, directory=directory, data_format=data_format)
        )

    async def datas_fred(
        self,
        save: bool = False,
        directory: Optional[str] = None,
        data_format: str = "csv",
    ) -> pd.DataFrame:
        dic_fred = self.data_index()

        # Configuração da API FRED
        base_dir = os.path.dirname(os.path.abspath(__file__))
        dotenv_path = os.path.abspath(os.path.join(base_dir, ".env"))

        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)

        api_key = os.getenv("FRED_API_KEY")
        if not api_key:
            set_fred_api_key()
            sys.exit(
                "Chave de API do FRED salva com sucesso. Encerrando o script. Rode o script novamente para coletar os dados."
            )

        async def processar_variavel_fred(
            key: str, code: str
        ) -> tuple[str, pd.Series | pd.DataFrame]:
            try:
                # Executa a coleta de dados de forma assíncrona
                fred = Fred(api_key=api_key)
                resultado = await asyncio.to_thread(fred.get_series, code)
                return key, resultado
            except ValueError:
                print(
                    f"Erro na coleta da variável {key}. Verifique se os códigos {code} estão ativos em https://fred.stlouisfed.org/."
                )
                return key, pd.DataFrame()

        if api_key:
            # Executa todas as chamadas em paralelo
            resultados = await asyncio.gather(
                *(
                    processar_variavel_fred(key, code)
                    for key, code in self.codes_fred.items()
                )
            )

            # Adiciona os resultados ao DataFrame
            for key, valor in resultados:
                if valor is not None:
                    dic_fred[key] = valor
        else:
            print(
                "Verifique se a chave da API está definida corretamente em https://fred.stlouisfed.org/."
            )

        if save:
            await asyncio.to_thread(self.save_datas, dic_fred, directory, data_format)
        return dic_fred

    def datas_fred_async(
        self,
        save: bool = False,
        directory: Optional[str] = None,
        data_format: str = "csv",
    ) -> pd.DataFrame:
        """
        Função síncrona que encapsula a chamada assíncrona para dados_fred_async.
        """
        return asyncio.run(
            self.datas_fred(save=save, directory=directory, data_format=data_format)
        )

    async def datas_brazil(
        self,
        datas_bcb: bool = True,
        datas_ibge_codigos: bool = True,
        datas_expectativas_inflacao: bool = True,
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

        # Lista para armazenar as tarefas assíncronas
        tarefas = []

        if datas_bcb:
            tarefas.append(self.datas_banco_central())
        if datas_ibge_codigos:
            tarefas.append(self.datas_ibge())
        if datas_ibge_link:
            tarefas.append(self.datas_ibge_link())
        if datas_expectativas_inflacao:
            tarefas.append(self.datas_expectativas_inflacao())
        if datas_ipeadata:
            tarefas.append(self.datas_ipeadata())
        if datas_fred:
            tarefas.append(self.datas_fred())

        # Executa todas as tarefas em paralelo
        resultados = await asyncio.gather(*tarefas)

        # Combina os resultados
        for resultado in resultados:
            dados = dados.join(resultado)

        # Trata dados faltantes
        if missing_data:
            if fill_method == "ffill":
                dados = await asyncio.to_thread(dados.ffill)
                dados = await asyncio.to_thread(dados.bfill)

        # Salva os dados
        if save:
            await asyncio.to_thread(self.save_datas, dados, directory, data_format)

        return dados

    def datas_brazil_async(
        self,
        datas_bcb: bool = True,
        datas_ibge_codigos: bool = True,
        datas_expectativas_inflacao: bool = True,
        datas_ibge_link: bool = True,
        datas_ipeadata: bool = True,
        datas_fred: bool = False,
        missing_data: bool = True,
        fill_method: str = "ffill",
        save: bool = False,
        directory: Optional[str] = None,
        data_format: str = "csv",
    ) -> pd.DataFrame:
        """
        Função síncrona que encapsula a chamada assíncrona para dados_brazil_async.
        """
        return asyncio.run(
            self.datas_brazil(
                datas_bcb=datas_bcb,
                datas_ibge_codigos=datas_ibge_codigos,
                datas_expectativas_inflacao=datas_expectativas_inflacao,
                datas_ibge_link=datas_ibge_link,
                datas_ipeadata=datas_ipeadata,
                datas_fred=datas_fred,
                missing_data=missing_data,
                fill_method=fill_method,
                save=save,
                directory=directory,
                data_format=data_format,
            )
        )

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

        - datas_banco_central_async(save=None, diretory=None, data_format=None):
            Fetch data from Banco Central and handle exceptions.
            
            Link for verification Time Series: https://www3.bcb.gov.br/sgspub/localizarseries/localizarSeries.do?method=prepararTelaLocalizarSeries  
            
            Input codes: 
                - The Banco Central codes should be a dictionary with the column name that the `datas_banco_central` function will recognize as the column name and the series code. Example: {"selic": 4189}
                
            
        - datas_ibge_async(save=False, diretory=None, data_format=None):
        
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

        - datas_ibge_link_async(save=None, diretory=None, data_format=None):
        
            Fetch data from IBGE links and handle exceptions.
            
            Link for verification Time Series: https://sidra.ibge.gov.br/home/pms/brasil
            
            Input codes:
                The `codes ibge link` input should be a dictionary where each key represents the name of an economic indicator or specific variable (e.g., "pib", "soja"), which the function will use as the column name. 
                The value associated with each key is a URL that points to an Excel file available on the IBGE website, containing the data corresponding to that indicator.
                These URLs are dynamically generated from the IBGE SIDRA system and can be used to download the tables directly. Each link contains specific parameters defining the selection of variables, 
                periods, and territorial levels relevant to the query.

                Example: 
                    {"pib": "https://sidra.ibge.gov.br/geratabela?format=xlsx&name=tabela5932.xlsx&terr=N&rank=-&query=t/5932/n1/all/v/6564/p/all/c11255/90707/d/v6564%201/l/v,p,t%2Bc11255&verUFs=false&verComplementos2=false&verComplementos1=false&omitirIndentacao=false&abreviarRotulos=false&exibirNotas=false&agruparNoCabecalho=false",}
          

        - datas_ipeadata_async(save=None, diretory=None, data_format=None):
            Fetch IPEADATA data and handle exceptions.
            
            Link for verification Time Series: http://www.ipeadata.gov.br/Default.aspx
            
            Input codes:
                The `IPEADATA codes` should be a dictionary with the column name that the `datas_ipeadata` function will recognize as the column name and the series code.

                Example: {"taja_juros_ltn": "ANBIMA12_TJTLN1212",}

        - datas_fred_async(save=None, diretory=None, data_format=None):
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


if __name__ == "__main__":
    start = time.time()

    load_dotenv()

    codigos_ipeadata_padrao = {
        "taja_juros_ltn": "ANBIMA12_TJTLN1212",
        "imposto_renda": "SRF12_IR12",
        "ibovespa": "ANBIMA12_IBVSP12",
        "consumo_energia": "ELETRO12_CEET12",
        "brent_fob": "EIA366_PBRENT366",
        "rendimento_real_medio": "PNADC12_RRTH12",
        "pessoas_forca_trabalho": "PNADC12_FT12",
        "caged_novo": "CAGED12_SALDON12",
        "caged_antigo": "CAGED12_SALDO12",
        "exportacoes": "PAN12_XTV12",
        "importacoes": "PAN12_MTV12",
        "m_1": "BM12_M1MN12",
        "taxa_cambio": "PAN12_ERV12",
        "atividade_economica": "SGS12_IBCBR12",
        "producao_industrial": "PAN12_QIIGG12",
        "producao_industrial_intermediario": "PIMPFN12_QIBIN12",
        "capcidade_instalada": "CNI12_NUCAP12",
        "caixas_papelao": "ABPO12_PAPEL12",
        "faturamento_industrial": "CNI12_VENREA12",
        "importacoes_industrial": "FUNCEX12_MDQT12",
        "importacoes_intermediario": "FUNCEX12_MDQBIGCE12",
        "confianca_empresario_exportador": "CNI12_ICEIEXP12",
        "confianca_empresario_atual": "CNI12_ICEICA12",
        "confianca_consumidor": "FCESP12_IIC12",
        "ettj_26": "ANBIMA366_TJTLN6366",
    }
    economic_brazil = EconomicDataAsync(codes_ipeadata=codigos_ipeadata_padrao)
    print("Index:")
    print(economic_brazil.data_index())

    print("fetch_data_for_code_async:")
    loop = asyncio.get_event_loop()
    print(
        loop.run_until_complete(
            economic_brazil.fetch_data_for_code_async(
                indicadores_ibge_link_padrao["pib"], "PIB"
            )
        )
    )

    print("Banco Central:")
    print(economic_brazil.datas_banco_central_async())

    print("Expectativas Inflação:")
    expectativas_inflacao_data = economic_brazil.datas_expectativas_inflacao_async(
        save=True, directory="dados_expectativas_inflacao.csv"
    )
    print(expectativas_inflacao_data)

    print("IBGE:")
    ibge_data = economic_brazil.datas_ibge_async()
    print(ibge_data)

    print("IBGE Link:")
    ibge_link_data = economic_brazil.datas_ibge_link_async()
    print(ibge_link_data)

    print("Ipeadata:")
    ipeadata_data = economic_brazil.datas_ipeadata_async()
    print(ipeadata_data)

    print("FRED:")
    fred_data = economic_brazil.datas_fred_async()
    print(fred_data)

    economic_brazil = EconomicDataAsync()

    print("dados_brazil_async:")
    print(economic_brazil.datas_brazil_async())

    end = time.time()
    print(f"Tempo de execução: {end - start} segundos")
    # loop.close()
