# Predicting-Myers-Briggs

Predicting Myers-Briggs personality types by analyzing social-media posts.

## Goal of this project

To explore classifications methods on texta.

## Source

The data was acquired from [Kaggle](https://www.kaggle.com/datasnaek/mbti-type), which was taken from [Personality Cafe](https://www.personalitycafe.com/).

## Significant files

* Predicting MBTI.pdf - screenshots of the presentatin.
* analysis/
    - spaCy.ipynb - analyze the data with spaCy.
    - nltk.ipynb - analyze the data with Natural Language Toolkit.  Establish a baseline.
    - nltk_Under.ipynb - undersamples the data to address the class imbalance.
    - nltk_Over.ipynb - oversamples the data to address the class imbalance.
    - nltk_EI.ipynb - predicts the EI pair.
    - nltk_EI_Over.ipynb - oversamples the EI pair.
    - nltk_NS.ipynb - predicts the NS pair.
    - ntlk_NS_Over.ipynb - oversamples the NS pair.
    - nltk_FT.ipynb - predicts the FT pair.
    - nltk_JP.ipynb - predicts the JP pair.
* HTML/ - the presentation files.

## Tools

* CountVectorizer 
* TF-IDF
* Bag of words
* Over-sampling

## Future work

* Explore topic modeling.
* Explore spaCy more thoroughly.

## Notes

* I discovered that my work was erroneous during my presentation.  I was able to correct my notebooks, but the error remains in the presentation.
