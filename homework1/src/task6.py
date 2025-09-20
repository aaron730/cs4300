
#Method to count words in a given file
def count_words(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            text = file.read()
        words = text.split()
        return len(words)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return -1
    except IOError as e:
        print(f"Error reading file '{filename}': {e}")
        return -1


#Prints the word count
print(count_words("task6_read_me.txt"))