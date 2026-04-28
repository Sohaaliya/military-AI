def get_window(words, index, k=2):
    left = words[max(0, index-k):index]
    right = words[index+1:index+1+k]
    return " ".join(left + ["___"] + right)