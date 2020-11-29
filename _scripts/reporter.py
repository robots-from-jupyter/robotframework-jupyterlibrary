from doit.reporter import ConsoleReporter

from . import project as P


START = "::group::" if P.CI else ""
END = "::endgroup::" if P.CI else ""


class GithubActionsReporter(ConsoleReporter):
    def execute_task(self, task):
        self.outstream.write(f"{START}🤖 {task.title()}\n")

    def add_failure(self, task, exception):
        super().add_failure(task, exception)
        self.outstream.write(f"   💥 {task.title()}{END}\n")

    def add_success(self, task):
        super().add_success(task)
        self.outstream.write(f"   🆗 {task.title()}{END}\n")

    def skip_uptodate(self, task):
        self.outstream.write(f"{START}🤖 {task.title()}{END}\n")

    skip_ignore = skip_uptodate
