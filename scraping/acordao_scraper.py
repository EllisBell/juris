import scraper
from bs4 import BeautifulSoup
import html_prework as hp
import acordao as acordao

base_url = "http://www.dgsi.pt"


def get_page(url):
    content = scraper.try_get_page_content(url, 5, 0.2)
    return content


def gimme_rows(case_url):
    content = get_page(case_url)
    this_soup = get_soup(content)
    case_rows = this_soup.find_all('tr')
    return case_rows


def get_soup(html):
    # n.b. using lxml instead of html.parser as it deals with unclosed tags better
    # n.b. specifying encoding as encoding of some pages was not being detected correctly
    # TODO this could lead to problems if page is not windows-1252 encoded so write
    # TODO something that deals with this
    return BeautifulSoup(html, 'lxml', from_encoding='windows-1252')
    # return BeautifulSoup(html, 'lxml')
    # return BeautifulSoup(html, 'html.parser')


def get_row(rows, section_header):
    for row in rows:
        if row.td.get_text(strip=True) == section_header:
            return row


def get_content(row):
    if row is not None:
        return row.find_all('td')[1].get_text(strip=True)
    return ""


def get_html(row):
    if row is not None:
        return str(row.find_all('td')[1])


def get_list_content(row):
    list_cont = []
    if row is not None:
        col = row.find_all('td')[1]
        for string in col.strings:
            list_cont.append(string)

        # Get rid of whitespace elements and strip away whitespace from actual terms
        list_cont = [term.strip() for term in list_cont if not term.isspace()]

    return list_cont


# This may or may not be necessary as it seems html parsing replaces
# <br> with newlines anyway. Not sure, only seems to happen in some cases.
# Seems to work with paragraphs too
def get_text_with_newlines(row):
    html_text = get_html(row)
    if not html_text:
        return ""
    html_with_newlines = hp.replace_html_new_lines(html_text)
    newline_soup = get_soup(html_with_newlines)
    text_with_newlines = newline_soup.get_text(strip=False)
    return text_with_newlines


# TODO want no strip on newlines but strip whitespace at start of lines...
def get_text_no_strip(row):
    if row is not None:
        return row.find_all('td')[1].get_text()
    return ""


def prepare_html_for_saving(html_to_prepare):
    if not html_to_prepare:
        return ""

    if how_much_text_is_bold(html_to_prepare) > 0.95:
        html_to_prepare = hp.remove_bold(html_to_prepare)

    new_html = hp.remove_font_tags(html_to_prepare)
    new_html = hp.close_p_tags(new_html)
    new_html = hp.replace_bold(new_html)
    new_html = hp.replace_italics(new_html)
    new_html = hp.replace_s_tags(new_html)
    return new_html


def how_much_text_is_bold(html_to_check):
    if html_to_check:
        soup = get_soup(html_to_check)
        texts = soup.find_all(string=True)
        texts = [text for text in texts if text != '\n']
        if texts and len(texts) > 0:
            bold_count = 0
            for text in texts:
                if text.find_parents('b'):
                    bold_count += 1

            return bold_count / len(texts)
    return 0


def get_acordao(case_url, trib_id):
    full_case_url = base_url + case_url
    rows = gimme_rows(full_case_url)

    processo = get_content(get_row(rows, "Processo:"))
    # get seccao, num_convencional
    seccao = get_content(get_row(rows, "Secção:"))
    num_convencional = get_content(get_row(rows, "Nº Convencional:"))
    relator = get_content(get_row(rows, "Relator:"))
    descritores = get_list_content(get_row(rows, "Descritores:"))
    numero = get_content(get_row(rows, "Nº do Documento:"))
    
    data = get_content(get_row(rows, "Data do Acordão:"))
    # see e.g. proc 770/12.3TBSLX.L1.S1 (STJ)
    if not data:
        data = get_content(get_row(rows, "Data da Decisão Sumária:"))
    # see e.g. proc 44/1999-A.E2.S1 (STJ)
    if not data:
        data = get_content(get_row(rows, "Data da Reclamação:"))

    votacao = get_content(get_row(rows, "Votação:"))

    aditamento = get_content(get_row(rows, "Aditamento:"))

    trib_recurso = get_content(get_row(rows, "Tribunal Recurso:"))
    if not trib_recurso:
        trib_recurso = get_content(get_row(rows, "Tribunal Recorrido:"))
    proc_trib_recurso = get_content(get_row(rows, "Processo no Tribunal Recurso:"))
    if not proc_trib_recurso:
        proc_trib_recurso = get_content(get_row(rows, "Processo no Tribunal Recorrido:"))

    data_dec_recorrida = get_content(get_row(rows, "Data Dec. Recorrida:"))

    recorrente = get_content(get_row(rows, "Recorrente:"))
    # get multiple recorridos
    index = 1
    recorridos = []
    while True:
        recorrido = get_content(get_row(rows, "Recorrido " + str(index) + ":"))
        if not recorrido:
            break
        recorridos.append(recorrido)
        index += 1

    indic_eventuais = get_content(get_row(rows, "Indicações Eventuais:"))

    area_tematica = get_text_no_strip(get_row(rows, "Área Temática:"))
    doutrina = get_text_no_strip(get_row(rows, "Doutrina:"))
    legis_nac = get_text_no_strip(get_row(rows, "Legislação Nacional:"))
    juris_nac = get_text_no_strip(get_row(rows, "Jurisprudência Nacional:"))

    txt_integral_flag = get_content(get_row(rows, "Texto Integral:"))
    txt_parcial_flag = get_content(get_row(rows, "Texto Parcial:"))
    meio_processual = get_content(get_row(rows, "Meio Processual:"))
    decisao = get_content(get_row(rows, "Decisão:"))

    sumario = get_text_no_strip(get_row(rows, "Sumário:"))
    # For STJ, Sumario field seems to have space between Sumário and colon
    if not sumario:
        sumario = get_text_no_strip(get_row(rows, "Sumário :"))

    dec_texto_parcial = get_text_no_strip(get_row(rows, "Decisão Texto Parcial:"))

    dec_texto_integral = get_text_no_strip(get_row(rows, "Decisão Texto Integral:"))

    # now get html but only if there is actually text there, not just empty tags
    html_parcial_for_saving = ''
    if dec_texto_parcial:
        html_parcial_for_saving = prepare_html_for_saving(get_html(get_row(rows, "Decisão Texto Parcial:")))
    html_integral_for_saving = ''
    if dec_texto_integral:
        html_integral_for_saving = prepare_html_for_saving(get_html(get_row(rows, "Decisão Texto Integral:")))

    ac = acordao.Acordao(processo, trib_id, seccao, num_convencional,
                         relator, descritores, numero, data, votacao, aditamento, trib_recurso,
                         proc_trib_recurso, data_dec_recorrida, txt_integral_flag, txt_parcial_flag, meio_processual,
                         recorrente, recorridos, decisao, indic_eventuais, area_tematica, doutrina, legis_nac,
                         juris_nac, sumario, dec_texto_parcial, html_parcial_for_saving, dec_texto_integral,
                         html_integral_for_saving, case_url)
    return ac


def check_source_not_found(acordao_url):
    return scraper.check_page_not_found(base_url + acordao_url)

if __name__ == "__main__":
    print("hello world")
    get_acordao("/jtrl.nsf/33182fc732316039802565fa00497eec/dfd77f12a75d13f2802581c80058e338?OpenDocument", "TRL")
