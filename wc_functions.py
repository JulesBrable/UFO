from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import pandas as pd
import matplotlib.pyplot as plt

def word_count(stri):
    
    """Function that counts the occurrence of different words within a string"""
    
    counts = dict()
    words = stri.split()

    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
            
    return counts

def mywc(df: pd.DataFrame, col: str, words_update: list, background = "white", mask = None, colors=None):
    
    """Creates a wordcloud with WordCloud package."""
    
    MYSTOPWORDS = STOPWORDS.update(words_update) # adding stopwords
    all_comments = " ".join(str(s) for s in df[col]) # joining comments all together
    wc = word_count(all_comments) # counting occurrence for each single word
    
    # generate the wordcloud with arbitrary predefined parameters
    wordcloud = WordCloud(scale=3,
                          stopwords=MYSTOPWORDS,
                          background_color=background,
                          mask=mask,
                          width=1600,
                          height=800, 
                          collocations=False,
                          max_words=200,
                          color_func=colors,
                          min_word_length=3).generate(all_comments)
    return wordcloud

def display_wc(wordcloud):
    
    fig, ax = plt.subplots(figsize=(10,6))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.set_axis_off()
    plt.imshow(wordcloud)
    return fig, ax