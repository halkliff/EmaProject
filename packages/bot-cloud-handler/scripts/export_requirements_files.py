def run():
    from subprocess import call
    from pathlib import Path

    with Path("requirements.txt") as f:
        f.unlink()
    with Path("requirements-dev.txt") as f:
        f.unlink()

    call(
        [
            "poetry",
            "export",
            "-f",
            "requirements.txt",
            "-o",
            "requirements.txt",
            "--without-hashes",
        ],
    )
    call(
        [
            "poetry",
            "export",
            "-f",
            "requirements.txt",
            "-o",
            "requirements-dev.txt",
            "--only",
            "dev",
            "--without-hashes",
        ],
    )
