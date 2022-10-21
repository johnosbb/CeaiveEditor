# Lyrical
## The First Choice For Creative Writing

![Publications](https://github.com/johnosbb/Lyrical/blob/main/Lyrical.png?raw=true)

## Feasability Stage
Goal - Create a application for creative writers that has all the features of a fully fledged editor, grammar checking, spell checker, thesarus, but also incorporates natural language processing and AI to stylise writing based on the styles of the great writers.

### Features
- Full featured editor focused on designing a non-invasive workspace that allows the writer write free of distraction.
- The goals of the software is to make the job of creative writing easier. It does not focus on the formating and layout of documents, but instead creates simple uncluttered workspaces that promote the creative process.
- Grammar checking, Thesarus and reference tools can be invoked through the main editor when required.
- Lyrical will support the complete writing process. It provides support for storing research material, context information, links and meta data for the writers work.
- It will support templates for story arcs.



Research Phase began in January 2022

## Research Links

### Natural Language Programming

- [Paraphrasing](https://towardsdatascience.com/how-to-paraphrase-text-using-python-73b40a8b7e66)
- [Discussion on Paraphrasing](https://stackoverflow.com/questions/63598204/python-rephrasing-paraphrasing-options)


#### Academic References
- [Stylometry](https://en.wikipedia.org/wiki/Stylometry)
- [Natural Language Processing](https://en.wikipedia.org/wiki/Natural_language_processing)
- [Identifying Different Writing Styles in a Document Intrinsically Using Stylometric Analysis](https://github.com/Hassaan-Elahi/Writing-Styles-Classification-Using-Stylometric-Analysis)
- [A Framework for Authorship Identification of Online Messages: Writing-Style Features and Classification Techniques](https://www.pages.drexel.edu/~jl622/docs/Jounals/Zheng_2006JASIST_AuthorshipIdentification.pdf)
- [Text Analysis](https://monkeylearn.com/text-classification/)
- [Literary Style Classification with Deep Linguistic Analysis Features](https://nlp.stanford.edu/courses/cs224n/2011/reports/mjipeo-evion-wonhong.pdf)
- [Using Natural Language Processing to Categorize Fictional
Literature in an Unsupervised Manner](https://digitalcommons.du.edu/cgi/viewcontent.cgi?article=2739&context=etd)
- [Functional Words](https://corpora.files.wordpress.com/2021/03/6-2.e8ab96e88083efbc88tangefbc89e6a99fe883bde8aa9ee383aae382b9e38388.pdf)



#### Terminology

| Term | Definition  |
| --- | :-- |
| Stop Words | A stop word is a commonly used word (such as “the”, “a”, “an”, “in”) that we may wish to ignore when processing language. NLTK(Natural Language Toolkit) in python has a list of stopwords stored in 16 different languages. We can use these tables to eliminate these stop words when processing text for some aspects of style analysis.
| Synonym | a word or phrase that means exactly or nearly the same as another word or phrase in the same language, for example shut is a synonym of close.
| Synset | In Natural Language Processing a Synset or Synonym-set is a grouping of synonymous words that express the same concept. Some of the words have only one Synset and some have several.
| Stemming | In Natural Language Processing, stemming is the process of reducing inflected (or sometimes derived) words to their word stem, base or root form—generally a written word form. The stem need not be identical to the morphological root of the word; it is usually sufficient that related words map to the same stem, even if this stem is not in itself a valid root.
| Lemmatisation | Lemmatisation (or lemmatization) in linguistics is the process of grouping together the inflected forms of a word so they can be analysed as a single item, identified by the word's lemma, or dictionary form. Lemmatisation is closely related to stemming. The difference is that a stemmer operates on a single word without knowledge of the context, and therefore cannot discriminate between words which have different meanings depending on part of speech.


## Libraries
- [The Natural Language Toolkit Python](https://www.nltk.org/)
- [Natural Language Processing Javascript](https://www.kommunicate.io/blog/nlp-libraries-node-javascript/)
- [Scikit-Learn, Tools for predictive data analysis](https://scikit-learn.org/stable/index.html)
- [NTLK and Wordnet](https://www.nltk.org/howto/wordnet.html)
- [Epub Library for Python](https://github.com/aerkalov/ebooklib/tree/master/ebooklib)

### Grammar Checking
#### Language Tool

LanguageTool is an open source spellchecking platform. It supports a large variety of languages and has advanced grammar support. Language tool is also available as a hosted commercial service that also offers a limited free option. The API documentation is available [Here](https://languagetool.org/http-api/#/default)

- [Grammar Checking](https://www.geeksforgeeks.org/grammar-checker-in-python-using-language-check/)
- [Grammar Checking with Language Check - Python Example](https://pypi.org/project/language-check/)
- [Language Tool - Python Wrapper for Language Check](https://pypi.org/project/language-tool-python/)
- [pyLanguageTool Library](https://github.com/Findus23/pyLanguagetool)
- [language_tool_python](https://github.com/jxmorris12/language_tool_python)

#### Other Checkers 
- [Stanford Parser](https://nlp.stanford.edu/software/lex-parser.shtml)
- [ Discussion on Stack Overflow](https://stackoverflow.com/questions/10252448/how-to-check-whether-a-sentence-is-correct-simple-grammar-check-in-python)
- [After The Deadline](https://open.afterthedeadline.com/download/download-source-code/)
- [Parsing English in Python](https://explosion.ai/blog/parsing-english-in-python

### Spell Checking
- [Spell Checking](https://pyenchant.github.io/pyenchant/)
- [Github page for Enchant](https://github.com/pyenchant/pyenchant)
- [Integrating spellchecking into a QTextEdit widget in PyQt5 with enchant](https://nethumlamahewage.medium.com/integrating-spellchecking-into-a-qtextedit-widget-in-pyqt5-with-enchant-f025f4097e5c)
- [Code for above article](https://gist.github.com/NethumL/264a0468ea8b041c7e51038e23de0752)
- [SpellChecker and TextBlob](https://www.askpython.com/python/examples/spell-checker-in-python)
- [Pure Python Spell Checking](https://pypi.org/project/pyspellchecker/)


### Finding Rhyming Words
- [Rhymes with NLP](https://www.garysieling.com/blog/rhyming-with-nlp-and-shakespeare/)
- [Metaphone](https://pypi.org/project/Metaphone/)

# Installing Enchant on Ubuntu

- On Ubuntu: sudo apt-get install -y libenchant-dev
- sudo apt-get -y install enchant

## Development Options
- [PyInstaller](https://pypi.org/project/pyinstaller/)
- [PyQT](https://pythonbasics.org/install-pyqt/)
- [PyQT Documentation](https://doc.qt.io/qtforpython/contents.html)
- [TkInter versus PyQT](https://dm4rnde.com/py-gui-soluts-tkinter-comp-to-pyqt5)
- [Guide to Toolbars, Menus and Status Bars](https://realpython.com/python-menus-toolbars/)

### QT Designer and Layout
- [Designer Tutorial](https://realpython.com/qt-designer-python/#getting-started-with-qt-designer)
- [Dockable Windows](https://www.tutorialspoint.com/pyqt5/pyqt5_qdockwidget.htm)
- [Frameless Windows](https://www.youtube.com/watch?v=bJBwSyHUobg)
- [Layout Options](https://realpython.com/python-pyqt-layout/)
- [Resource files](https://www.pythonguis.com/tutorials/packaging-data-files-pyqt5-with-qresource-system/)
- [Styling with Style Sheets](https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qpushbutton)

## Editor References
- [Python Rich Text Editor](https://www.pythonguis.com/examples/python-rich-text-editor/)
  - [Github Reference](https://github.com/Macmillan2004/My-Microsoft-Word)
- [No2Pads](https://www.pythonguis.com/examples/python-notepad-clone/)
- [Building a Text Editor in Python and QT](https://www.binpress.com/building-text-editor-pyqt-1/)
- [Axel Erfurt](https://gist.github.com/Axel-Erfurt/8c84b5e70a1faf894879cd2ab99118c2)

## Python
- [Under Score Conventions and Rules in Python](https://ericplayground.com/2019/03/26/underscore-naming-convention-in-python/)
- [Source Code for Beginning PyQT](https://github.com/Apress/beginning-pyqt)
- [Tree Widget and JSON](https://stackoverflow.com/questions/51506378/pyqt-recursively-adding-children-to-treewidget-dynamically)
- [Using JSON with Python](https://oxylabs.io/blog/python-parse-json)
- [Example of Syntax High Lighting](https://github.com/baoboa/pyqt5/blob/master/examples/richtext/syntaxhighlighter.py)
- [Simple Syntax Highlighting](https://wiki.python.org/moin/PyQt/Python%20syntax%20highlighting)
- [More detailed discussion on highlighting](https://stackoverflow.com/questions/27716625/qtextedit-change-font-of-individual-paragraph-block)
- [PYQT5 Examples](https://github.com/baoboa/pyqt5/tree/master/examples)
- [Python Typing - Type Hints & Annotations](https://www.youtube.com/watch?v=QORvB-_mbZ0)
- [Vocabulary Bot](https://www.twilio.com/blog/build-vocabulary-bot-whatsapp-python-twilio)
- [Guide to PYQT](https://doc.qt.io/qtforpython/overviews/model-view-programming.html)
- [Python Environments](https://code.visualstudio.com/docs/python/environments)
- [Web Scrapping and 403 errors](https://www.pythonpool.com/urllib-error-httperror-http-error-403-forbidden/)
- [TextBlob - Parts of Speech Processing](https://textblob.readthedocs.io/en/dev/)
- [Lector Epub Reader](https://github.com/BasioMeusPuga/Lector/tree/master/lector/readers)
- [pygments - lexer](https://pygments.org/docs/quickstart/)

# Literature

## Source Material
- [Project Gutenberg catalogue](https://gnikdroy.pythonanywhere.com/docs/#installation-and-setup)
- [WordNet® is a large lexical database of English](https://wordnet.princeton.edu/download)
- [Literary Quotes Research](https://guides.loc.gov/quotations/online)
- [Dictionary of Similes](https://www.bartleby.com/161/)
- [Roget’s Thesaurus as a lexical resource](https://arxiv.org/ftp/arxiv/papers/1204/1204.0140.pdf)

## Short Stories

- [Short Story Guidelines](https://www.turnerstories.com/blog/2019/3/1/how-to-structure-a-short-story)

# Writers Aids
- [Describing Colour](https://www.writerswrite.co.za/204-words-that-describe-colours/)
- [Encycolorpedia](https://encycolorpedia.com/named)
- [Words for smell](https://www.writerswrite.co.za/75-words-that-describe-smells/)


# Online Tools

- [The Free Thesaurus](https://www.freethesaurus.com/picked)
- [API to Merriam-Webster](https://dictionaryapi.com/products/json)
- [Old Python Wrappers for Merriam-Webster API](https://github.com/pfeyz/merriam-webster-api)
- [Quillbot - API in Python](https://github.com/Anu-bhav/Paraphrasing/blob/master/paraphrasing.py)
- [Quillbot](https://quillbot.com/)
- [Describing Words](https://describingwords.io/)
- [Gutenberg Project](https://www.gutenberg.org/policy/robot_access.html)


# Additional Information

- There is additional information available on the [Wiki](https://github.com/johnosbb/Lyrical/wiki)
