def naive_weight(text: str, terms: list[str]):
    term_counts = {t:0 for t.upper() in terms}    
    
    for word in text.split():
        if word.upper() in term_counts:
            term_counts[word.upper()] += 1
