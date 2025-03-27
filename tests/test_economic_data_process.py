from brazilian_data.economic_data_process import (
    tratando_dados_expectativas,
    tratando_dados_ibge_codigos,
    tratando_dados_ibge_link,
    tratatando_dados_ipeadata,
    tratando_dados_ibge_link_producao_agricola,
)
import pandas as pd


# write tests for tratando_dados_bcb,
# pylint: disable=W0105

"""def test_tratando_dados_bcb_datetime():
    dados = tratando_dados_bcb({"selic": 4189}, "2000-01-01")
    assert isinstance(dados.index, pd.DatetimeIndex)
"""
# pylint: disable=W0105

# pylint: disable=W0105
"""def test_tratando_dados_bcb_columns():
    dados = tratando_dados_bcb({"selic": 4189}, "2000-01-01")
    assert "selic" in dados.columns"""
# pylint: disable=W0105


# write tests for tratando_dados_expectativas
def test_tratando_dados_expectativas() -> None:
    dados = tratando_dados_expectativas()
    assert isinstance(dados.index, pd.DatetimeIndex)


# write tests for tratando_dados_ibge_codigos
def test_tratando_dados_ibge_codigos_time() -> None:
    dados = tratando_dados_ibge_codigos()
    assert isinstance(dados.index, pd.DatetimeIndex)


def test_tratando_dados_ibge_codigos_columns() -> None:
    dados = tratando_dados_ibge_codigos()
    assert "Valor" in dados.columns


# write tests for tratando_dados_ibge_link
def test_tratando_dados_ibge_link() -> None:
    dados = tratando_dados_ibge_link(
        coluna="pib",
        link="https://sidra.ibge.gov.br/geratabela?format=xlsx&name=tabela5932.xlsx&terr=N&rank=-&query=t/5932/n1/all/v/6561/p/all/c11255/90707/d/v6561%201/l/v,p%2Bc11255,t",
    )
    assert isinstance(dados.index, pd.DatetimeIndex)


def test_tratando_dados_ibge_link_columns() -> None:
    dados = tratando_dados_ibge_link(
        coluna="pib",
        link="https://sidra.ibge.gov.br/geratabela?format=xlsx&name=tabela5932.xlsx&terr=N&rank=-&query=t/5932/n1/all/v/6561/p/all/c11255/90707/d/v6561%201/l/v,p%2Bc11255,t",
    )
    assert "pib" in dados.columns


def test_tratando_dados_ibge_link_producao_agricola() -> None:
    dados = tratando_dados_ibge_link_producao_agricola(
        url="https://sidra.ibge.gov.br/geratabela?format=xlsx&name=tabela6588.xlsx&terr=N&rank=-&query=t/6588/n1/all/v/35/p/all/c48/0,39443/l/v,p%2Bc48,t",
        nome_coluna="soja",
    )
    assert isinstance(dados.index, pd.DatetimeIndex)
    assert "soja" in dados.columns
    assert isinstance(dados, pd.DataFrame)


def test_tratatando_dados_ipeadata() -> None:
    codigo_ipea = {"taja_juros_ltn": "ANBIMA12_TJTLN1212"}
    dados = tratatando_dados_ipeadata(codigo_ipeadata=codigo_ipea, data="2000-01-01")
    assert isinstance(dados.index, pd.DatetimeIndex)
    assert not dados.empty
