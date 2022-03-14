import tempfile


def create_tempfile():
    return tempfile.TemporaryFile("wb", prefix="adam_")


