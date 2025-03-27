# pylint: disable=redefined-outer-name
import pytest
import pandas as pd
from brazilian_data import EconomicDataAsync


@pytest.fixture
def economic_data_fixture() -> EconomicDataAsync:
    """Fixture para criar uma instância de EconomicDataAsync para testes"""
    return EconomicDataAsync()


@pytest.fixture
def bcb_codes_fixture() -> dict:
    """Fixture com códigos de exemplo do Banco Central"""
    return {"selic": 4189, "cambio": 3698}


@pytest.fixture
def ibge_codes_fixture() -> dict:
    """Fixture com códigos de exemplo do IBGE"""
    return {
        "ipca": {
            "codigo": 1737,
            "territorial_level": "1",
            "ibge_territorial_code": "all",
            "variable": "63",
        }
    }


@pytest.mark.asyncio
async def test_data_index(economic_data_fixture: EconomicDataAsync) -> None:
    """Testa a geração do índice de datas"""
    df = economic_data_fixture.data_index()
    assert isinstance(df, pd.DataFrame)
    assert len(df.index) > 0
    # Verifica se o índice é do tipo datetime
    assert isinstance(df.index, pd.DatetimeIndex)


@pytest.mark.asyncio
async def test_datas_banco_central(
    economic_data_fixture: EconomicDataAsync, bcb_codes_fixture: dict
) -> None:
    """Testa a coleta de dados do Banco Central"""
    economic_data_fixture.codes_banco_central = bcb_codes_fixture
    df = await economic_data_fixture.datas_banco_central()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "selic" in df.columns
    assert "cambio" in df.columns


@pytest.mark.asyncio
async def test_datas_ibge(
    economic_data_fixture: EconomicDataAsync, ibge_codes_fixture: dict
) -> None:
    """Testa a coleta de dados do IBGE"""
    economic_data_fixture.codes_ibge = ibge_codes_fixture
    df = await economic_data_fixture.datas_ibge()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


@pytest.mark.asyncio
async def test_datas_brazil_integration(
    economic_data_fixture: EconomicDataAsync,
) -> None:
    """Teste de integração para datas_brazil"""
    df = await economic_data_fixture.datas_brazil(
        datas_bcb=True,
        datas_ibge_codigos=True,
        datas_expectativas_inflacao=True,
        datas_ibge_link=True,
        datas_ipeadata=True,
        datas_fred=False,
    )
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
