#!/usr/bin/env python3

def usage(progname: str) -> None:
	print(f"Usage: {progname} [var-bf file] <output file> <mapping requirements,>")
	print(f"Usage: {progname} [var-bf file] -- <mapping requirements,>")
	print("Mapping Requirements:")
	print("\tComma-separated list of pairs of variable names (characters) and required locations (integers)")
	print("\tMost useful: mapping N vars to 0..N or to k-N..k-1 for k = # of vars")

eliminate_nonvar_chars_transation_table = str.maketrans(
	{
		"[": "",
		"]": "",
		">": "",
		"<": "",
		",": "",
		".": "",
		"+": "",
		"-": "",

		" ": "",
		"\n": "",
		"\t": "",
	}
)

commented_bf_chars_translation_table = str.maketrans(
	",.[]<>+-",
	"，．［］＜＞＋－"
)

def make_program(var_program: str, var_map: "Dict[str, int]") -> str:
	program: str = "#vbf[" + repr(var_map) + "]\n"
	current_location: int = 0
	skip_comment: bool = False
	for c in var_program:
		if skip_comment and c == '\n':
			skip_comment = False
			program += c
		elif c == '#':
			skip_comment = True
			program += c
		elif not skip_comment and c in var_map:
			new_location: int = var_map[c]
			location_diff = new_location - current_location
			if location_diff > 0:
				program += ">"*location_diff
			elif location_diff < 0:
				program += "<"*-location_diff
			current_location = new_location
		elif skip_comment:
			program += c.translate(commented_bf_chars_translation_table)
		else:
			program += c
	return program

def strip_comments(program: str) -> str:
	program_nocomments = ""
	skip_comment: bool = False
	for c in program:
		if c == '\n':
			skip_comment = False
		elif c == '#':
			skip_comment = True

		if not skip_comment:
			program_nocomments += c
	return program_nocomments

def main(var_program: str, mapping_requirements) -> "Tuple[str, Dict[str, int]]":
	from sys import stderr
	from itertools import permutations
	var_program_nocomments = strip_comments(var_program)
	vars = {*var_program_nocomments.translate(eliminate_nonvar_chars_transation_table)}

	print("vars =", vars, file=stderr)

	best: "Tuple[str, Dict[str, int]]" = None

	mapping_template = [None] * len(vars)
	vars -= {*mapping_requirements.keys()}
	for var, index in mapping_requirements.items():
		mapping_template[index] = var

	def fix_var_array(var_array):
		new_var_array = mapping_template[:]
		index: int = 0
		for var in var_array:
			while new_var_array[index] is not None:
				index += 1
			new_var_array[index] = var
		return new_var_array

	for var_array in map(fix_var_array, permutations(vars)):
		print("var_array =", var_array, end='', file=sys.stderr)
		var_map = {v: index for index, v in enumerate(var_array)}
		program = make_program(var_program, var_map)
		print("; length = ", len(program), file=sys.stderr)
		if best is None or len(program) < len(best[0]):
			best = (program, var_map)

	return best

def parse_mapping_requirements(mapping_requirements_str: str) -> "Dict[str, int]":
	mapping_requirements = [requirement.split(':') for requirement in mapping_requirements_str.split(',')]
	for requirement in mapping_requirements:
		if len(requirement) != 2 or len(requirement[0]) != 1:
			raise ValueError
		requirement[1] = int(requirement[1]) # may raise ValueError
	return {k: v for k, v in mapping_requirements}

if __name__ == "__main__":
	import sys
	if len(sys.argv) == 2 or len(sys.argv) == 3 or len(sys.argv) == 4:
		mapping_requirements: "Dict[str, int]" = dict()
		if len(sys.argv) == 4:
			mapping_requirements = parse_mapping_requirements(sys.argv[3])

		try:
			file = open(sys.argv[1], "r")
		except FileNotFoundError:
			print(f"File not found: {repr(sys.argv[1])}")
			usage(sys.argv[0])
			sys.exit(-1)
		results = main(file.read(), mapping_requirements)
		print(results[1], "length =", len(results[0]))
		if len(sys.argv) >= 3 and sys.argv[2] != "--":
			try:
				file = open(sys.argv[2], "x")
			except FileExistsError:
				print(f"Output file ({repr(sys.argv[2])}) already exists. Overwrite? (y/N) ", end='')
				sys.stdout.flush()
				response = sys.stdin.readline()
				if response[:1] not in "yY":
					sys.exit(-1)
				try:
					file = open(sys.argv[2], "w")
				except:
					print(f"Could not open output file: {repr(sys.argv[2])}")
					sys.exit(-1)
			except:
				print(f"Could not open output file: {repr(sys.argv[2])}")
				sys.exit(-1)
			file.write(results[0])
			file.close()
	else:
		usage(sys.argv[0])
