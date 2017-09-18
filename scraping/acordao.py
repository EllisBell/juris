import psycopg2 as ppg


class Acordao(object):
    def __init__(self, processo, relator, descritores, numero, data, votacao, texto_integral_flag, texto_parcial_flag,
                 meio_processual, decisao, sumario, dec_texto_parcial, dec_texto_integral, html_texto_integral):
        self.processo = processo
        self.relator = relator
        self.descritores = descritores
        self.numero = numero
        self.data = data
        self.votacao = votacao
        self.texto_integral_flag = texto_integral_flag
        self.texto_parcial_flag = texto_parcial_flag
        self.meio_processual = meio_processual
        self.decisao = decisao
        self.sumario = sumario
        self.dec_texto_parcial = dec_texto_parcial
        self.dec_texto_integral = dec_texto_integral
