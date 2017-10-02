import requests
from bs4 import BeautifulSoup
import re
import html_prework as hp
import acordao as acordao

# TODOTODOTODO Index of row for each section is not always consistent between pages But if names of sections are
# consistent (and I think they are) - have method that finds the row based on the name of the section e.g. meio
# processual, relator etc.
# 

headers = {'User-Agent': 'Mozilla/5.0'}


def gimme_rows(case_url):
    r = requests.get(case_url, headers=headers)
    this_soup = get_soup(r.content)
    case_rows = this_soup.find_all('tr')
    return case_rows


def get_soup(html):
    return BeautifulSoup(html, 'html.parser')


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
    col = row.find_all('td')[1]
    for string in col.strings:
        list_cont.append(string)

    # Get rid of whitespace elements and strip away whitespace from actual terms
    list_cont = [term.strip() for term in list_cont if not term.isspace()]
    return list_cont


# save this html as txt integral html
def get_processed_html(row):
    col = row.find_all('td')[1]
    col_html = str(col)
    new_html = hp.remove_font_tags(col_html)
    new_html = hp.close_p_tags(new_html)
    new_html = hp.replace_bold(new_html)
    new_html = hp.replace_italics(new_html)
    return new_html


# # make soup from the new html
# txt_int_soup = BeautifulSoup(new_html, 'html.parser')

# paragraphs = txt_int_soup.find_all('p')
# #for para in paragraphs:
# #	print(repr(para.get_text(strip = True)))


# def get_multi_paragraph_content(row):

def prepare_html_for_saving(html_to_prepare):
    new_html = hp.remove_font_tags(html_to_prepare)
    new_html = hp.close_p_tags(new_html)
    new_html = hp.replace_bold(new_html)
    new_html = hp.replace_italics(new_html)
    new_html = hp.replace_s_tags(new_html)
    return new_html

def get_acordao(case_url):
    rows = gimme_rows(case_url)
    processo = get_content(get_row(rows, "Processo:"))
    relator = get_content(get_row(rows, "Relator:"))
    descritores = get_list_content(get_row(rows, "Descritores:"))
    numero = get_content(get_row(rows, "Nº do Documento:"))
    data = get_content(get_row(rows, "Data do Acordão:"))
    votacao = get_content(get_row(rows, "Votação:"))
    txt_integral_flag = get_content(get_row(rows, "Texto Integral:"))
    txt_parcial_flag = get_content(get_row(rows, "Texto Parcial:"))
    meio_processual = get_content(get_row(rows, "Meio Processual:"))
    decisao = get_content(get_row(rows, "Decisão:"))
    # TODO here we need to get newlines as well
    sumario = get_content(get_row(rows, "Sumário:"))
    dec_texto_parcial = get_content(get_row(rows, "Decisão Texto Parcial:"))

    # At this point
    # Get the row for texto integral
    # From the row, get the column with the content
    # Pass that whole thing to html_prework to replace with new lines
    # then make soup from that, then get text
    html_texto_integral = get_html(get_row(rows, "Decisão Texto Integral:"))
    html_for_integral_soup = hp.replace_html_new_lines(html_texto_integral)
    integral_soup = get_soup(html_for_integral_soup)
    dec_texto_integral = integral_soup.get_text(strip=False)

    # now get html
    html_for_saving = prepare_html_for_saving(html_texto_integral)

    ac = acordao.Acordao(processo, relator, descritores, numero, data, votacao, txt_integral_flag, txt_parcial_flag,
                         meio_processual, decisao, sumario, dec_texto_parcial, dec_texto_integral, html_for_saving)
    return ac

