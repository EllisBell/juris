import psycopg2 as ppg


def save(acordao):
    # connect to db. do this somewhere else
    conn = ppg.connect("dbname=jurisdb user=jurisuser password=intenserecovery")
    cur = conn.cursor()

    sql = """INSERT INTO acordao(processo, relator, numero, data, votacao, txt_integral_flag, txt_parcial_flag,
			 meio_processual, decisao, sumario, txt_parcial, txt_integral)
			 VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id"""

    cur.execute(sql, (
        acordao.processo, acordao.relator, acordao.numero, acordao.data, acordao.votacao, acordao.texto_integral_flag,
        acordao.texto_parcial_flag,
        acordao.meio_processual, acordao.decisao, acordao.sumario, acordao.dec_texto_parcial,
        acordao.dec_texto_integral))

    acordao_id = cur.fetchone()[0]

    for desc in acordao.descritores:
        desc_sql = """INSERT INTO acordao_descritor(acordao_id, descritor)
		VALUES(%s, %s)"""

        cur.execute(desc_sql, (acordao_id, desc))

    conn.commit()
    conn.close()
