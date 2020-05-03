
class Format(object):

    @staticmethod
    def remove_accents(t):
        acc = 'âäàåáêëèéïîìíóüçúûùññ'
        rep = 'aaaaaeeeeiiiioucuuunn'
        for e in zip(acc, rep):
            t = t.replace(e[0], e[1])
        #  from string import maketrans
        return t

    @staticmethod
    def remove_punc(t):
        punc = '?!,.()'
        for e in punc:
            t = t.replace(e[0], '')
        return t

    @staticmethod
    def lower(t):
        return t.lower()

    @staticmethod
    def remove(t, punc=True, accents=True, lower=True):
        if punc:
            t = Format.remove_punc(t)
        if accents:
            t = Format.remove_accents(t)
        if lower:
            t = Format.lower(t)
        return t
