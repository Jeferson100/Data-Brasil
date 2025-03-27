from .economic_data_collection import (
    dados_bcb,
    dados_ibge_link,
    dados_ibge_codigos,
    dados_expectativas_focus,
    dados_ipeadata,
)
import pandas as pd
import numpy as np
from datetime import datetime
import requests
from io import BytesIO
from typing import Optional, Dict, Any


# Tratando dados IBGE/SIDRAPY
def trimestral_para_mensal(df: pd.DataFrame) -> pd.DataFrame:
    """
    A função recebe um DataFrame df com valores trimestrais do PIB. Primeiro, ela aplica a interpolação para obter os valores mensais, usando o método resample com uma frequência de 'M' e o método interpolate para preencher os valores faltantes.
    Em seguida, ela percorre os valores de cada trimestre e distribui a variação trimestral em cada um dos três meses dentro do trimestre, adicionando um terço do valor trimestral aos dois meses intermediários. Finalmente, ela retorna o DataFrame
    interpolado e transformado em mensal.
    """

    # Primeiro, definimos uma nova frequência mensal e aplicamos a interpolação
    df_mensal = df.resample("MS").interpolate()

    # Em seguida, distribuímos a variação trimestral em cada um dos três meses dentro do trimestre
    for i in range(1, len(df)):
        if i % 3 != 0:
            val = df.iloc[i].values[0]
            month_val = val / 3
            df_mensal.iloc[i * 2 - 1] += month_val
            df_mensal.iloc[i * 2] += month_val

    return df_mensal


def converter_mes_para_data(mes: int) -> datetime:
    mes_texto = str(mes)
    ano = int(mes_texto[:4])
    mes = int(mes_texto[4:])
    data = datetime(year=ano, month=mes, day=1)
    return data


def trimestre_string_int(dados: pd.DataFrame) -> list:
    lista_trimestre = []
    for i in range(len(dados.index)):
        trimestre_str = str(dados.index[i][0])
        trimestre_int = int(trimestre_str)
        if trimestre_int * 3 == 12:
            lista_trimestre.append(dados.index[i][-4:] + "-" + str(trimestre_int * 3))
        else:
            lista_trimestre.append(
                dados.index[i][-4:] + "-" + "0" + str(trimestre_int * 3)
            )
    return lista_trimestre


def transforma_para_mes_incial_trimestre(dados: pd.DataFrame) -> list:
    lista_mes = []
    for i in range(len(dados.index)):
        trimestre = dados.index.month[i]  # type:ignore
        ano = str(dados.index.year[i])  # type:ignore
        lista_mes.append(
            str(
                np.where(
                    trimestre == 1,
                    ano + "-" + "0" + str(trimestre),
                    np.where(
                        trimestre == 2,
                        ano + "-" + "0" + str(trimestre + 2),
                        np.where(
                            trimestre == 3,
                            ano + "-" + "0" + str(trimestre + 4),
                            np.where(trimestre == 4, ano + "-" + str(trimestre + 6), 0),
                        ),
                    ),
                )
            )
        )
    return lista_mes


def transforme_data(data: pd.DataFrame) -> pd.DataFrame:
    months = {
        "janeiro": "january",
        "fevereiro": "february",
        "março": "march",
        "abril": "april",
        "maio": "may",
        "junho": "june",
        "julho": "july",
        "agosto": "august",
        "setembro": "september",
        "outubro": "october",
        "novembro": "november",
        "dezembro": "december",
    }

    lista_data = []
    for dat in data.index:
        date_components = dat.split(" ")
        formatted_month = months[date_components[0].lower()].capitalize()
        formatted_date = f"{formatted_month} {date_components[1]}"
        date_object = datetime.strptime(formatted_date, "%B %Y")
        lista_data.append(date_object.strftime("%Y-%m-%d"))
    data.index = lista_data  # type:ignore
    return data


###Tratando dados IBGE
def tratando_dados_ibge_codigos(
    codigos: Optional[Dict[str, Any]] = None,
    period: str = "all",
    salvar: bool = False,
    formato: str = "csv",
    diretorio: Optional[str] = None,
) -> pd.DataFrame:
    if codigos is None:
        ibge_codigos = dados_ibge_codigos(period="all")
    else:
        ibge_codigos = dados_ibge_codigos(**codigos, period=period)
    # Verificar se o DataFrame não está vazio
    if ibge_codigos.empty:
        raise ValueError("O DataFrame está vazio. Verifique os códigos fornecidos.")
    ibge_codigos.columns = ibge_codigos.iloc[0, :]
    ibge_codigos = ibge_codigos.iloc[1:, :]
    if ibge_codigos.columns.str.contains("Trimestre Móvel").any():
        ibge_codigos["data"] = ibge_codigos["Trimestre Móvel (Código)"].apply(
            converter_mes_para_data
        )
    else:
        ibge_codigos["data"] = ibge_codigos["Mês (Código)"].apply(
            converter_mes_para_data
        )
    ibge_codigos.index = ibge_codigos["data"]  # type:ignore
    try:
        ibge_codigos["Valor"] = ibge_codigos["Valor"][1:].astype(float)
    except ValueError as exc:
        ibge_codigos["Valor"] = pd.to_numeric(ibge_codigos["Valor"], errors="coerce")
        primeiro_valido_index = ibge_codigos["Valor"].first_valid_index()
        if primeiro_valido_index is None:
            # pylint: disable=W0622
            raise ValueError(
                f'Não há valores válidos para a variável {ibge_codigos["Variável"][0]}. Verifique se os códigos {codigos} estão ativos em https://sidra.ibge.gov.br/home/pms/brasil.'
            ) from exc
            # pylint: disable=W0622
        else:
            ibge_codigos = ibge_codigos.loc[primeiro_valido_index:]
            ibge_codigos["Valor"] = ibge_codigos["Valor"][1:].astype(float)
            print(
                f'Valores validos apartir de {primeiro_valido_index} para a variável {ibge_codigos["Variável"][0]}'
            )
    # ibge_codigos = ibge_codigos[ibge_codigos.index > primeiro_valido_index]
    if salvar:
        if diretorio is None:
            print("Diretório não especificado para salvar o arquivo")
        if formato == "csv":
            ibge_codigos.to_csv(diretorio)
        elif formato == "json":
            ibge_codigos.to_json(diretorio)
    return ibge_codigos


def tratando_dados_ibge_link(
    coluna: Optional[str] = None,
    link: str = "https://sidra.ibge.gov.br/geratabela?format=xlsx&name=tabela5932.xlsx&terr=N&rank=-&query=t/5932/n1/all/v/6561/p/all/c11255/93405/d/v6561%201/l/v,p%2Bc11255,t",
    salvar: bool = False,
    formato: str = "csv",
    diretorio: Optional[str] = None,
) -> pd.DataFrame:
    dado_ibge = dados_ibge_link(url=link)
    ibge_link = pd.DataFrame(dado_ibge.T)
    ibge_link = pd.DataFrame(ibge_link[[1]])
    ibge_link = pd.DataFrame(ibge_link[3:])
    ibge_link.columns = [coluna]
    ibge_link[coluna] = pd.to_numeric(ibge_link[coluna], errors="coerce")

    if ibge_link.index.str.contains("trimestre").any():
        ibge_link.index = pd.to_datetime(trimestre_string_int(ibge_link))

        ibge_link = ibge_link.resample("MS").ffill()

    else:
        ibge_link = transforme_data(ibge_link)
        ibge_link.index = pd.to_datetime(ibge_link.index)

    if salvar:
        if diretorio is None:
            raise ValueError("Diretório não especificado para salvar o arquivo")
        if formato == "csv":
            ibge_link.to_csv(diretorio)
        elif formato == "json":
            ibge_link.to_json(diretorio)

    return ibge_link


###Tratando dados BCB

selic = {
    "selic": 4189,
}


def tratando_dados_bcb(
    codigo_bcb_tratado: Optional[Dict[str, int]] = None,
    data_inicio_tratada: str = "2000-01-01",
    salvar: bool = False,
    diretorio: Optional[str] = None,
    formato: str = "csv",
    **kwargs,
) -> pd.DataFrame:
    if codigo_bcb_tratado is None:
        codigo_bcb_tratado = selic
    if not isinstance(codigo_bcb_tratado, dict):
        print("Código BCB deve ser um dicionário. Usando valor padrão.")
        codigo_bcb_tratado = selic
    inflacao_bcb = dados_bcb(codigo_bcb_tratado, data_inicio_tratada, **kwargs)
    if salvar:
        if diretorio is None:
            raise ValueError("Diretório não especificado para salvar o arquivo")
        if formato == "csv":
            inflacao_bcb.to_csv(diretorio)
        elif formato == "json":
            inflacao_bcb.to_json(diretorio)
    return inflacao_bcb


def tratando_dados_expectativas(
    salvar: bool = False, formato: str = "csv", diretorio: Optional[str] = None
) -> pd.DataFrame:
    ipca_expec = dados_expectativas_focus()
    dados_ipca = ipca_expec.copy()
    dados_ipca = dados_ipca[::-1]
    dados_ipca["monthyear"] = pd.to_datetime(dados_ipca["Data"]).apply(  # type:ignore
        lambda x: x.strftime("%Y-%m")  # type:ignore
    )  # type:ignore

    dados_ipca = dados_ipca.groupby("monthyear")["Mediana"].mean().to_frame()
    # criar índice com o formato "YYYY-MM"
    dados_ipca.index = pd.to_datetime(dados_ipca.index, format="%Y-%m", errors="coerce")

    # adicionar o dia como "01"
    dados_ipca.index = dados_ipca.index.to_period("M").to_timestamp()

    if salvar:
        if diretorio is None:
            raise ValueError("Diretório não especificado para salvar o arquivo")
        if formato == "csv":
            dados_ipca.to_csv(diretorio)
        elif formato == "json":
            dados_ipca.to_json(diretorio)

    return dados_ipca


def tratatando_dados_ipeadata(
    codigo_ipeadata: Dict[str, str], data: str = "2000-01-01"
) -> pd.DataFrame:
    ((nome_coluna, codigo),) = codigo_ipeadata.items()
    dados_ipea = dados_ipeadata(codigo=codigo, data=data)
    coluna = dados_ipea.filter(like="VALUE").columns[0]
    dados_ipea = dados_ipea[[coluna]]
    if isinstance(dados_ipea.index, pd.DatetimeIndex):
        if (dados_ipea.index.day == 1).all():  # type: ignore
            pass
        else:
            dados_ipea = dados_ipea.resample("MS").mean()
    else:
        print("Index is not a DatetimeIndex")
    try:
        dados_ipea = dados_ipea[dados_ipea.index >= pd.to_datetime(data)]
    except ValueError:
        print(
            f"Data inicial posterior a {data} definida, o conjunto de dados {codigo} tem data inicial em {dados_ipea.index[0]}"
        )
    if not isinstance(dados_ipea, pd.DataFrame):
        dados_ipea = pd.DataFrame(dados_ipea)
    dados_ipea.columns = [nome_coluna]
    return dados_ipea


def tratando_dados_ibge_link_producao_agricola(
    url: str, nome_coluna: str, header: int = 3
) -> pd.DataFrame:
    dados = pd.read_excel(url, header=header)
    dados = dados.T
    dados = dados.iloc[1:]
    dados = dados[[1]]
    data = pd.DataFrame()
    data = dados.iloc[::2, :]
    data.loc[:, nome_coluna] = dados[
        dados.index.str.contains("Unnamed")
    ].values.squeeze()
    data = transforme_data(data)
    data = data[[nome_coluna]]
    data.index = pd.to_datetime(data.index)
    data[nome_coluna] = pd.to_numeric(data[nome_coluna], errors="coerce")
    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)
    return data


def tratando_dados_ibge_link_colum_brazil(
    coluna: Optional[str] = None,
    link: str = "https://sidra.ibge.gov.br/geratabela?format=xlsx&name=tabela5932.xlsx&terr=N&rank=-&query=t/5932/n1/all/v/6561/p/all/c11255/93405/d/v6561%201/l/v,p%2Bc11255,t",
    salvar: bool = False,
    formato: str = "csv",
    diretorio: Optional[str] = None,
) -> pd.DataFrame:
    dado_ibge = dados_ibge_link(url=link)
    ibge_link = dado_ibge.T
    ibge_link.columns = ibge_link.iloc[0]
    ibge_link = pd.DataFrame(
        ibge_link[ibge_link.columns[ibge_link.columns.str.contains("Brasil", na=False)]]
    )
    ibge_link = pd.DataFrame(ibge_link[3:])
    ibge_link.columns = [coluna]
    ibge_link[coluna] = pd.to_numeric(ibge_link[coluna], errors="coerce")

    if ibge_link.index.str.contains("trimestre").any():
        ibge_link.index = pd.to_datetime(trimestre_string_int(ibge_link))

        # ibge_link.index = pd.to_datetime(
        # transforma_para_mes_incial_trimestre(ibge_link))
        ibge_link = ibge_link.resample("MS").ffill()

    else:
        ibge_link = transforme_data(ibge_link)
        ibge_link.index = pd.to_datetime(ibge_link.index)

    if salvar:
        if diretorio is None:
            raise ValueError("Diretório não especificado para salvar o arquivo")
        if formato == "csv":
            ibge_link.to_csv(diretorio)
        elif formato == "json":
            ibge_link.to_json(diretorio)

    return ibge_link


def read_indice_abcr() -> pd.DataFrame | None:
    url = "https://melhoresrodovias.org.br/wp-content/uploads/2024/06/abcr_0624.xls"

    # Cabeçalhos para simular um navegador
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code == 200:
        # Usar BytesIO para ler os dados binários
        data = BytesIO(response.content)
        try:
            df = pd.read_excel(data, sheet_name="(C) Original", header=2)
            df = df.iloc[:, :4]
            df.columns = ["data", "ibcr_leves", "ibcr_pesados", "ibcr_total"]
            df.index = df["data"]  # type:ignore
            df.drop("data", axis=1, inplace=True)
            return df
        except ValueError:
            print("Erro ao ler o arquivo Excel:")
    else:
        print(f"Erro ao acessar o recurso: {response.status_code} - {response.reason}")


def sondagem_industria(sheet: str, variable: str) -> pd.DataFrame:
    ##pagina para fazer web scraping
    url = "https://static.portaldaindustria.com.br/media/filer_public/62/24/6224e62d-7f5d-419d-ab6f-edd21e05cdf5/sondagemindustrial_serie-recente_maio2024.xls"

    response = requests.get(url, timeout=10)
    open("si.xls", "wb").write(response.content)
    df = pd.read_excel("si.xls", sheet_name=sheet, skiprows=7)
    df = df.iloc[0:1, 1:]
    df = pd.DataFrame(df.iloc[0, :])
    df.columns = [variable]
    lista = []
    for i in df.index:
        if isinstance(i, str):
            b = np.where(
                i[0:3] == "jan",
                "01",
                np.where(
                    i[0:3] == "fev",
                    "02",
                    np.where(
                        i[0:3] == "mar",
                        "03",
                        np.where(
                            i[0:3] == "abr",
                            "04",
                            np.where(
                                i[0:3] == "mai",
                                "05",
                                np.where(
                                    i[0:3] == "jun",
                                    "06",
                                    np.where(
                                        i[0:3] == "jul",
                                        "07",
                                        np.where(
                                            i[0:3] == "ago",
                                            "08",
                                            np.where(
                                                i[0:3] == "set",
                                                "09",
                                                np.where(
                                                    i[0:3] == "out",
                                                    "10",
                                                    np.where(
                                                        i[0:3] == "nov",
                                                        "11",
                                                        np.where(
                                                            i[0:3] == "dez",
                                                            "12",
                                                            i[0:3],
                                                        ),
                                                    ),
                                                ),
                                            ),
                                        ),
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
            )
            lista.append("20" + str(i)[3:5] + "-" + str(b) + "-01")
        else:
            lista.append(str(i))
    df["data"] = lista
    df["data"] = df["data"].str.replace("20t1", "2017")
    df.dropna(axis=0, inplace=True)
    df.index = pd.to_datetime(df["data"].str.split(" ").str[0].values)
    df.drop(columns="data", inplace=True)
    df[variable] = df[variable].astype(float)
    return df
