# Prose Linter


## Reference

- [proselint on github](https://github.com/amperser/proselint)



## Notes

Proselint returns a suggestion with the following properties


```python

{
  // Type of check that output this suggestion.
  check: "wallace.uncomparables",

  // Message to describe the suggestion.
  message: "Comparison of an uncomparable: 'unique' cannot be compared.",

  // The person or organization giving the suggestion.
  source: "David Foster Wallace"

  // URL pointing to the source material.
  source_url: "http://www.telegraph.co.uk/a/9715551"

  // Line where the error starts.
  line: 0,

  // Column where the error starts.
  column: 10,

  // Index in the text where the error starts.
  start: 10,

  // Index in the text where the error ends.
  end: 21,

  // length from start -> end
  extent: 11,

  // How important is this? Can be "suggestion", "warning", or "error".
  severity: "warning",

  // Possible replacements.
  replacements: [
    {
      value: "unique"
    }
  ]
}
```

As an example, for the line: "He was thinking outside the box."

Proselint returns:
```txt
[('cliches.garner', "'thinking outside the box.' is cliché.", 0, 7, 7, 32, 25, 'warning', None)]

where

Index[0] -  cliches.garner is the check
Index[1] -  "'thinking outside the box.' is cliché." is the message
Index[2] -  The line number is 0
Index[3] -  7 is the column (the start of the word thinking).
Index[4] -  7 is the index in the text where the error starts (the start of the word thinking).
Index[5] -  32 in the index in the text where the error ends. (after the full stop)
Index[6] -  25 is the extent or length of the error (the length of the phrase: "thinking outside the box" in this case)
Index[7] -  It is a warning
Index[8] -  There are no suggested replacements

```


## More examples

```pyhton
String: He was thinking outside the box. -> Suggestions: [('cliches.garner', "'thinking outside the box.' is cliché.", 0, 7, 7, 32, 25, 'warning', None)]


String: under the weather. -> Suggestions: [('cliches.write_good', "'under the weather.' is a cliché.", 0, 1, 1, 18, 17, 'warning', None)]


String: She swam by a bunch of oysters. -> Suggestions: [('oxford.venery_terms', "The venery term is 'a bed of oysters'.", 0, 12, 12, 31, 19, 'warning', 'a bed of oysters')]


String: A girl with colitis goes by. -> Suggestions: []


String: The building is deceptively large. -> Suggestions: [('skunked_terms.misc', "'deceptively' is a bit of a skunked term, impossible to use without issue. Find some other way to say it.", 0, 16, 16, 28, 12, 'warning', None)]


String: and so I said PLEASE STOP YELLING! -> Suggestions: [('leonard.exclamation.30ppm', 'More than 30 ppm of exclamations. Keep them under control.', 0, 33, 33, 34, 1, 'warning', None)]


String: He was academicly superior. -> Suggestions: [('spelling.ally_ly', "-ally vs. -ly. 'academically' is the correct spelling.", 0, 7, 7, 18, 11, 'warning', 'academically'), ('spelling.misc', "Misspelling. 'academically' is the preferred spelling.", 0, 7, 7, 18, 11, 'warning', 'academically')]


String: Get ready: button your seatbelts. -> Suggestions: [('mixed_metaphors.misc.misc', "Mixed metaphor. Try 'fasten your seatbelts'.", 0, 11, 11, 33, 22, 'warning', 'fasten your seatbelts')]


String: There were approximately about 5 atm machines. -> Suggestions: [('redundancy.garner', "Redundancy. Use 'approximately' instead of 'approximately about'.", 0, 11, 11, 31, 20, 'warning', 'approximately')]

```
