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

# for keeping formatting, maybe every bit of text is in a tuple with list of formattings e.g.
# [('text, etc', [italics, bold]), ('text, etc', [bold])]
# OR JUST KEEP HTML AS IS FOR DECISAO INTEGRAL


# Parameterise so can do this for all types of formatting	
# all_bold = column_txt_integral.find_all('b')
# bold_list = []
# for bold in all_bold:
# 	bold_list.append(bold.get_text())

# bold_list = [bold.strip() for bold in bold_list if not bold.isspace()]


# just_strings = [string_format[0] for string_format in text_format]
# for bold_text in bold_list:
# 	position_of_string = just_strings.index(bold_text)
# 	# check if string already marked as bold in which case move on to the next one
# 	while('b' in text_format[position_of_string][1]):
# 		position_of_string = just_strings.index(bold_text, position_of_string + 1)
# 	#after exiting loop, put 'b' in formatting list

# 	text_format[position_of_string][1].append('b')
# 	print(position_of_string)
# 	print(bold_text)

# for tf in text_format:
# 	if 'b' in tf[1]:
# 		print(tf)


# while(start_index < end_index):
# 	font_open_start = html_text.find('<font', start_index, end_index)
# 	font_open_end = html_text.find('>', font_open_start, end_index)
# 	print("font open start " + str(font_open_start))

# 	font_string = html_text[font_open_start: font_open_end+1]
# 	print(font_string)	
# 	# iterate backwards
# 	close_tag_start = html_text.find('</', start_index, font_open_start)

# 	if close_tag_start == -1:
# 		close_tag_start = start_index
# 		close_tag_end = start_index -1
# 	else:
# 		close_tag_end = html_text.find('>', close_tag_start)

# 	print('close tag start: ' + str(close_tag_start))
# 	print('close tag end: ' + str(close_tag_end))

# 	font_close_start = html_text.find('</font>', font_open_end+1, end_index)
# 	font_close_end = font_close_start + len('</font')
# 	print('font_close_start' + str(font_close_start))
# 	print(html_text[font_close_start:font_close_end])
# 	# find next instance of non-closing tag

# 	regex = re.compile('<[a-zA-Z]+')
# 	result = regex.search(html_text, font_close_end)
# 	if result:
# 		next_open = result.start()
# 	else:
# 		next_open = end_index	

# 	print("next open: " + str(next_open))

# 	# recreate string
# 	html_text = (html_text[:close_tag_end+1] + font_string + html_text[close_tag_end+1:font_open_start] + html_text[font_open_end+1:font_close_start] 
# 		+ html_text[font_close_end+1:next_open] + html_text[font_close_start:font_close_end+1] + html_text[next_open:])
# 	#print(html_text)
# 	start_index = next_open
# 	print('start_index: ' + str(start_index))
# 	#with open('new_html.txt', 'w+') as f:
# 	#	f.write(html_text)
# 	#print(html_text[start_index:])
# 	#break
# 	time.sleep(10)



# print('exited loop')


# def close_p_tags(html_text):
# # dgsi html has <p> but no </p> meaning we can't parse for <p>s through beautiful soup
# #html_text = '<p>' + html_text + '</p>'
# p_open = '<p>'
# p_close = '</p>'
# # start = 0
# # print(len(html_text))
# # while(start <= len(html_text)):
# # 	p_open_start = html_text.find(p_open, start)
# # 	if p_open_start == -1:
# # 		break
# # 	html_text = html_text[:p_open_start] + p_close + html_text[p_open_start:]
# # 	start = p_open_start + len(p_close + p_open)

# html_text = html_text.replace(p_open, p_close + p_open)

# # Also it doesn't usually have a <p> tag right at the start, add one
# html_text = p_open + html_text + p_close
# return html_text
