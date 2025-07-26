#! /usr/bin/env python3
from os import getcwd, listdir, makedirs, read, rmdir
from shutil import copytree, rmtree
import frontmatter
from markdown import markdown

base = getcwd()

def read_file(path: str):
  with open(f"{base}/{path}", "r") as f:
    return f.read()
  raise Exception(f"file not found at path: {path}")

def write_file(path: str, contents: str):
  with open(f"{base}/{path}", "w") as f:
    return f.write(contents)
  raise Exception(f"failed to write file at path: {path}")

def template(file: str, values: dict[str, str]):
  templated = file
  for key in values:
    templated = templated.replace("{{" + key + "}}", values[key])
  return templated

def copy_and_template(source_path: str, dest_path: str, values: dict[str, str]):
  source = read_file(source_path)
  templated = template(source, values)
  write_file(dest_path, templated)

rmtree(f"{base}/dist")
makedirs(f"{base}/dist", exist_ok=True)
makedirs(f"{base}/dist/posts", exist_ok=True)
copytree(f"{base}/src/img", f"{base}/dist/img")

copy_and_template("src/index.html", "dist/index.html", {})
# TODO: template out the various entries
copy_and_template("src/posts.html", "dist/posts.html", {})

post_template = read_file("src/post.html")
filenames = listdir(f"{getcwd()}/src/posts")
for filename in filenames:
  post = frontmatter.load(f"{base}/src/posts/{filename}")
  post_html = markdown(post.content)
  templated = template(post_template, {
    'title': post.metadata["title"],
    'content': post_html
  })
  target_filepath = f"dist/posts/{filename.replace('.md', ".html")}"
  write_file(target_filepath, templated)
  print(f"Generated {filename}")

print("Done!")