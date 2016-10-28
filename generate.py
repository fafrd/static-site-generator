#!/usr/bin/env python
# inspired by habu github.com/botherder/habu

import os
import re
import sys
import time
import shutil
import mistune
import argparse

try:
	import yaml
	from markdown import Markdown
	from markdown.preprocessors import Preprocessor
	from jinja2.loaders import FileSystemLoader
	from jinja2.environment import Environment
	from pygments import highlight
	from pygments.formatters import HtmlFormatter
	from pygments.lexers import get_lexer_by_name, TextLexer
except ImportError as e:
	print("Unable to import dependency:" + str(e))
	sys.exit(-1)

env = Environment()
env.loader = FileSystemLoader("templates")

class CodeBlockPreprocessor(Preprocessor):
	"""This converts code blocks into highlighted code.
	Neat stuff."""
	pattern = re.compile(r"\[code:(.+?)\](.+?)\[/code\]", re.S)
	formatter = HtmlFormatter(noclasses=True, cssclass="colorful")

	def run(self, lines):
		def repl(m):
			try:
				lexer = get_lexer_by_name(m.group(1))
			except ValueError:
				lexer = TextLexer()

			code = highlight(m.group(2), lexer, self.formatter)
			return "\n{0}\n".format(code)

		return [self.pattern.sub(repl, "\n".join(lines))]


def generate_posts(destination):
	posts = []

	for post in os.listdir("posts"):
		if post[0] == '.':
			print("skipping post " + post)
			continue
		orig = os.path.join("posts", post)
		print("processing post: " + post)
		raw = open(orig, "r").read()
		metadata, content = raw.split("\n\n", 1)
		headers = yaml.load(metadata)
		md = Markdown()
		md.preprocessors.add("sourcecode", CodeBlockPreprocessor(), "_begin")
		content = md.convert(content)
		
		if headers.has_key("date"):
			date = headers["date"]
		else:
			date = str(time.strftime("%Y-%m-%d %H:%M:%S"))

		if headers.has_key("tags"):
			tags = headers["tags"]
		else:
			tags = []

		if headers.has_key("title") == 0:
			print("markdown file does not contain a title! see examples. skipping...")
			return
		else:
			title = headers["title"]

		filename = title + ".html"
		filename = filename.replace(' ', '-').lower()

		"""post object describes post content plus metadata. 'active' specifies which one is printed in the next for loop."""
		post_obj = {'title': title, 'date': date, 'link': filename, 'content': content, 'active': 0}
	
		posts.append(post_obj)

	posts.sort(key=lambda key: key["date"])
	posts.reverse()
	
	for post in posts:
		filename = post['title'] + ".html"
		filename = filename.replace(' ', '-').lower()
		dest = os.path.join(destination, filename)
		print("processing post2: " + post['title'])
		template = env.get_template("post.html")
		post['active'] = 1
		html = template.render(**{'posts': posts})
		post['active'] = 0

		with open(dest, "w") as handle:
			handle.write(html)
	
	return posts

def generate_index(posts, destination):
	dest = os.path.join(destination, "index.html")

	template = env.get_template("index.html")
	html = template.render(**{'posts': posts})

	with open(dest, "w") as handle:
		handle.write(html)

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-d", "--destination", help="specify destination folder", required=True)
	args = parser.parse_args()
	
	if not os.path.exists(args.destination):
		print("destination folder does not exist")
		return
	
	print("generating posts, destination is " + args.destination)
	posts = generate_posts(args.destination)
	print("generating index")
	generate_index(posts, args.destination)

main()
