import pandas as pd
from bcb import sgs
import sidrapy
from bcb import Expectativas
import ipeadatapy as ip
from pytrends.request import TrendReq
import time
from datetime import date
from typing import List, Dict, Optional
import asyncio

# Dados BCB
SELIC_CODES = {
    "selic": 4189,
    "IPCA-EX2": 27838,
    "IPCA-EX3": 27839,
    "IPCA-MS": 4466,
    "IPCA-MA": 11426,
    "IPCA-EX0": 11427,
    "IPCA-EX1": 16121,
    "IPCA-DP": 16122,
}

DATA_INICIO = "2000-01-01"


async def dados_bcb_async(
    codigos_banco_central: Optional[Dict[str, int]] = None,
    data_inicio: str = "2000-01-01",
) -> pd.DataFrame:
    dados = pd.DataFrame()
    if codigos_banco_central is None:
        codigos_banco_central = SELIC_CODES
    dados = await asyncio.to_thread(sgs.get, codigos_banco_central, start=data_inicio)
    if not isinstance(dados, pd.DataFrame):
        print("Erro: sgs.get() não retornou um DataFrame. Retornando DataFrame vazio.")
        return pd.DataFrame()
    return dados


# DADOS IBGE
async def dados_ibge_codigos_async(
    codigo: str = "1737",
    territorial_level: str = "1",
    ibge_territorial_code: str = "all",
    variable: str = "63",
    period: str = "all",
) -> pd.DataFrame:
    ipca = await asyncio.to_thread(
        sidrapy.get_table,
        table_code=codigo,
        territorial_level=territorial_level,
        ibge_territorial_code=ibge_territorial_code,
        variable=variable,
        period=period,
    )
    if not isinstance(ipca, pd.DataFrame):
        print("Erro: sgs.get() não retornou um DataFrame. Retornando DataFrame vazio.")
        return pd.DataFrame()
    return ipca


async def dados_ibge_link_async(
    cabecalho: int = 3,
    url: str = "https://sidra.ibge.gov.br/geratabela?format=xlsx&name=tabela5932.xlsx&terr=N&rank=-&query=t/5932/n1/all/v/6561/p/all/c11255/93405/d/v6561%201/l/v,p%2Bc11255,t",
) -> pd.DataFrame:
    # carregar a tabela em um DataFrame
    dados_link = await asyncio.to_thread(pd.read_excel, url, header=cabecalho)
    return dados_link


async def dados_expectativas_focus_async(
    indicador: str = "IPCA",
    tipo_expectativa: str = "ExpectativaMercadoMensais",
    data_inicio: str = "2000-01-01",
) -> pd.DataFrame:
    # End point
    em = Expectativas()
    ep = em.get_endpoint(tipo_expectativa)

    # Dados do IPCA
    def get_ipca_expec():
        return (
            ep.query()  # type: ignore
            .filter(ep.Indicador == indicador)  # type: ignore
            .filter(ep.Data >= data_inicio)  # type: ignore
            .filter(ep.baseCalculo == 0)  # type: ignore
            .select(
                ep.Indicador,  # type: ignore
                ep.Data,  # type: ignore
                ep.Media,  # type: ignore
                ep.Mediana,  # type: ignore
                ep.DataReferencia,  # type: ignore
                ep.baseCalculo,  # type: ignore
            )
            .collect()
        )

    ipca_expec = await asyncio.to_thread(get_ipca_expec)

    if not isinstance(ipca_expec, pd.DataFrame):
        print("Erro: sgs.get() não retornou um DataFrame. Retornando DataFrame vazio.")
        return pd.DataFrame()
    return ipca_expec


async def dados_ipeadata_async(
    codigo: str = "ANBIMA12_TJTLN1212", data: str = "2020-01-01"
) -> pd.DataFrame:
    dados_ipea = await asyncio.to_thread(
        ip.timeseries, codigo, yearGreaterThan=int(data[0:4]) - 1
    )
    if not isinstance(dados_ipea, pd.DataFrame):
        print(
            "Erro: ip.timeseries não retornou um DataFrame. Retornando DataFrame vazio."
        )
        return pd.DataFrame()
    return dados_ipea


async def coleta_google_trends_async(
    kw_list: Optional[List[str]] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """
    Coleta dados do Google Trends de forma assíncrona.

    Args:
        kw_list (Optional[List[str]]): Lista de palavras-chave para pesquisa.
        start_date (Optional[str]): Data de início no formato "YYYY-MM-DD".
        end_date (Optional[str]): Data de término no formato "YYYY-MM-DD".

    Returns:
        pd.DataFrame: DataFrame com os dados coletados.
    """
    if start_date is None:
        start_date = "2004-01-01"
    if end_date is None:
        end_date = str(date.today())
    if kw_list is None:
        kw_list = ["seguro desemprego"]

    # Dividindo a pesquisa em vários períodos de 5 anos
    periods = pd.date_range(start=start_date, end=end_date, freq="5YE")
    if periods[-1] < pd.to_datetime(end_date):
        periods = pd.DatetimeIndex(list(periods) + [pd.to_datetime(end_date)])

    # Criando uma instância do TrendReq

    pytrends = TrendReq()

    # Fazendo a pesquisa para cada período de 5 anos
    data = pd.DataFrame()
    for i in range(len(periods) - 1):
        timeframe = (
            f"{periods[i].strftime('%Y-%m-%d')} {periods[i+1].strftime('%Y-%m-%d')}"
        )

        # Executa a construção do payload e coleta de dados em um thread separado
        await asyncio.to_thread(pytrends.build_payload, kw_list, timeframe=timeframe)
        temp_data = await asyncio.to_thread(pytrends.interest_over_time)

        # Concatena os dados coletados
        data = pd.concat([data, temp_data])

        # Aguarda alguns segundos para evitar sobrecarga no servidor do Google Trends
        await asyncio.sleep(10)

    print("O google trends tem como data de início o ano 2004.")
    return data


if __name__ == "__main__":

    async def main():
        start = time.time()
        # Obtém dados do Banco Central
        print("Obtendo dados do Banco Central...")
        dados_bcb_result = await dados_bcb_async()
        print(dados_bcb_result)

        # Obtém dados do IBGE
        print("Obtendo dados do IBGE...")
        dados_ibge_result = await dados_ibge_codigos_async()
        print(dados_ibge_result)

        print("Obtendo dados do IBGE via link...")
        dados_ibge_link_result = await dados_ibge_link_async()
        print(dados_ibge_link_result)

        print("Obtendo dados de expectativas Focus...")
        dados_expectativas_focus_result = await dados_expectativas_focus_async()
        print(dados_expectativas_focus_result)

        print("Obtendo dados do Ipeadata via async...")
        dados_ipeadata_async_result = await dados_ipeadata_async()
        print(dados_ipeadata_async_result)

        print("Obtendo dados do Google Trends...")
        # dados_google_trends_result = await coleta_google_trends_async()
        # print(dados_google_trends_result)

        end = time.time()
        print(f"Tempo de execução: {end - start} segundos")

    # Executa o loop de eventos
    asyncio.run(main())
