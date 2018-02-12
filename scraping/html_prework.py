new_line_html = ['<p>', '</p>', '<br>', '<br/>']


def remove_font_tags(html_text):
    # delete all font open tags
    font_open_start = 0
    while (font_open_start != -1):
        end_index = len(html_text)
        font_open_start = html_text.find('<font')
        if font_open_start == -1:
            break
        font_open_end = html_text.find('>', font_open_start)
        html_text = html_text[:font_open_start] + html_text[font_open_end + 1:]

    # delete all font close tags
    font_close_start = 0
    while (font_close_start != -1):
        font_close_start = html_text.find('</font')
        if font_close_start == -1:
            break
        font_close_end = html_text.find('>', font_close_start)
        html_text = html_text[:font_close_start] + html_text[font_close_end + 1:]

    return html_text


def close_p_tags(html_text):
    # dgsi html has <p> but no </p> meaning we can't parse for <p>s through beautiful soup
    # html_text = '<p>' + html_text + '</p>'
    p_open = '<p>'
    p_close = '</p>'
    html_text = html_text.replace(p_open, p_close + p_open)

    # Also it doesn't usually have a <p> tag right at the start, add one
    html_text = p_open + html_text + p_close

    # what if closing tags were already there? Replace double close tags with just one
    html_text = html_text.replace(p_close + p_close, p_close)
    return html_text


def replace_bold(html_text):
    html_text = html_text.replace('<b>', '<strong>')
    html_text = html_text.replace('</b>', '</strong>')
    return html_text


def remove_bold(html_text):
    html_text = html_text.replace('<b>', '')
    html_text = html_text.replace('</b>', '')
    return html_text


def replace_italics(html_text):
    html_text = html_text.replace('<i>', '<em>')
    html_text = html_text.replace('</i>', '</em>')
    return html_text


def replace_s_tags(html_text):
    html_text = html_text.replace('<s>', '<del>')
    html_text = html_text.replace('</s>', '</del>')
    return html_text


def replace_html_new_lines(html_text):
    for tag in new_line_html:
        html_text = html_text.replace(tag, '\n')

    return html_text
