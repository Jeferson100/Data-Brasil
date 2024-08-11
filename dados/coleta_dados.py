import sys
sys.path.append('..')
from brazilian_data import EconomicData
#from economic_brazil.coleta_dados.tratando_economic_brazil import tratando_dados_bcb, tratando_dados_ibge_link, tratando_metas_inflacao, tratando_dados_expectativas, tratando_dados_ibge_codigos
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

banco_central_codes = {
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
    'estoque_caged': 28763,
    'saldo_bc': 22707,
    'vendas_auto':7384,
    'divida_liquida_spc':4513,  
    "indice_condicoes_economicas": 4394,
    "indice_valores_garantias_imoveis_residencias_financiados": 21340,
    "venda_veiculos_concessionarias": 1378,
    "indicador_movimento_comercio_prazo": 1453,
    "indice_volume_vendas_varejo": 1455,
    "imposto_sobre_produtos": 22098,
    'metas_inflacao': 13521,
    'indice_expectativas_futuras': 4395,
    'indice_confianca_empresarial_industrial': 7343,
    'selic': 4189,
    'ibc':24364
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
    "producao_fisica_industrial": {
        "codigo": '8159',
        "territorial_level": "1",
        "ibge_territorial_code": "all",
        "variable": "11599",},

    "producao_fisica_para_construcao_civil": {
        "codigo": '7980',
        "territorial_level": "1",
        "ibge_territorial_code": "all",
        "variable": "11599",},
    
    "producao_soja_milho": {    
        "codigo": '6588',
        "territorial_level": "1",
        "ibge_territorial_code": "all",
        "variable": "35",},
    
    "precos_construcao_civil": {
        "codigo": '2296',
        "territorial_level": "1",
        "ibge_territorial_code": "all",
        "variable": "1198",},
    "volume_servicos_(pms)": {
        "codigo": '8162',
        "territorial_level": "1",
        "ibge_territorial_code": "all",
        "variable": "11621",
        
    }, 
    
    "taxa_desocupacao": { 
        "codigo": '6381',
        "territorial_level": "1",
        "ibge_territorial_code": "all",
        "variable": "4099",
            
            }
}

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
    'producao_industrial': 'PAN12_QIIGG12',
    'producao_industrial_intermediario': 'PIMPFN12_QIBIN12',
    'capcidade_instalada': 'CNI12_NUCAP12',
    'caixas_papelao': 'ABPO12_PAPEL12',
    'faturamento_industrial': 'CNI12_VENREA12',
    'importacoes_industrial': 'FUNCEX12_MDQT12',
    'importacoes_intermediario': 'FUNCEX12_MDQBIGCE12',
    'confianca_empresario_exportador': 'CNI12_ICEIEXP12',
    'confianca_empresario_atual': 'CNI12_ICEICA12',
    'confianca_consumidor':'FCESP12_IIC12',
    'ettj_26': 'ANBIMA366_TJTLN6366',  
}

indicadores_ibge_link_padrao = {
    "pib": "https://sidra.ibge.gov.br/geratabela?format=xlsx&name=tabela5932.xlsx&terr=N&rank=-&query=t/5932/n1/all/v/6564/p/all/c11255/90707/d/v6564%201/l/v,p,t%2Bc11255&verUFs=false&verComplementos2=false&verComplementos1=false&omitirIndentacao=false&abreviarRotulos=false&exibirNotas=false&agruparNoCabecalho=false",
    "despesas_publica": "https://sidra.ibge.gov.br/geratabela?format=xlsx&name=tabela5932.xlsx&terr=N&rank=-&query=t/5932/n1/all/v/6561/p/all/c11255/93405/d/v6561%201/l/v,p%2Bc11255,t",
    "capital_fixo": "https://sidra.ibge.gov.br/geratabela?format=xlsx&name=tabela5932.xlsx&terr=N&rank=-&query=t/5932/n1/all/v/6561/p/all/c11255/93406/d/v6561%201/l/v,p%2Bc11255,t",
    "producao_industrial_manufatureira": "https://sidra.ibge.gov.br/geratabela?format=xlsx&name=tabela8158.xlsx&terr=N&rank=-&query=t/8158/n1/all/v/11599/p/all/c543/129278/d/v11599%205/l/v,p%2Bc543,t",
    "soja": "https://sidra.ibge.gov.br/geratabela?format=xlsx&name=tabela6588.xlsx&terr=N&rank=-&query=t/6588/n1/all/v/35/p/all/c48/0,39443/l/v,p%2Bc48,t",
    "milho_1": "https://sidra.ibge.gov.br/geratabela?format=xlsx&name=tabela6588.xlsx&terr=N&rank=-&query=t/6588/n1/all/v/35/p/all/c48/0,39441/l/v,p%2Bc48,t",
    "milho_2": "https://sidra.ibge.gov.br/geratabela?format=xlsx&name=tabela6588.xlsx&terr=N&rank=-&query=t/6588/n1/all/v/35/p/all/c48/0,39442/l/v,p%2Bc48,t",
    'pms': 'https://sidra.ibge.gov.br/geratabela?format=xlsx&name=tabela8162.xlsx&terr=N&rank=-&query=t/8162/n1/all/v/11622/p/all/c11046/56726/c12355/107071/d/v11622%205/l/v,p%2Bc11046,t%2Bc12355'
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

data_bcb = True
data_ibge = True
data_ibge_link = True
data_ipeadata = True
data_fred = True


DATA_INICIO = "2000-01-01"

economic_brazil = EconomicData(codes_banco_central=banco_central_codes, 
                                 codes_ibge=variaveis_ibge_padrao, 
                                 codes_ipeadata=codigos_ipeadata_padrao , 
                                 codes_ibge_link=indicadores_ibge_link_padrao,
                                 codes_fred=codigos_fred_padrao,
                                 start_date=DATA_INICIO)

economic_brazil.datas_brazil(
                                     save=True,
                                     directory="economicos_brazil",
                                     data_format='pickle')


print('Coletando dados Brazil')

economic_brazil.datas_banco_central(save=True, directory="economicos_banco_central", data_format='pickle')

print('Coletando dados IBGE')

economic_brazil.datas_ibge(save=True, directory="economicos_ibge", data_format='pickle')

print('Coletando dados IBGE Link')

economic_brazil.datas_ibge_link(save=True, directory="economicos_ibge_link", data_format='pickle')

print('Coletando dados IPEADATA')

economic_brazil.datas_fred(save=True, directory="economicos_fred", data_format='pickle')

print('Coletando dados FRED')

