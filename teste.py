from brazilian_data import EconomicData
DATA_INICIO = "2010-01-01"

variaveis_banco_central= {
    "selic": 4189,
    "cambio": 3698,
    "pib_mensal": 4380,
    "igp_m": 189,
    "igp_di": 190,
    "m1": 27788,
}

economic_brazil = EconomicData(codes_banco_central=variaveis_banco_central, 
                                start_date=DATA_INICIO)

dados = economic_brazil.datas_banco_central()

print(dados.head())