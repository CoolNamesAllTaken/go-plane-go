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
def parse_text_file(filename, vars={}):
	with open(filename, 'r') as file:
		lines = file.readlines()
	line_num = 0
	for line in lines:
		words = line.split()

		# skip blank or commented lines
		if len(words) == 0 or words[0] == "#":
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