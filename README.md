# cue-challenge

For the following challenge I chose the 3 facets:

1. prodType which are the 3 most mentioned music related nouns extracted from the review.  The dictionary for cross referencing these occurences was from manually observing which musical instruments occured in all reviews.
2. customerRating which is trying to determine the quality of the product based on how positive or negative the review is.  I used a positive and negative lexicon from https://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html.  And did a naive difference between the total count of positive words and the total count of negative words and taking and normalized it for how many words were in the total review.  This evaluates each word without context for negation, so I allowed for a larger range for neutral and negative reviews.
3. material which is the main thing the product is made of.  The lexicon for this was also created by manually scanning materials that occured in all reviews.
