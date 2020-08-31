import datetime
import os
import sys

import jinja2
from pysmith import BuildInfo, Pysmith
from pysmith.contrib.core.frontmatter import Frontmatter
from pysmith.contrib.web.markdown import Markdown
from pysmith.contrib.web.permalink import Permalink
from pysmith.contrib.web.sass import Sass
from pysmith.contrib.web.template import LayoutTemplate


class GlobalMetadata(object):

    def build(self, build_info: BuildInfo):
        build_info.metadata["title"] = "Dave Korhumel"


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(current_dir, "src")
    dest_dir = os.path.join(current_dir, "build")

    build_date = datetime.datetime.now()
    template_loader = jinja2.FileSystemLoader(os.path.join(current_dir, "_layouts"))

    p = Pysmith(src=src_dir, dest=dest_dir)
    p.enable_logging()
    p.use(GlobalMetadata())
    p.use(Frontmatter(match_pattern="*.md"))
    p.use(Markdown(
        extras=["header-ids", "smarty-pants"]
    ))
    p.use(LayoutTemplate(
        match_pattern="*.md",
        globals={
            "build_date": build_date,
        },
        environment_args={
            "loader": template_loader,
        }))
    p.use(Permalink())
    p.use(Sass(compile_args={
        "include_paths": [os.path.join(current_dir, "_sass")],
    }))

    p.clean().build()


if __name__ == "__main__":
    main()
