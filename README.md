# Kneser-Ney Word Prediction

One technique used for predicting words in auto word suggestion software
is [Kneser-Ney smoothing](https://en.wikipedia.org/wiki/Kneser%E2%80%93Ney_smoothing),
which calculates the probabilities of n-grams given an initial training body of
text. It uses absolute discounting by substracting some discount `delta` from
the probability's lower order to filter out less frequent n-grams.

This is a PyQt application that demonstrates the use of Kneser-Ney in the
context of word suggestion. As words are typed into the text area, up to five
of the most probable continuing words are suggested at the top. Only bigrams
are considered, although Kneser-Ney could be extended to n-grams with a
recursive Kneser-Ney formula.

### Starting Up:

```
python3 src/app.py
```
