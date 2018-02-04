import psycopg2 as ppg
import datetime


# Should I be using something like sqlalchemy (providing a layer of abstraction/ORM) rather than pyscopg2 directly?
# Would this make sense given this may or may not tie in with django
# If not should I have a simple db abstraction class anyway?
# tbh since this is just for scraping and Django will handle interacting between app and db, probs not necessary
class AcordaoSaver(object):
    def __init__(self):
        # TODO review when to connect, close etc... pooled connections?
        self.conn = ppg.connect("dbname=jurisdb user=jurisuser password=intenserecovery")

    # have function for checking whether acordao already in db before saving
    def check_exists(self, processo, data):
        # query db to check if acordao with this processo and date already saved
        return False

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
        cur = self.conn.cursor()

        sql = """INSERT INTO acordao(processo, tribunal_id, relator, numero, data, votacao, txt_integral_flag, 
                 txt_parcial_flag, meio_processual, decisao, sumario, txt_parcial, html_txt_parcial, 
                 txt_integral, html_txt_integral, url, date_loaded)
                 VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING acordao_id"""

        cur.execute(sql, (
            acordao.processo, acordao.tribunal, acordao.relator, acordao.numero, acordao.data, acordao.votacao,
            acordao.texto_integral_flag,
            acordao.texto_parcial_flag,
            acordao.meio_processual, acordao.decisao, acordao.sumario, acordao.dec_texto_parcial,
            acordao.html_txt_parcial, acordao.dec_texto_integral, acordao.html_texto_integral,
            acordao.url, datetime.datetime.now().date()))

        # since we included "RETURNING id" in insert stmt, we can get the id from result
        acordao_id = cur.fetchone()[0]

        for desc in acordao.descritores:
            desc_sql = """INSERT INTO acordao_descritor(acordao_id, descritor)
            VALUES(%s, %s)"""

            cur.execute(desc_sql, (acordao_id, desc))

        for rec in acordao.recorridos:
            rec_sql = """INSERT INTO acordao_reccorido(acordao_id, recorrido)
             VALUES(%s, %s)"""

            cur.execute(rec_sql, (acordao_id, rec))

        self.conn.commit()

    def close_connection(self):
        self.conn.close()
