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


# sys.path.append("..")
from .economic_data_process_async import (
    tratando_dados_bcb_async,
    tratando_dados_expectativas_async,
    tratando_dados_ibge_link_async,
    tratando_dados_ibge_codigos_async,
    tratatando_dados_ipeadata_async,
    tratando_dados_google_trends_async,
    tratando_dados_ibge_link_producao_agricola_async,
    tratando_dados_ibge_link_colum_brazil_async,
)
from fredapi import Fred
from .configuracao_apis.api_fred import set_fred_api_key
from pytrends.exceptions import TooManyRequestsError
from typing import List, Dict, Optional

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


class EconomicBrazilAsync:
    def __init__(
        self,
        codigos_banco_central: Optional[Dict[str, int]] = None,
        codigos_ibge: Optional[Dict[str, int]] = None,
        codigos_ibge_link: Optional[Dict[str, str]] = None,
        codigos_ipeadata: Optional[Dict[str, str]] = None,
        codigos_fred: Optional[Dict[str, str]] = None,
        lista_termos_google_trends: Optional[List[str]] = None,
        data_inicio=None,
    ) -> None:
        self.codigos_banco_central = (
            codigos_banco_central or variaveis_banco_central_padrao
        )
        self.codigos_ibge = codigos_ibge or variaveis_ibge_padrao
        self.codigos_ibge_link = codigos_ibge_link or indicadores_ibge_link_padrao
        self.codigos_ipeadata = codigos_ipeadata or codigos_ipeadata_padrao
        self.lista_termos_google_trends = (
            lista_termos_google_trends or lista_google_trends_padrao
        )
        self.codigos_fred = codigos_fred or codigos_fred_padrao
        self.data_inicio = data_inicio or DATA_INICIO

    async def fetch_data_for_code_async(self, link: str, column: str) -> pd.DataFrame:
        return await tratando_dados_ibge_link_async(coluna=column, link=link)

    def data_index(self) -> pd.DataFrame:
        data_index = pd.date_range(
            start=self.data_inicio, end=datetime.today().strftime("%Y-%m-%d"), freq="MS"
        )
        return pd.DataFrame(index=data_index)

    async def dados_banco_central(
        self,
        salvar: bool = False,
        diretorio: Optional[str] = None,
        formato: str = "csv",
    ) -> pd.DataFrame:
        dados = pd.DataFrame()

        async def processar_variavel_banco_central(nome, codigo):
            try:
                # Executa a coleta de dados de forma assíncrona
                resultado = await asyncio.to_thread(
                    tratando_dados_bcb_async,
                    codigo_bcb_tratado={nome: codigo},
                    data_inicio_tratada=self.data_inicio,
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
                for nome, codigo in self.codigos_banco_central.items()
            )
        )

        # Adiciona os resultados ao DataFrame
        for nome, coluna in resultados:
            dados[nome] = coluna

        # Salva os dados, se necessário
        if salvar:
            await asyncio.to_thread(self.salvar_dados, dados, diretorio, formato)
        return dados

    def dados_banco_central_async(
        self,
        salvar: bool = False,
        diretorio: Optional[str] = None,
        formato: str = "csv",
    ) -> pd.DataFrame:
        """
        Função síncrona que encapsula a chamada assíncrona para dados_banco_central_async.
        """
        return asyncio.run(
            self.dados_banco_central(
                salvar=salvar, diretorio=diretorio, formato=formato
            )
        )

    async def dados_expectativas_inflacao(
        self,
        salvar: bool = False,
        diretorio: Optional[str] = None,
        formato: str = "csv",
    ) -> pd.DataFrame:
        """
        Função assíncrona para coletar dados de expectativas de inflação.
        """
        dic_expectativas_inflacao = self.data_index()
        dic_expectativas_inflacao = dic_expectativas_inflacao.join(
            await tratando_dados_expectativas_async()
        )
        if "Mediana" in dic_expectativas_inflacao.columns:
            dic_expectativas_inflacao.rename(
                columns={"Mediana": "ipca_expectativa_focus"}, inplace=True
            )
        if salvar:
            await asyncio.to_thread(
                self.salvar_dados, dic_expectativas_inflacao, diretorio, formato
            )
        return dic_expectativas_inflacao

    def dados_expectativas_inflacao_async(
        self,
        salvar: bool = False,
        diretorio: Optional[str] = None,
        formato: str = "csv",
    ) -> pd.DataFrame:
        """
        Função síncrona que encapsula a chamada assíncrona para dados_expectativas_inflacao_async.
        """
        return asyncio.run(
            self.dados_expectativas_inflacao(
                salvar=salvar, diretorio=diretorio, formato=formato
            )
        )

    async def dados_ibge(
        self,
        salvar: bool = False,
        diretorio: Optional[str] = None,
        formato: str = "pickle",
    ) -> pd.DataFrame:
        dic_ibge = self.data_index()

        async def processar_variavel_ibge(key, valor):
            try:
                if isinstance(valor, dict):
                    # Executa a coleta de dados de forma assíncrona
                    resultado = await asyncio.to_thread(
                        tratando_dados_ibge_codigos_async, codigos=valor, period="all"
                    )
                    resultado = await resultado
                    return key, resultado["Valor"]
                else:
                    print(f"Tipo de valor não suportado para {key}: {type(valor)}")
                    return key, None
            except ValueError:
                print(
                    f"Erro na coleta de dados da variável {key}. Verifique se os códigos {valor} estão ativos em https://sidra.ibge.gov.br/home/pms/brasil."
                )
                return key, None

        # Executa todas as chamadas em paralelo
        resultados = await asyncio.gather(
            *(
                processar_variavel_ibge(key, valor)
                for key, valor in self.codigos_ibge.items()
            )
        )

        # Adiciona os resultados ao DataFrame
        for key, valor in resultados:
            if valor is not None:
                dic_ibge[key] = valor

        if salvar:
            await asyncio.to_thread(self.salvar_dados, dic_ibge, diretorio, formato)
        return dic_ibge

    def dados_ibge_async(
        self,
        salvar: bool = False,
        diretorio: Optional[str] = None,
        formato: str = "pickle",
    ) -> pd.DataFrame:
        """
        Função síncrona que encapsula a chamada assíncrona para dados_ibge_async.
        """
        return asyncio.run(
            self.dados_ibge(salvar=salvar, diretorio=diretorio, formato=formato)
        )

    async def dados_ibge_link(
        self,
        salvar: bool = False,
        diretorio: Optional[str] = None,
        formato: str = "csv",
    ) -> pd.DataFrame:
        dic_ibge_link = self.data_index()

        async def processar_variavel_ibge_link(coluna, link):
            try:
                resultado = await self.fetch_data_for_code_async(
                    link=link, column=coluna
                )
                return coluna, resultado
            except KeyError:
                # Segunda tentativa: tratando_dados_ibge_link_producao_agricola_async
                try:
                    resultado = await asyncio.to_thread(
                        tratando_dados_ibge_link_producao_agricola_async, link, coluna
                    )
                    resultado = await resultado
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
                for key, link in self.codigos_ibge_link.items()
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
                        resultado = await asyncio.to_thread(
                            tratando_dados_ibge_link_colum_brazil_async,
                            key,
                            self.codigos_ibge_link[key],
                        )
                        resultado = await resultado
                        dic_ibge_link[key] = resultado
                    except ValueError:
                        print(
                            f"Erro na coleta da variável {key}. Verifique se o link está ativo: {self.codigos_ibge_link[key]}."
                        )
        if salvar:
            await asyncio.to_thread(
                self.salvar_dados, dic_ibge_link, diretorio, formato
            )
        return dic_ibge_link

    def dados_ibge_link_async(
        self,
        salvar: bool = False,
        diretorio: Optional[str] = None,
        formato: str = "csv",
    ):
        """
        Função síncrona que encapsula a chamada assíncrona para dados_ibge_link_async.
        """
        return asyncio.run(
            self.dados_ibge_link(salvar=salvar, diretorio=diretorio, formato=formato)
        )

    async def dados_ipeadata(
        self,
        salvar: bool = False,
        diretorio: Optional[str] = None,
        formato: str = "csv",
    ) -> pd.DataFrame:
        dic_ipeadata = self.data_index()

        async def processando_variavel_ipeadata(nome, codigo):
            try:
                resultado = await tratatando_dados_ipeadata_async(
                    codigo_ipeadata={nome: codigo}, data=self.data_inicio
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
                for nome, codigo in self.codigos_ipeadata.items()
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
        if salvar:
            await asyncio.to_thread(self.salvar_dados, dic_ipeadata, diretorio, formato)
        return dic_ipeadata

    def dados_ipeadata_async(
        self,
        salvar: bool = False,
        diretorio: Optional[str] = None,
        formato: str = "csv",
    ):
        """
        Função síncrona que encapsula a chamada assíncrona para dados_ipeadata_async.
        """
        return asyncio.run(
            self.dados_ipeadata(salvar=salvar, diretorio=diretorio, formato=formato)
        )

    async def dados_google_trends(
        self,
        frequencia_datas: Optional[str] = None,
        salvar: bool = False,
        diretorio: Optional[str] = None,
        formato: str = "csv",
    ) -> pd.DataFrame:
        """
        Função assíncrona para coletar dados do Google Trends.
        """
        if frequencia_datas is None:
            frequencia_datas = "MS"

        dic_google_trends = self.data_index()

        async def processar_termo_google_trends(termo: str):
            try:
                resultado = await asyncio.to_thread(
                    tratando_dados_google_trends_async,
                    [termo],
                    frequencia_data=frequencia_datas,
                    start_date=self.data_inicio,
                )
                return termo, resultado
            except ValueError:
                print(
                    f"Erro na coleta da variavel {termo}. Verifique se o termo esta ativo: https://trends.google.com/trends/explore?hl=pt-BR"
                )
                return termo, None
            except TooManyRequestsError:
                print(
                    f"Too many requests error for {termo}. Skipping this term for now."
                )
                return termo, None

        # Executa todas as chamadas em paralelo
        resultados = await asyncio.gather(
            *(
                processar_termo_google_trends(termo)
                for termo in self.lista_termos_google_trends
            )
        )

        # Adiciona os resultados ao DataFrame
        for termo, resultado in resultados:
            if resultado is not None:
                dic_google_trends = dic_google_trends.join(await resultado)

        if salvar:
            await asyncio.to_thread(
                self.salvar_dados, dic_google_trends, diretorio, formato
            )

        return dic_google_trends

    def dados_google_trends_async(
        self,
        frequencia_datas: Optional[str] = None,
        salvar: bool = False,
        diretorio: Optional[str] = None,
        formato: str = "csv",
    ):
        """
        Função síncrona que encapsula a chamada assíncrona para dados_google_trends_async.
        """
        return asyncio.run(
            self.dados_google_trends(
                frequencia_datas=frequencia_datas,
                salvar=salvar,
                diretorio=diretorio,
                formato=formato,
            )
        )

    async def dados_fred(
        self,
        salvar: bool = False,
        diretorio: Optional[str] = None,
        formato: str = "csv",
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

        async def processar_variavel_fred(key: str, code: str):
            try:
                # Executa a coleta de dados de forma assíncrona
                fred = Fred(api_key=api_key)
                resultado = await asyncio.to_thread(fred.get_series, code)
                return key, resultado
            except ValueError:
                print(
                    f"Erro na coleta da variável {key}. Verifique se os códigos {code} estão ativos em https://fred.stlouisfed.org/."
                )
                return key, None

        if api_key:
            # Executa todas as chamadas em paralelo
            resultados = await asyncio.gather(
                *(
                    processar_variavel_fred(key, code)
                    for key, code in self.codigos_fred.items()
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

        if salvar:
            await asyncio.to_thread(self.salvar_dados, dic_fred, diretorio, formato)
        return dic_fred

    def dados_fred_async(
        self,
        salvar: bool = False,
        diretorio: Optional[str] = None,
        formato: str = "csv",
    ):
        """
        Função síncrona que encapsula a chamada assíncrona para dados_fred_async.
        """
        return asyncio.run(
            self.dados_fred(salvar=salvar, diretorio=diretorio, formato=formato)
        )

    async def dados_brazil(
        self,
        dados_bcb: bool = True,
        dados_ibge_codigos: bool = True,
        dados_expectativas_inflacao: bool = True,
        dados_ibge_link: bool = True,
        dados_ipeadata: bool = True,
        dados_google_trends: bool = False,
        dados_fred: bool = False,
        sem_dados_faltantes: bool = True,
        metodo_preenchimento: str = "ffill",
        salvar: Optional[bool] = None,
        diretorio: Optional[str] = None,
        formato: str = "csv",
    ) -> pd.DataFrame:
        """
        Função assíncrona para coletar todos os dados econômicos.
        """
        dados = self.data_index()

        # Lista para armazenar as tarefas assíncronas
        tarefas = []

        if dados_bcb:
            tarefas.append(self.dados_banco_central())
        if dados_ibge_codigos:
            tarefas.append(self.dados_ibge())
        if dados_ibge_link:
            tarefas.append(self.dados_ibge_link())
        if dados_expectativas_inflacao:
            tarefas.append(self.dados_expectativas_inflacao())
        if dados_ipeadata:
            tarefas.append(self.dados_ipeadata())
        if dados_google_trends:
            tarefas.append(self.dados_google_trends())
        if dados_fred:
            tarefas.append(self.dados_fred())

        # Executa todas as tarefas em paralelo
        resultados = await asyncio.gather(*tarefas)

        # Combina os resultados
        for resultado in resultados:
            dados = dados.join(resultado)

        # Trata dados faltantes
        if sem_dados_faltantes:
            if metodo_preenchimento == "ffill":
                dados = await asyncio.to_thread(dados.ffill)
                dados = await asyncio.to_thread(dados.bfill)

        # Salva os dados
        if salvar:
            await asyncio.to_thread(self.salvar_dados, dados, diretorio, formato)

        return dados

    def dados_brazil_async(
        self,
        dados_bcb: bool = True,
        dados_ibge_codigos: bool = True,
        dados_expectativas_inflacao: bool = True,
        dados_ibge_link: bool = True,
        dados_ipeadata: bool = True,
        dados_google_trends: bool = False,
        dados_fred: bool = False,
        sem_dados_faltantes: bool = True,
        metodo_preenchimento: str = "ffill",
        salvar: Optional[bool] = None,
        diretorio: Optional[str] = None,
        formato: str = "csv",
    ) -> pd.DataFrame:
        """
        Função síncrona que encapsula a chamada assíncrona para dados_brazil_async.
        """
        return asyncio.run(
            self.dados_brazil(
                dados_bcb=dados_bcb,
                dados_ibge_codigos=dados_ibge_codigos,
                dados_expectativas_inflacao=dados_expectativas_inflacao,
                dados_ibge_link=dados_ibge_link,
                dados_ipeadata=dados_ipeadata,
                dados_google_trends=dados_google_trends,
                dados_fred=dados_fred,
                sem_dados_faltantes=sem_dados_faltantes,
                metodo_preenchimento=metodo_preenchimento,
                salvar=salvar,
                diretorio=diretorio,
                formato=formato,
            )
        )

    def salvar_dados(self, dados, diretorio=None, formato="csv"):
        if not diretorio:
            raise ValueError("Diretório não especificado para salvar o arquivo")
        if formato == "csv":
            dados.to_csv(diretorio)
        elif formato == "excel":
            dados.to_excel(f"{diretorio}.xlsx")
        elif formato == "json":
            dados.to_json(f"{diretorio}.json")
        elif formato == "pickle":
            with open(f"{diretorio}.pkl", "wb") as f:
                pickle.dump(dados, f)
        else:
            raise ValueError("Formato de arquivo não suportado")


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
    economic_brazil = EconomicBrazilAsync(codigos_ipeadata=codigos_ipeadata_padrao)
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
    print(economic_brazil.dados_banco_central_async())

    print("Expectativas Inflação:")
    expectativas_inflacao_data = economic_brazil.dados_expectativas_inflacao_async(
        salvar=True, diretorio="dados_expectativas_inflacao.csv"
    )
    print(expectativas_inflacao_data)

    print("IBGE:")
    ibge_data = economic_brazil.dados_ibge_async()
    print(ibge_data)

    print("IBGE Link:")
    ibge_link_data = economic_brazil.dados_ibge_link_async()
    print(ibge_link_data)

    print("Ipeadata:")
    ipeadata_data = economic_brazil.dados_ipeadata_async()
    print(ipeadata_data)

    print("Google Trends:")
    # google_trends_data = economic_brazil.dados_google_trends_async()
    # print(google_trends_data)

    print("FRED:")
    fred_data = economic_brazil.dados_fred_async()
    print(fred_data)

    economic_brazil = EconomicBrazilAsync()

    print("dados_brazil_async:")
    print(economic_brazil.dados_brazil_async())

    end = time.time()
    print(f"Tempo de execução: {end - start} segundos")
    # loop.close()
