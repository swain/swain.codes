#! /usr/bin/env python3
from datetime import datetime
from os import getcwd, listdir, makedirs
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

def to_readable_date(day: str):
  dt = datetime.strptime(day, "%Y-%m-%d")
  return dt.strftime("%B %-d, %Y")

rmtree(f"{base}/dist")
makedirs(f"{base}/dist", exist_ok=True)
makedirs(f"{base}/dist/posts", exist_ok=True)
copytree(f"{base}/src/img", f"{base}/dist/img")
copytree(f"{base}/src/styles", f"{base}/dist/styles")

copy_and_template("src/index.html", "dist/index.html", {})

post_anchors: list[str] = []
post_template = read_file("src/post.html")
for filename in listdir(f"{base}/src/posts"):
  post = frontmatter.load(f"{base}/src/posts/{filename}")
  post_html = markdown(post.content, extensions=["fenced_code", "codehilite"])
  templated = template(post_template, {
    'title': post.metadata["title"],
    'date': to_readable_date(filename[0:10]),
    'content': post_html
  })
  slug = filename[11:].replace(".md", "")
  target_filepath = f"dist/posts/{slug}.html"
  write_file(target_filepath, templated)
  post_anchors.append(
    f'<a href="/posts/{slug}" class="postlink">{post.metadata["title"]}</a>'
  )

copy_and_template("src/posts.html", "dist/posts.html", {
  "posts": "\n".join(post_anchors)
})

print("Built!")