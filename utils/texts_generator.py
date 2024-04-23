import os
import random
import string


def generate_files(num_files, file_size):
    file_contents = {}
    for i in range(num_files):
        file_name = f"file_{i}.txt"
        try:
            with open(file_name, "w") as file:
                random_content = "".join(
                    random.choices(string.ascii_lowercase, k=file_size)
                )
                file.write(random_content)
            file_contents[file_name] = random_content
        except IOError as e:
            print(f"Error creating file {file_name}: {e}")
    return file_contents


def generate_keywords(file_contents, num_keywords, keyword_length):
    keywords = []
    for content in file_contents.values():
        for i in range(len(content) - keyword_length + 1):
            keyword = content[i : i + keyword_length]
            keywords.append(keyword)

    random.shuffle(keywords)
    return keywords[:num_keywords]


def generate_data():
    num_files = 10
    file_size = 1000
    num_keywords = 5
    keyword_length = 5

    files = generate_files(num_files, file_size)
    keywords = generate_keywords(files, num_keywords, keyword_length)

    return files, keywords


def remove_files(files):
    for file in files:
        try:
            os.remove(file)
        except OSError as e:
            print(f"Error deleting file {file}: {e}")
