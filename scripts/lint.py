from subprocess import check_call


def lint():
    check_call(["isort", "-rc", "src"])
    check_call(["black", "src", "setup.py"])
    check_call(["python", "-m", "robot.tidy", "-r", "atest"])


if __name__ == "__main__":
    lint()
