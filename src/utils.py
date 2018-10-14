import os

"""
Parses the text file with the specified file path, and adds variables to a dictionary.  Creates
a new dictionary if none is given, or adds to an existing dictionary if it is supplied with the
vars argument.

Inputs:
	filename = path to .txt file to read
	vars = existing variable dictionary (with strings as keys) to add to

Syntax for text file:
	# comment lines like this
	variable_name = 5

	# blank lines are ignored
	array_variable = [1, 2, 3, 4]
	also_ok_array = [ 1 2 3 4 ]
	expression_variable = variable_name * 2 + 0.3
"""
def parse_text_file(filename, vars=None):
	# create variable dictionary if one is not provided
	if vars is None:
		vars = {}
	with open(filename, 'r') as f:
		lines = f.readlines()
	line_num = 0
	for line in lines:
		words = line.split()

		# skip blank or commented lines
		if len(words) == 0 or "#" in words[0]:
			line_num += 1
			continue;

		# check validity of line
		if len(words) < 3:
			raise ValueError("Not enough words in line {} (expected 3, got {})".format(line_num, len(words)))

		# line is an assignment to a constant value
		if (words[1] == "="):
			var_name = words[0]
			var_val_string = words[2]

			# var is an array
			if "[" in words[2]:
				vars[var_name] = []
				words_ind = 2
				while words_ind < len(words):
					stripped_word = words[words_ind].replace('[', '').replace(']', '').replace(',', '')
					# word is not an isolated comma or bracket
					if len(stripped_word) > 0:
						vars[var_name].append(parse_word(stripped_word))
					words_ind += 1
			# var is a single value
			else:
				vars[var_name] = parse_word(var_val_string)
		# line is an expression
		elif (words[1] == ":"):
			var_name = words[0]
			var_expression_sentence = words[2:]
			# print(var_expression_sentence)
			for i in range(len(var_expression_sentence)):
				word = var_expression_sentence[i]
				# expression word corresponds to existing value in vars
				if "#" in word:
					break # stop parsing expression upon encountering comment
				if word in vars:
					# replace expression word with value string
					var_expression_sentence[i] = str(vars[word])
			# print(var_expression_sentence)
			vars[var_name] = eval(''.join(var_expression_sentence))
		# line does not have an assignment or expression symbol
		else:
			raise ValueError("Did not find expected '=' or ':' as second word in line {}".format(line_num))
		
		# successfully read line
		line_num += 1

	return vars

"""
Helper function for parse_text_file and parse_results_file
Inputs:
	parse_word = string blob to be processed into a data type
"""
def parse_word(word):
	# word is a string (not a number with 1 or 0 decimals)
	if not word.replace('.', '', 1).lstrip("+-").isdigit():
		var = word
	# word is a float
	elif "." in word:
		var = float(word)
	# word is an int
	else:
		var = int(word)

	return var

"""
Takes an input dictionary of lists, and builds an output dictionary of elements at the specified index in the
lists of the input dictionary.
Inputs:
	input_dict = input dictionary of lists
	element_index = index of elements to pull from input dictionary lists
	output_dict = output dictionary of elements from index element_index in input dictioary list
"""
def element_dict_from_list_dict(list_dict, element_index, element_dict=None):
	# create element dict if one is not provided
	if element_dict is None:
		element_dict = {}
	for key in list_dict.keys():
		# check if value retrieved by key is subscriptable
		if not isinstance(list_dict[key], list):
			continue
		element_dict[key] = list_dict[key][element_index]
	return element_dict

"""
Parses a particular type of text file where every value on the right of an "=" sign is associated with the string
word to the left of the "=" sign.
"""
def parse_results_file(filename, vars=None):
	# create variable dictionary if one is not provided
	if vars is None:
		vars = {}
	with open(filename, 'r') as f:
		lines = f.readlines()
	line_num = 0
	for line in lines:
		words = line.split()
		for i in range(len(words)):
			if words[i] is "=":
				vars[words[i-1]] = parse_word(words[i+1])
	return vars

def list_dict_from_element_dicts(element_dicts, list_dict=None):
	# create lists dict if one is not provided
	if list_dict is None:
		list_dict = {}
	# find all keys from first element dictionary, iterate through
	for key in element_dicts[0].keys():
		list_dict[key] = []
		# add elements from all element dictionaries with the same key to list in list dictionary
		for element_dict in element_dicts:
			list_dict[key].append(element_dict[key])
	return list_dict