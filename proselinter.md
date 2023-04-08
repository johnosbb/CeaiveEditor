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

cliches.garner is the check
"'thinking outside the box.' is cliché." is the message
The line number is 0
7 is the column (the start of the word thinking).
7 is the index in the text where the error starts (the start of the word thinking).
32 in the index in the text where the error ends. (after the full stop)
25 is the extent or length of the error (the length of the phrase: "thinking outside the box" in this case)
It is a warning
There are no suggested replacements

```
