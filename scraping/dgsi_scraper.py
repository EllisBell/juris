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
    this_soup = BeautifulSoup(r.content, 'html.parser')
    case_rows = this_soup.find_all('tr')
    return case_rows


def get_row(rows, section_header):
    for row in rows:
        if row.td.get_text(strip=True) == section_header:
            return row


def get_content(row):
    if row is not None:
        return row.find_all('td')[1].get_text(strip=True)
    return ""


def get_list_content(row):
    list_cont = []
    col = row.find_all('td')[1]
    for string in col.strings:
        list_cont.append(string)

    # Get rid of whitespace elements and strip away whitespace from actual terms
    list_cont = [term.strip() for term in list_cont if not term.isspace()]
    return list_cont


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
    sumario = get_content(get_row(rows, "Sumário:"))
    dec_texto_parcial = get_content(get_row(rows, "Decisão Texto Parcial:"))
    dec_texto_integral = get_content(get_row(rows, "Decisão Texto Integral:"))
    # TODO figure out how to get html
    ac = acordao.Acordao(processo, relator, descritores, numero, data, votacao, txt_integral_flag, txt_parcial_flag,
                         meio_processual, decisao, sumario, dec_texto_parcial, dec_texto_integral, '')
    return ac






# base_url = "http://www.dgsi.pt"

# # try out TRLisboa
# url = "http://www.dgsi.pt/jtrl.nsf?OpenDatabase"

# headers = {'User-Agent': 'Mozilla/5.0'}

# r = requests.get(url, headers=headers)

# #print(r.content)

# # get all hrefs to each case on page
# soup = BeautifulSoup(r.content, 'html.parser')
# #print(soup.prettify)

# #print(soup.findall('a'))
# #for link in soup.find_all('a'):
# #  print(link.get('href'))

# # Get only the a tags that have hrefs that match regex 
# #for link in soup.find_all('a', href=re.compile('jtrl.nsf/[0-9a-z]')):
# #  print(link.get('href'))

# links = soup.find_all('a', href=re.compile('OpenDocument'))

# print(links[1])
# case_html = requests.get(base_url + links[1].get('href'), headers=headers)
# #print(case_html.content)

# case_soup = BeautifulSoup(case_html.content, 'html.parser')
# #print(case_soup.prettify)

# rows = case_soup.find_all('tr')

# # Get <td> tags in row which has processo
# columns_processo = rows[1].find_all('td')
# # Get <td> tags within second column, grab the first one
# column_processo = columns_processo[1].find_all('td')[0]

# processo = column_processo.get_text(strip=True)

# # Relator
# columns_relator = rows[3].find_all('td')
# column_relator = columns_relator[1]
# relator = column_relator.get_text(strip=True)

# print("processo: {0}, Relator: {1}".format(processo, relator))

# # Descritores
# columns_descs = rows[4].find_all('td')
# column_descs = columns_descs[1]
# print(column_descs.get_text())
# # Make list of descriptors
# descs_list = []
# for string in column_descs.strings:
# 	descs_list.append(string)

# # Get rid of whitespace elements and strip away whitespace from actual terms
# descs_list = [desc.strip() for desc in descs_list if not desc.isspace()]
# print(descs_list)

# #Nº do documento
# columns_numero = rows[6].find_all('td')
# column_numero = columns_numero[1]
# numero = column_numero.get_text(strip=True)
# print(numero)

# # Data do acordao
# columns_date = rows[7].find_all('td')
# column_date = columns_date[1]
# date = column_date.get_text(strip=True)
# print(date)

# # Votacao
# columns_votacao = rows[8].find_all('td')
# column_votacao = columns_votacao[1]
# votacao = column_votacao.get_text(strip=True)
# print(votacao)

# # Texto Integral Flag
# columns_integral = rows[9].find_all('td')
# column_integral = columns_integral[1]
# integral = column_integral.get_text(strip=True)
# print(integral)

# # Meio Processual
# columns_meio = rows[11].find_all('td')
# column_meio = columns_meio[1]
# meio = column_meio.get_text(strip=True)
# print(meio)

# # Decisao
# columns_decisao = rows[12].find_all('td')
# column_decisao = columns_decisao[1]
# decisao = column_decisao.get_text(strip=True)
# print(decisao)

# # Sumario
# columns_sumario = rows[14].find_all('td')
# column_sumario = columns_sumario[1]
# sumario = column_sumario.get_text(strip=True)
# print(sumario)
# for string in column_sumario.stripped_strings:
# 	print(repr(string))

# # Decisao Texto Parcial
# columns_txt_parcial = rows[15].find_all('td')
# column_txt_parcial = columns_txt_parcial[1]
# txt_parcial = column_txt_parcial.get_text(strip=True)
# print(txt_parcial)

# # Decisao Texto Integral
# # Get just text and get untouched html as well
# columns_txt_integral = rows[17].find_all('td')
# print(columns_txt_integral)
# column_txt_integral = columns_txt_integral[1]
# #print(column_txt_integral)
# txt_integral = column_txt_integral.get_text()
# #print(txt_integral)


# # this is the html for the txt integral that we will store
# txt_int_html = str(column_txt_integral)
# new_html = hp.remove_font_tags(txt_int_html)
# # by closing the p tags we can then parse this html for paragraphs properly and build up the text to store from there
# new_html = hp.close_p_tags(new_html)

# new_html = hp.replace_bold(new_html)

# new_html = hp.replace_italics(new_html)
# #print()

# with open('new_html.html', 'w+') as f:
#  	f.write(new_html)


# string_parts = []
# for string in column_txt_integral.stripped_strings:
# 	string_parts.append(str(string))

# # make soup from the new html
# txt_int_soup = BeautifulSoup(new_html, 'html.parser')

# paragraphs = txt_int_soup.find_all('p')
# #for para in paragraphs:
# #	print(repr(para.get_text(strip = True)))

# # with open('text_results.txt', 'w') as f:
# # 	f.write(new_string)
