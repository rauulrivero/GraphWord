def file_tokenizer(content):
    # obtener un diccionario de palabras y su frecuencia
    words = content.split()
    word_freq = {}
    for word in words:
        if word in word_freq:
            word_freq[word] += 1
        else:
            word_freq[word] = 1
    return word_freq
