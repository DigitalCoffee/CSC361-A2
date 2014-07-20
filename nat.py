import os
import copy

import file_util
import nat_util
import html_util

class nat:
	def __init__(self,question_library_path,question_path):
		self.question_library_path = question_library_path
		self.question_path = question_path

		config = file_util.dynamic_import(os.path.join(
		 question_library_path,question_path,'cqg_config.py'))
		self.public_ip_address = config.public_ip_address
		self.starting_port = config.starting_port

		self.traffic_list = config.traffic_list
		self.traffic_hotspots = config.traffic_hotspots
		self.conntrack_hotspots = config.conntrack_hotspots

		self.input_fields = []
		self.answer_key = {}

	'''
	purpose
		return question_library_path passed in constructor
	preconditions
		None
	'''
	def get_question_library_path(self):
		return self.question_library_path

	'''
	purpose
		return question_path passed in constructor
	preconditions
		None
	'''
	def get_question_path(self):
		return self.question_path

	'''
	purpose
		return a CSS string which will be placed in the HTML <head> tag
	preconditions
		None
	'''
	def get_css(self,answer):
		return ''

	'''
	purpose
		return a string containing the html to be displayed
		by abstract_question, including answers
	preconditions
		for each key K in get_input_element_ids():
			K is also in answer
			if K was not in submitted answer
				answer[K] == None
	'''
	def get_html(self,answer):
		i = 0
		(traff, conn) = nat_util.generate_tables(self.traffic_list, self.public_ip_address, self.starting_port)

		HTMLstring = '<h4>Private Network:10/24 &nbsp; &nbsp; &nbsp; Public IP Address:' + self.public_ip_address + '</h4>'
		HTMLstring += '<h4>NAT ports allocated sequentially starting at ' + self.starting_port
		HTMLstring += '<p></p>'

		HTMLstring += '<center>'
		HTMLstring += '<table border="1"><tbody>'
		HTMLstring += '<tr><td align="center" colspan="8">Traffic Table</td></tr>'
		HTMLstring += '<tr>'
		HTMLstring += '<td align="center" colspan="5">5-tuple</td><td>Direction</td><td align="center" colspan="2">Action</td>'
		HTMLstring += '</tr>'

		
		for row in traff:
			HTMLstring += '<tr>'
			for column in row[0]:
				HTMLstring += '<td>' + column + '</td>'
			btnName = self.input_fields[i]
			HTMLstring += '<td>' + row[1] + '</td>'
			HTMLstring += '<td>Accept:<input type="radio" value="accept" name="' + btnName + '"></input>'
			HTMLstring += 'Drop:<input type="radio" value="drop" name="' + btnName + '"></input></td>'
			HTMLstring += '</tr>'
			self.answer_key[btnName] = row[2]
			i = i+1
		
		HTMLstring += '</tbody></table>'
		HTMLstring += '</center>'

		HTMLstring += '<br /><br /><br />'

		HTMLstring += '<center>'
		HTMLstring += '<table border="1"><tbody>'
		HTMLstring += '<tr><td align="center" colspan="10">Connection tracking table</td></tr>'
		HTMLstring += '<tr>'
		HTMLstring += '<td align="center" colspan="5">Private 5-tuple</td>'
		HTMLstring += '<td align="center" colspan="5">Public 5-tuple</td>'
		HTMLstring += '</tr>'

		for j, row in enumerate(conn):
			HTMLstring += '<tr>'
			for k, col in enumerate(row[0]):
				if [[j, 0, k]] == self.conntrack_hotspots:
					txtBoxName = self.input_fields[i]
					HTMLstring += '<td>'
					HTMLstring += '<input type="text" size="3" value="" name="' + txtBoxName + '"></input>'
					HTMLstring += '</td>'
					self.answer_key[txtBoxName] = col
					i = i+1
				else:
					HTMLstring += '<td>' + col + '</td>'
			for k, col in enumerate(row[1]):
				if [[j, 1, k]] == self.conntrack_hotspots:
					txtBoxName = conntrack_textbox_name(j, 1, k)
					HTMLstring += '<td>'
					HTMLstring += '<input type="text" size="3" value="" name="' + txtBoxName + '"></input>'
					HTMLstring += '</td>'
					self.answer_key[txtBoxName] = col
					i = i+1
				else:
					HTMLstring += '<td>' + col + '</td>'
			HTMLstring += '</tr>'

		HTMLstring += '</tbody></table>'
		HTMLstring += '</center>'
		HTMLstring += '</h4>'

		return HTMLstring
			

	'''
	purpose
		return a list containing the names of the HTML
		input elements returned by get_html()
	preconditions
		None
	'''
	def get_input_element_ids(self):
		for row in enumerate(self.traffic_list):
			self.input_fields.append(traffic_button_name(row[0]))
		for field in self.traffic_hotspots:
			self.input_fields.append(traffic_textbox_name(field[0], field[1]))
		for field in self.conntrack_hotspots:
			self.input_fields.append(conntrack_textbox_name(field[0], field[1], field[2]))
		return self.input_fields

	'''
	purpose
		return True iff answer is correct
	preconditions
		for each key K in get_input_element_ids():
			K is also in answer
			if K was not in submitted answer
				answer[K] == None
	'''
	def check_answer(self,answer):
		for key, value in self.answer_key.items():
			if not key in answer:
				return False
			else:
				if not value == answer[key]:
					return False
		return True

# return name of text box in traffic table at row/col
def traffic_textbox_name(row,col):
	return 'traffic_' + str(row) + '_' + str(col)

# return name of radio button in traffic table at row
def traffic_button_name(row):
	return 'button_' + str(row)

# return string name of text box in connection tracking table at row/public_private/col
def conntrack_textbox_name(row,public_private,col):
	return 'conntrack_' + str(row) + '_' + str(public_private) + '_' + str(col)

