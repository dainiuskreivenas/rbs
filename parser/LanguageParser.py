"""

Context free grammer language parser.
Usage:

parser = LanguageParser()

parser.parseSentence("I saw the dog")

"""
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

from rbs import RBS

class LanguageParser:

    def addGrammerRules(self):
        self.rbs.addRule(
            (
                "S<NP+VP",
                (
                    [
                        (True, "NP", ("?np", "?p1", "?p2"),"np"),
                        (True, "VP", ("?vp", "?p2", "?p3"),"vp"),
                    ],
                    [
                        ("assert", ("S", (("+", "?np", "?vp"), "?p1","?p3"))),
                        ("retract", "np"),
                        ("retract", "vp")
                    ]
                )
            )
        )

        self.rbs.addRule(
            (
                "NP<ART+NOUN",
                (
                    [
                        (True, "ART", ("?art", "?p1", "?p2"), "art"),
                        (True, "NOUN", ("?noun", "?p2", "?p3"), "noun")
                    ],
                    [
                        ("assert", ("NP", (("+", "?art", "?noun"), "?p1","?p3"))),
                        ("retract", "art"),
                        ("retract", "noun")
                    ]
                )
            )
        )

        self.rbs.addRule(
            (
                "NP<NAME",
                (
                    [
                        (True, "NAME", ("?name", "?p1","?p2"), "name")
                    ],
                    [
                        ("assert", ("NP", ("?name", "?p1","?p2"))),
                        ("retract", "name"),
                    ]
                )
            )
        )

        self.rbs.addRule(
            (
                "VP<VERB+NP",
                (
                    [
                        (True, "VERB", ("?verb", "?p1","?p2"), "verb"),
                        (True, "NP", ("?np" ,"?p2", "?p3"), "np")
                    ],
                    [
                        ("assert", ("VP", (("+", "?verb", "?np"), "?p1","?p3"))),
                        ("retract", "verb"),
                        ("retract", "np")
                    ]
                )
            )
        )
    
    def addArt(self, art):
        self.rbs.addRule(
            (
                "art-"+art,
                (
                    [
                        (True, "WORD", (art.upper(), "?s", "?e"), "word")
                    ],
                    [
                        ("assert", ("ART", (art, "?s", "?e"))),
                        ("retract", "word")
                    ]
                )
            )
        )
    
    def addNounPhrase(self, np):
        self.rbs.addRule(
            (
                "nounphrase-"+np,
                (
                    [
                        (True, "WORD", (np.upper(), "?s", "?e"), "word")
                    ],
                    [
                        ("assert", ("NP", (np, "?s", "?e"))),
                        ("retract", "word")
                    ]
                )
            )
        )

    def addVerb(self, verb):
        self.rbs.addRule(
            (
                "verb-"+verb,
                (
                    [
                        (True, "WORD", (verb.upper(), "?s", "?e"), "word")
                    ],
                    [
                        ("assert", ("VERB", (verb, "?s", "?e"))),
                        ("retract", "word")
                    ]
                )
            )
        )

    def addNoun(self, noun):
        self.rbs.addRule(
            (
                "noun-"+noun,
                (
                    [
                        (True, "WORD", (noun.upper(), "?s", "?e"), "word")
                    ],
                    [
                        ("assert", ("NOUN", (noun, "?s", "?e"))),
                        ("retract", "word")
                    ]
                )
            )
        )

    def addName(self, name):
        self.rbs.addRule(
            (
                "name-"+name,
                (
                    [
                        (True, "WORD", (name.upper(), "?s", "?e"), "word")
                    ],
                    [
                        ("assert", ("NAME", (name, "?s", "?e"))),
                        ("retract", "word")
                    ]
                )
            )
        )

    def addLexicon(self):
        # Names
        self.addName("John")

        # Noun Phrases
        self.addNounPhrase("I")

        # Verbs
        self.addVerb("Saw")
        self.addVerb("Ate")

        # Articles
        self.addArt("The")
        self.addArt("A")
        self.addArt("An")

        # Nouns
        self.addNoun("Dog")
        self.addNoun("Cat")

    def __init__(self):
        self.rbs = RBS()
        self.addGrammerRules()
        self.addLexicon()
        
    def parseSentence(self, sentence):
        words = sentence.split(" ")
        for i,word in enumerate(words):
            self.rbs.addFact(("WORD", (word.upper(),i+1,i+2)))
