""" File to create a wordcloud
	Input - CSV File
	Output - PNG file (Image file extension) """

import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from scipy.misc import imread

df = pd.read_csv('output.csv')


twitter_mask = imread('./twitter_mask.png', flatten=True)

# join tweets to a single string
words = ' '.join(df['tweet'])

# remove URLs, RTs, and twitter handles
no_urls_no_tags = " ".join([word for word in words.split()
                            if 'http' not in word
                                and not word.startswith('@')
                                and word != 'RT'
                            ])

#print type(no_urls_no_tags)
more_stopwords = {'oh', 'will', 'hey', 'yet', 'and', 'what', 'why', 'how', 'some', 'maybe', 'becase'}
STOPWORDS = STOPWORDS.union(more_stopwords)

# Generate Wordcloud
wordcloud = WordCloud(
                      font_path='Fonts/champagne_limousines/Champagne & Limousines.ttf',
                      stopwords=STOPWORDS,
                      background_color='white',
                      width=1800,
                      height=1400,
                      mask=twitter_mask
                     ).generate(no_urls_no_tags)

plt.imshow(wordcloud)
plt.axis('off')
plt.savefig('./my_twitter_wordcloud_9.png', dpi=300)
plt.show()
print "Completed wordcloud generation"