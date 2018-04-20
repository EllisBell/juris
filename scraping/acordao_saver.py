import psycopg2 as ppg
import datetime
from datetime import timedelta
import os


# Should I be using something like sqlalchemy (providing a layer of abstraction/ORM) rather than pyscopg2 directly?
# Would this make sense given this may or may not tie in with django
# If not should I have a simple db abstraction class anyway?
# tbh since this is just for scraping and Django will handle interacting between app and db, probs not necessary
class AcordaoSaver(object):
    def __init__(self):
        # TODO review when to connect, close etc... pooled connections?
        password = os.environ.get('JURIS_DB_PW', '')
        self.conn = ppg.connect("host=localhost dbname=jurisdb user=jurisuser password=" + password)

    def get_currently_saved(self, trib_id):
        # query db to get urls of all currently saved acordaos
        cur = self.conn.cursor()
        sql = "select url from acordao where tribunal_id = %s;"
        cur.execute(sql, (trib_id,))
        results = cur.fetchall()
        url_list = [result[0] for result in results]
        # return set to make checking if in here faster
        return set(url_list)

    # TODO need to give this the tribunal to which it pertains (e.g. pass in tribunal id)
    def save(self, acordao):
        # prepare descritores for saving
        desc_string = "|".join(acordao.descritores)

        cur = self.conn.cursor()

        sql = """INSERT INTO acordao(processo, tribunal_id, relator, numero, data, votacao, txt_integral_flag, 
                 txt_parcial_flag, meio_processual, decisao, sumario, txt_parcial, html_txt_parcial, 
                 txt_integral, html_txt_integral, url, date_loaded, descritores)
                 VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING acordao_id"""

        cur.execute(sql, (
            acordao.processo, acordao.tribunal, acordao.relator, acordao.numero, acordao.data, acordao.votacao,
            acordao.texto_integral_flag,
            acordao.texto_parcial_flag,
            acordao.meio_processual, acordao.decisao, acordao.sumario, acordao.dec_texto_parcial,
            acordao.html_txt_parcial, acordao.dec_texto_integral, acordao.html_texto_integral,
            acordao.url, datetime.datetime.now(), desc_string))

        # since we included "RETURNING id" in insert stmt, we can get the id from result
        acordao_id = cur.fetchone()[0]

        for rec in acordao.recorridos:
            rec_sql = """INSERT INTO acordao_reccorido(acordao_id, recorrido)
             VALUES(%s, %s)"""

            cur.execute(rec_sql, (acordao_id, rec))

        self.conn.commit()

    # TODO Fix
    def get_saved_since(self, hours_ago):
        cur = self.conn.cursor()
        sql = """select tribunal_id, count(*) from acordao 
        where date_loaded > %s 
        group by tribunal_id"""
        cur.execute(sql, (datetime.datetime.now() - timedelta(hours=hours_ago),))
        results = cur.fetchall()
        return results

    # Sometimes there is more than one acordao with same processo number
    # Sometimes this is legitimate, they are different acordaos under same processo
    # Other times there was a revision or something so the acordao was reposted, and the
    # previous one was deleted. We want to get rid of the deleted urls so here we get
    # all duplicate processos to check if their urls still exist
    def get_duplicate_processos(self):
        cur = self.conn.cursor()
        # Get the duplicate processo urls
        sql = """select url from acordao where processo in 
        (select processo from acordao
        group by processo 
        having count(*) > 1)
        order by data desc"""
        cur.execute(sql)
        results = cur.fetchall()
        url_list = [result[0] for result in results]
        return url_list

    def delete_acordao_by_url(self, acordao_url):
        cur = self.conn.cursor()
        sql = """delete from acordao
        where url = %s"""
        cur.execute(sql, (acordao_url,))
        self.conn.commit()

    def close_connection(self):
        self.conn.close()


