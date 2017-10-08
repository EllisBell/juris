import psycopg2 as ppg


class Acordao(object):
    def __init__(self, processo, tribunal, seccao, num_convencional, relator, descritores, numero, data, votacao,
                 aditamento, trib_recurso, proc_trib_recurso, texto_integral_flag, texto_parcial_flag, meio_processual,
                 recorrente, recorridos, decisao, indic_eventuais, area_tematica, doutrina, legis_nacional,
                 juris_nacional, sumario, dec_texto_parcial, dec_texto_integral, html_texto_integral, url):
        self.processo = processo
        self.tribunal = tribunal
        self.seccao = seccao
        self.num_convencional = num_convencional
        self.relator = relator
        self.descritores = descritores
        self.numero = numero
        self.data = data
        self.votacao = votacao
        self.aditamento = aditamento
        self.trib_recurso = trib_recurso
        self.proc_trib_recurso = proc_trib_recurso
        self.texto_integral_flag = texto_integral_flag
        self.texto_parcial_flag = texto_parcial_flag
        self.meio_processual = meio_processual
        self.recorrente = recorrente
        self.recorridos = recorridos
        self.decisao = decisao
        self.indic_eventuais = indic_eventuais
        # single string but should add new lines for break tags
        self.area_tematica = area_tematica
        # same as above for dout, legis and juris
        self.doutrina = doutrina
        self.legis_nacional = legis_nacional
        self.juris_nacional = juris_nacional
        self.sumario = sumario
        self.dec_texto_parcial = dec_texto_parcial
        self.dec_texto_integral = dec_texto_integral
        self.html_texto_integral = html_texto_integral
        self.url = url
