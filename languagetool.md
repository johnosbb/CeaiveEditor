# LanguageTool

## References

- [LanguageTool on Github](https://github.com/jxmorris12/language_tool_python)


## Notes

The match or rule in language tool has the following properties

```python
    print("Match: {}\n".format(index))
    print("Rule ID: {}\n".format(match.ruleId))
    print("Context: {}\n".format(match.context))
    print("Sentence: {}\n".format(match.sentence))
    print("Category: {}\n".format(match.category))
    print("Rule Issue Type: {}\n".format(match.ruleIssueType))
    print("Replacements: {}\n".format(match.replacements))
    print("Messages: {}\n".format(match.message))
    print("Offset: {}\n".format(match.offsetInContext))
    print("Offset in context: {}\n".format(match.offset))
    print("Error Length: {}\n".format(match.errorLength))
 ```
