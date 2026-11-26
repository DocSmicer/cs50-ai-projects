# Analysis

## Layer 2, Head 1

This head appears to direct most tokens' attention to the [MASK] token. In the
diagram, nearly every row is brightest in the [MASK] column regardless of the
word's part of speech, suggesting the head gathers information about the
masked position so the model can use the surrounding sentence to predict it.

Example Sentences:
- Maria handed the book to John because [MASK] had asked for it.
- The chef sliced the [MASK] before dinner.

## Layer 3, Head 11

This head appears to connect a verb with its direct object. In the diagrams,
the row for the verb ("handed", "chased") is brightest at the object noun
("book", "ball"), and the noun sometimes attends back to the verb. In one
sentence the pronoun "it" also attended strongly to its antecedent "book", but
this did not repeat in the second sentence, so the head is not a reliable
pronoun resolver.

Example Sentences:
- Maria handed the book to John because [MASK] had asked for it.
- The dog chased the ball until it rolled under the [MASK].
