def write_file(path, content):
    try:
        with open(path, "wb") as file:
            file.write(content)
    except Exception as e:
        print(e)
