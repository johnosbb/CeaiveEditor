from typing import Callable
import language_tool_python
from PyQt5.QtCore import pyqtSignal, QObject, pyqtSlot
from PyQt5.QtGui import QTextDocument, QTextBlockUserData
import logging
import proselint
from rule import Rule

options = {
    "max_errors": 1000,
    "checks": {
        "airlinese.misc": True,
        "annotations.misc": True,
        "archaism.misc": True,
        "cliches.hell": True,
        "cliches.misc": True,
        "consistency.spacing": True,
        "consistency.spelling": True,
        "corporate_speak.misc": True,
        "cursing.filth": True,
        "cursing.nfl": False,
        "cursing.nword": True,
        "dates_times.am_pm": True,
        "dates_times.dates": True,
        "hedging.misc": True,
        "hyperbole.misc": True,
        "jargon.misc": True,
        "lexical_illusions.misc": True,
        "lgbtq.offensive_terms": True,
        "lgbtq.terms": True,
        "links.broken": False,
        "malapropisms.misc": True,
        "misc.apologizing": True,
        "misc.back_formations": True,
        "misc.bureaucratese": True,
        "misc.but": True,
        "misc.capitalization": True,
        "misc.chatspeak": True,
        "misc.commercialese": True,
        "misc.composition": True,
        "misc.currency": True,
        "misc.debased": True,
        "misc.false_plurals": True,
        "misc.illogic": True,
        "misc.inferior_superior": True,
        "misc.institution_name": True,
        "misc.latin": True,
        "misc.many_a": True,
        "misc.metaconcepts": True,
        "misc.metadiscourse": True,
        "misc.narcissism": True,
        "misc.not_guilty": True,
        "misc.phrasal_adjectives": True,
        "misc.preferred_forms": True,
        "misc.pretension": True,
        "misc.professions": True,
        "misc.punctuation": True,
        "misc.scare_quotes": True,
        "misc.suddenly": True,
        "misc.tense_present": True,
        "misc.waxed": True,
        "misc.whence": True,
        "mixed_metaphors.misc": True,
        "mondegreens.misc": True,
        "needless_variants.misc": True,
        "nonwords.misc": True,
        "oxymorons.misc": True,
        "psychology.misc": True,
        "redundancy.misc": True,
        "redundancy.ras_syndrome": True,
        "skunked_terms.misc": True,
        "spelling.able_atable": True,
        "spelling.able_ible": True,
        "spelling.ally_ly": True,
        "spelling.ance_ence": True,
        "spelling.athletes": True,
        "spelling.ely_ly": True,
        "spelling.em_im_en_in": True,
        "spelling.er_or": True,
        "spelling.in_un": True,
        "spelling.misc": True,
        "spelling.ve_of": True,
        "security.credit_card": True,
        "security.password": True,
        "sexism.misc": True,
        "terms.animal_adjectives": True,
        "terms.denizen_labels": True,
        "terms.eponymous_adjectives": True,
        "terms.venery": True,
        "typography.diacritical_marks": True,
        "typography.exclamation": True,
        "typography.symbols": True,
        "uncomparables.misc": True,
        "weasel_words.misc": True,
        "weasel_words.very": True
    }
}

# background worker


class LintCheck(QObject):

    result = pyqtSignal()

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.__suggestions = {}
        self.__rules = []
        self.content = ""

    @pyqtSlot()
    def start(self): print("Thread started")

    def getErrors(self):
        return self.__suggestions

    def getCorrection(self) -> str:
        return self.tool.correct(self.content)

    def setText(self, text: str):
        self.content = text

    def convertSuggestionsToRules(self, suggestions, sentence):
        ruleKeys = ("ruleId", "context", "sentence", "category", "ruleIssueType",
                    "replacements", "message", "offsetInContext", "offset", "errorLength")
        self.__rules = []
        for suggestion in suggestions:
            print("suggestion {} for sentence {} {} {}".format(
                suggestion, sentence, suggestion[3], suggestion[5]))
            rule_dict = dict.fromkeys(ruleKeys)
            rule = Rule(rule_dict)
            rule.ruleId = -1
            rule.context = suggestion[1]
            rule.sentence = sentence
            rule.category = suggestion[0]
            rule.ruleIssueType = suggestion[1]
            rule.replacements = suggestion[8]
            rule.message = suggestion[1]
            rule.offsetInContext = suggestion[4]
            if(suggestion[8] == None):
                rule.replacements = [suggestion[1]]
                rule.matchedText = ""
            else:
                rule.matchedText = sentence[int(
                    suggestion[3]): int(suggestion[5])]
            rule.offset = suggestion[4]
            rule.errorLength = suggestion[6]
            self.__rules.append(rule)

    def showSuggestion(self):
        index = 0
        for match in self.__suggestion:
            index = index + 1
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

    @ pyqtSlot(QTextDocument)
    def checkDocument(self, document):
        for blockIndex in range(document.blockCount()):
            logging.debug("Finding rules for block {}".format(blockIndex))
            block = document.findBlockByNumber(blockIndex)
            logging.debug("Block Text: {}".format(block.text()))
            self.checkSection(block, blockIndex)
        self.result.emit()

    def checkSection(self, block, blockIndex):
        logging.debug("lintCheck: Checking Section: {}".format(block.text()))
        self.content = block.text()
        # self.content = "He was thinking outside the box."
        if(self.content != ""):
            self.__suggestions = proselint.tools.lint(
                self.content, config=options)
            if(len(self.__suggestions) > 0):
                print("Suggestions: {}".format(self.__suggestions))
                self.convertSuggestionsToRules(
                    self.__suggestions, self.content)
                # self.__matches = self.__tool.check(self.content)
                logging.debug("lintCheck: checking Section: found {} rules for block {} containing text: {} ".format(
                    self.__rules, blockIndex, block.text()))
                userData = QTextBlockUserData()
                userData.value = self.__rules
                block.setUserData(userData)
            else:
                print("No suggestions found for text")
        else:
            logging.debug("lintCheck: checkSection: Nothing to check")

        # we will now have a set of matches and each of these relates to a section of text in the given text block.
        # We can return these as a collection of corrections
        # The calling program should ideally present these as a correction option when:
        # (a) Someone hovers over that section of text or
        # (b) As a panel of issues which can be corrected by clicking on the relevant issue

    @ property
    def rules(self):
        return self.__suggestions

    @ rules.setter
    def textToCorrect(self, theRules):
        self.__suggestions = theRules
