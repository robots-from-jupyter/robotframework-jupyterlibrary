""" a lightweight robot runner

Install once (per notebook/kernel):

    %reload_ext JupyterLibrary
"""
from pathlib import Path
from hashlib import sha256
import shutil

from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers.robotframework import RobotFrameworkLexer
from pygments.styles import get_all_styles

from IPython import get_ipython
from IPython.display import (
    display,
    HTML,
    Markdown,
)
from IPython.core import magic_arguments
from IPython.core.magic import (
    Magics,
    magics_class,
    cell_magic,
)

import robot


@magics_class
class RobotMagics(Magics):
    """
    Run Robot Framework code

    Example:
        %%robot --
        *** Tasks ***
        Just Log Something
            Log    Something
    """

    PRETTY_CLASS = "robot-magic"

    @cell_magic
    @magic_arguments.magic_arguments()
    @magic_arguments.argument(
        "output_dir",
        default="_robot_magic_",
        nargs="?",
        help="""Name of directory to update (default:.robot-magic) """,
    )
    @magic_arguments.argument(
        "-e", "--execute", default=True, help="""run the robot test"""
    )
    @magic_arguments.argument(
        "-p",
        "--pretty",
        default=True,
        help="""print out syntax highlighted, tidied source""",
    )
    @magic_arguments.argument(
        "-s",
        "--style",
        default="colorful",
        help=f"""style to use, one of: {", ".join(sorted(get_all_styles()))}""",
    )
    @magic_arguments.argument(
        "-g",
        "--gui",
        default="display",
        help="""how to show outputs, one of: display, widget""",
    )
    @magic_arguments.argument(
        "-a",
        "--arg",
        default=None,
        help="name of a variable in user_ns to use for robot.run arguments",
    )
    def robot(self, line, cell):
        """run some Robot Framework code"""
        ip = get_ipython()
        line = f" {line} "

        m = sha256()
        m.update(line.encode("utf-8"))
        m.update(cell.encode("utf-8"))

        content_hash = str(m.hexdigest())[:12]

        args = magic_arguments.parse_argstring(self.robot, line)

        # displays = []
        # widget = None

        if args.gui == "display":
            display(Markdown("- _🤖 getting ready..._"))

        if args.pretty:
            lexer = RobotFrameworkLexer()
            formatter = HtmlFormatter(cssclass=self.PRETTY_CLASS, style=args.style)
            css = formatter.get_style_defs(f".{self.PRETTY_CLASS}")
            highlighted = highlight(cell, lexer, formatter)
            html = HTML(
                f"""
                <ul><li>
                <details>
                    <summary>Formatted Robot Code</summary>
                    <style>{css}</style>{highlighted}
                </details>
                </li></ul>
            """
            )

            if args.gui == "display":
                display(html)

        if args.execute:
            outputdir = Path.cwd() / args.output_dir / content_hash
            display(Markdown(f"- _🤖 making files in_ `{outputdir}`"))
            if outputdir.exists():
                shutil.rmtree(outputdir)

            outputdir.mkdir(parents=True)

            robot_file = outputdir / "it.robot"

            robot_file.write_text(cell)

            display(Markdown("- _🤖 running!_"))
            stdout_file = outputdir / "stdout.txt"
            stderr_file = outputdir / "stderr.txt"

            robot_args = ip.user_ns[args.arg] if args.arg else {}

            with open(stdout_file, "w+") as stdout:
                with open(stderr_file, "w+") as stderr:
                    rc = robot.run(
                        robot_file,
                        exit=False,
                        outputdir=outputdir,
                        stderr=stderr,
                        stdout=stdout,
                        **robot_args,
                    )

            if args.gui == "display":
                for outfile in [stdout_file, stderr_file]:
                    display(
                        HTML(
                            f"""
                            <ul><li>
                                <code>{outfile.name}</code>
                                <code><pre>{outfile.read_text() or "empty"}</pre></code>
                            </li></ul>
                            """
                        )
                    )
                files = [
                    f"""<li>
                        <a href="{p.relative_to(Path.cwd()).as_posix()}"
                                data-commandlinker-command="filebrowser:open"
                                data-commandlinker-args="{{}}">
                            {p.relative_to(outputdir).as_posix()}
                        </a>
                    </li>
                    """
                    for p in sorted(outputdir.rglob("*"))
                ]
                display(
                    HTML(
                        """
                    <ul><li><details>
                        <summary>{} Files</summary>
                        <ul>{}</ul>
                    </li></ul>
                """.format(
                            len(files), "\n".join(files)
                        )
                    )
                )
                display(Markdown(f"- _🤖 returned {rc}_"))

            if rc:
                raise RuntimeError(f"robot returned {rc}")


def load_ipython_extension(ip):
    ip = get_ipython()
    ip.register_magics(RobotMagics)
