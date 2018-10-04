import os

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
		if (words[1] != "="):
			raise ValueError("Did not find expected equals sign as second word in line {}".format(line_num))

		# set variable in dictionary
		var_name = words[0]
		var_val_string = words[2]

		# var is an array
		if "[" in words[2]:
			vars[var_name] = []
			words_ind = 2
			while words_ind < len(words):
				vars[var_name].append(
					parse_word(
						words[words_ind].replace('[','').replace(']','')))
				words_ind += 1
		# var is a single value
		else:
			vars[var_name] = parse_word(var_val_string)

		# successfully read line
		line_num += 1

	return vars

def parse_word(word):
	# word is a string (not a number with 1 or 0 decimals)
	if not word.replace('.', '', 1).isdigit():
		var = word
	# word is a float
	elif "." in word:
		var = float(word)
	# word is an int
	else:
		var = int(word)

	return var