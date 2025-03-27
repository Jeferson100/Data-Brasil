import pytest
from unittest.mock import patch, mock_open
import pandas as pd
from brazilian_data.economic_data import EconomicData


# pylint: disable=W0621
@pytest.fixture
def econ_brazil() -> EconomicData:
    # dados_economicos = EconomicBrazil()
    return EconomicData()


# pylint: disable=W0621
def test_datas_banco_central(econ_brazil: EconomicData) -> None:
    # dados_economicos = EconomicBrazil()
    dados = econ_brazil.datas_banco_central()
    assert isinstance(dados.index, pd.DatetimeIndex)
    assert isinstance(dados, pd.DataFrame)


def test_datas_ibge(econ_brazil: EconomicData) -> None:
    dados = econ_brazil.datas_ibge()
    assert isinstance(dados.index, pd.DatetimeIndex)
    assert isinstance(dados, pd.DataFrame)


def test_datas_ibge_link(econ_brazil: EconomicData) -> None:
    dados = econ_brazil.datas_ibge_link()
    assert isinstance(dados.index, pd.DatetimeIndex)
    assert isinstance(dados, pd.DataFrame)


def test_datas_ipeadata(econ_brazil: EconomicData) -> None:
    dados = econ_brazil.datas_ipeadata()
    assert isinstance(dados.index, pd.DatetimeIndex)
    assert isinstance(dados, pd.DataFrame)


def test_datas_fred(econ_brazil: EconomicData) -> None:
    dados = econ_brazil.datas_fred()
    assert isinstance(dados.index, pd.DatetimeIndex)
    assert isinstance(dados, pd.DataFrame)


def test_datas_brazil(econ_brazil: EconomicData) -> None:
    dados = econ_brazil.datas_brazil()
    assert dados.notnull().all().all()
    assert isinstance(dados.index, pd.DatetimeIndex)
    assert isinstance(dados, pd.DataFrame)


def test_salvar_dados(econ_brazil: EconomicData) -> None:
    dados = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    with patch("builtins.open", mock_open()) as mocked_file:
        econ_brazil.save_datas(dados, diretory="test_file", data_format="pickle")
        mocked_file.assert_called_with("test_file.pkl", "wb")
