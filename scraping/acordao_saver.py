import psycopg2 as ppg


# have function for checking whether acordao already in db before saving
def check_exists(processo, data):
    # query db to check if acordao with this processo and date already saved
    return False;

# TODO need to give this the tribunal to which it pertains (e.g. pass in tribunal id)
def save(acordao):
    # connect to db. do this somewhere else
    conn = ppg.connect("dbname=jurisdb user=jurisuser password=intenserecovery")
    cur = conn.cursor()

    sql = """INSERT INTO acordao(processo, tribunal_id, relator, numero, data, votacao, txt_integral_flag, 
             txt_parcial_flag, meio_processual, decisao, sumario, txt_parcial, txt_integral, html_txt_integral)
			 VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id"""

    cur.execute(sql, (
        acordao.processo, acordao.relator, acordao.numero, acordao.data, acordao.votacao, acordao.texto_integral_flag,
        acordao.texto_parcial_flag,
        acordao.meio_processual, acordao.decisao, acordao.sumario, acordao.dec_texto_parcial,
        acordao.dec_texto_integral, acordao.html_texto_integral))

    # since we included "RETURING id" in insert stmt, we can get the id from result
    acordao_id = cur.fetchone()[0]

    for desc in acordao.descritores:
        desc_sql = """INSERT INTO acordao_descritor(acordao_id, descritor)
		VALUES(%s, %s)"""

        cur.execute(desc_sql, (acordao_id, desc))

    for rec in acordao.recorridos:
        rec_sql = """INSERT INTO acordao_reccorido(acordao_id, recorrido)
         VALUES(%s, %s)"""

        cur.execute(rec_sql, (acordao_id, rec))

    conn.commit()
    conn.close()
