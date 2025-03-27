import pandas as pd
from bcb import sgs
import sidrapy
from bcb import Expectativas
import ipeadatapy as ip
import time
from typing import Dict, Optional, cast
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
    dados_link: pd.DataFrame = await asyncio.to_thread(
        pd.read_excel, url, header=cabecalho
    )
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
    def get_ipca_expec() -> pd.DataFrame:
        resultado = (
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
        return cast(pd.DataFrame, resultado)

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


if __name__ == "__main__":

    async def main() -> None:
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

        end = time.time()
        print(f"Tempo de execução: {end - start} segundos")

    # Executa o loop de eventos
    asyncio.run(main())
