import re
class Expr:
    def __init__(self, op, args=None):
        self.op = op
        self.args = args #ex: "Genre(Pop) & !Genre(Rock)", Artists(Michael Jackson)
        self.value = True

    def __eq__(self, other):
        return isinstance(other, Expr) and self.op == other.op and self.args == other.args

class Song:
    def __init__(self, title, artist, genre):
        self.title = title
        self.artist = artist
        self.genre = genre

class KnowledgeBase:
    def __init__(self):
        self.clauses = []

    #Stores the do not recommend lists/ recommend lists

    #
    def tell(self, sentence):
        prop = self.sentenceToExpr(sentence)
        self.clauses.append(prop)

    def like_genre(self, genre):
        genre_like_prop = self.find(f"Genre({genre})")
        if genre_like_prop:
            return True
        return False

    def dislike_genre(self, genre):
        genre_dislike_prop = self.find(f"!Genre({genre})")
        if genre_dislike_prop:
            return True
        return False

    def like_artist(self, artist):
        artist_like_prop = self.find(f"Artist({artist})")
        if artist_like_prop:
            return True
        return False

    def dislike_artist(self, artist):
        artist_dislike_prop = self.find(f"!Artist({artist})")
        if artist_dislike_prop:
            return True
        return False

    def retract(self, sentence):
        """Remove the sentence's clauses from the KB."""
        exp = self.sentenceToExpr(sentence)
        for c in self.clauses:
            if c == exp:
                self.clauses.remove(c)

    def sentenceToExpr(self, sentence):
        op = re.findall(r'(?<=\w)\s*&\s*(?=\w)', sentence)
        if ' & ' in op:
            op = '&'
            args = re.split(r'\s*&\s*(?![^(]*\))', sentence)
            return Expr(op, args)
        return Expr(sentence)

    def find(self, exp):
        if exp in (True, False):
            return exp
        for c in self.clauses:
            if c.op == exp:
                return True
            if c.args is not None:
                args = c.args
                if exp in args:
                    return True
        return False

    def printClauses(self):
        str = ""
        for clause in self.clauses:
            if clause.op == '&':
                for arg in clause.args:
                    str += arg + ' & '
                str.rstrip(" &")
                print(str)
            else:
                str = clause.op
                print(str)

# Test Cases
#kb = KnowledgeBase()
#kb.tell("Genre(Pop) & !Genre(Rock) & Artist(Hello & Me) & !Artist(Love You)")
#kb.printClauses()
#print(kb.like_genre("Pop"))
#print(kb.like_genre("Rock"))
#print(kb.dislike_genre("Rock"))
#print(kb.like_artist("Hello & Me"))
#print(kb.dislike_artist("Hello & Me"))
#print(kb.dislike_artist("Love You"))
#print("")
#kb.retract("Genre(Pop) & !Genre(Rock) & Artist(Hello & Me) & !Artist(Love You)")
#print(kb.like_genre("Pop"))
#print(kb.like_genre("Rock"))
#print(kb.dislike_genre("Rock"))
#print(kb.like_artist("Hello & Me"))
#print(kb.dislike_artist("Hello & Me"))
#print(kb.dislike_artist("Love You"))
#kb.printClauses()
