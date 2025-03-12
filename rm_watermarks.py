#!/usr/bin/env python3

import argparse
import os
from pathlib import Path
import re
import glob
from lib.toolprint import print_info, print_err, print_success

try:
	import pikepdf
except:
	print_err('Install pikepdf with "pip3 install pikepdf"')
	exit(1)

STRING_OPS = [pikepdf.Operator("Tj"), pikepdf.Operator("TJ")]
FONT_OPS = [pikepdf.Operator("Tf")]

def clean_pdf(pdf_path: str, password: str, output_dir: str, is_class_path=False):
	with pikepdf.open(pdf_path, password = password) as p:
		for i, page in enumerate(p.pages):
			bad_fonts = []
			for font in page.resources.as_dict()['/Font'].items():
				# Removing "Differences" font definitions which are used to create the watermarks.
				if font[1].as_dict()['/Encoding']["/Differences"]:
					bad_fonts.append(font[0])
					font[1].as_dict()['/Encoding']['/Differences'] = []

			instr = pikepdf.parse_content_stream(page)

			bad_code_block = False
			return_list = list()
			for _, ins in enumerate(instr):
				if(ins.operator in FONT_OPS and ins.operands[0] in bad_fonts):
					bad_code_block = True
				# bad code blocks continue to end of page so don't bother setting it back
				elif ins.operator in STRING_OPS and bad_code_block:
					continue				
				if not bad_code_block:
					return_list.append(ins)

			new_stream = pikepdf.unparse_content_stream(return_list)
			page.Contents = p.make_stream(new_stream)

		basename = Path(pdf_path).stem
		if not is_class_path:
			out_path = os.path.join(output_dir, f"{basename}_cleaned.pdf")
		else:
			out_path = os.path.join(output_dir, convert_class_path(basename))
		p.save(out_path)
		print_success(f"Saved pdf to {out_path}")

# checks if pdf filename is default filename
def is_class_path(pdf_path: str) -> bool:
	basename = Path(pdf_path).stem
	expr = r"[a-zA-Z]{3}[0-9]{3} - [a-zA-Z]+ ?[0-9]?_[0-9]+"
	return re.match(expr, basename) != None

def convert_class_path(pdf_basename: str) -> str:
	splits = pdf_basename.split(" - ")
	classname = splits[0]
	book_num_splits = splits[1].split()
	if len(book_num_splits) == 1:
		book_num_splits = splits[1].split("_")
		return f"{classname}_{book_num_splits[0]}.pdf"
	else:    
		return f"{classname}_{book_num_splits[0]}_{book_num_splits[1].split("_")[0]}.pdf"

def output_dir_path(path: str) -> bool:
	if os.path.isdir(path):
		return True
	try:
		os.mkdir(path)
		return True
	except:
		return False

if __name__ == "__main__":
	try:
		parser = argparse.ArgumentParser()
		parser.add_argument("-f", "--file", type=str, help="A pdf file to process")
		parser.add_argument("-d", "--directory", type=str, help="A directory of pdf files to process")
		parser.add_argument("-p", "--password", type=str, required=True, help="Password for pdf file")
		parser.add_argument("-o", "--output_dir", type=str, required=False, default="", help="Directory to return processed pdfs")

		args = parser.parse_args()
	except Exception as e:
		print_err(e)
		exit(1)

	# convert directory to absolute path
	if args.directory and not os.path.isabs(args.directory):
		args.directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), args.directory)

	if not args.directory and not args.file:
		print_err("Please include a file or directory to process")
		exit(1)
	
	if args.directory and not output_dir_path(args.directory):
		print_err(f"{args.directory} is not a valid directory")
		exit(1)
	
	if args.file and not os.path.exists(args.file):
		print_err(f"{args.file} does not exist or is not a valid file")
		exit(1)

	if args.output_dir and not output_dir_path(args.output_dir):
		print_err(f"{args.output_dir} is not a valid directory path and it was unable to be created...")
		exit(1)
	
	if args.file:
		print_info(f"Cleaning {args.file}...")
		try:
			clean_pdf(args.file, args.password, args.output_dir, is_class_path=is_class_path(args.file))
		except Exception as e:
			print_err(f"Couldn't process {args.file} because of: {e}")
			exit(1)
	elif args.directory:
		files = glob.glob(os.path.join(args.directory, "*.pdf"))
		for file in files:
			print_info(f"Cleaning {file}...")
			try:
				clean_pdf(file, args.password, args.output_dir, is_class_path=is_class_path(file))
			except Exception as e:
				print_err(f"Couldn't process {file} because of: {e}")
			print()
