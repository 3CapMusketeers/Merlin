def write_file(path, content):
    with open(path, "wb") as file:
        file.write(content)