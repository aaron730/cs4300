def count_words(filename):
    with open(filename, 'r') as file:
        text = file.read()
    words = text.split()
    return len(words)

print(count_words("task6_read_me.txt"))