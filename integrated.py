import warnings
from copy import deepcopy
warnings.filterwarnings("ignore")


class ObjectUsageError(Exception):
    pass


class CheckConditionError(Exception):
    pass


class UnsolvedError(Exception):
    pass


def handle_error(parser):
    func = parser.match
    history = (0, parser.name)

    def _f(objs, meta=None, partial=True):
        if not meta: raise CheckConditionError("Meta Information not defined yet!")
        res = func(objs, meta=meta)
        if res is None:
            c = meta.count
            r = meta.rdx
            for ch in objs[c:]:
                if ch is '\n':
                    r += 1
                    c += 1
                    continue
                break
            info = " ".join(objs[c:c + 10])
            if len(objs) > c + 10:
                info += '...'
            raise SyntaxError('''
Syntax Error at row {r}
   Error startswith :
{info}
'''.format(r=r, info=info))
        else:
            if not partial and len(objs) != meta.count:
                warnings.warn("Parsing unfinished.")
                c = meta.count
                r = meta.rdx
                for ch in objs[c:]:
                    if ch is '\n':
                        r += 1
                        c += 1
                        continue
                    break
                info = " ".join(objs[c:c + 10])
                if len(objs) > c + 10:
                    info += '...'
                raise SyntaxError('''
Syntax Error at row {r}
   Error startswith :
{info}
'''.format(r=r, info=info))
        return res

    return _f


# ====== Define Generic Type Params =============

WarningInfo = """
                You're trying to visit the elems that've been deprecated.
                If it occurred when you're using EBNFParser, report it as 
                a BUG at 
                `https://github.com/thautwarm/EBNFParser`. Thanks a lot!
            """

# ======

Undef = None


class Const:
    def __new__(self):
        raise ObjectUsageError("You're trying to new an instance with a module.")

    UnMatched = None
    NameFilter = 0
    RawFilter = 1
    RegexFilter = 2


class RecursiveFound(Exception):
    def __init__(self, node):
        self.node = node
        self.possibilities = []

    def add(self, possibility):
        self.possibilities.append(possibility)

    def __str__(self):
        s = '=====\n'
        s += self.node.name + '\n'
        s += '\n'.join(a.name + ' | ' + str([c.name for c in b])
                       for a, b in self.possibilities)
        return s


class Recur:
    def __new__(self, name, count):
        return (name, count)


class Trace:
    def __init__(self,
                 trace=Undef,
                 length=Undef):
        self.length = length if length is not Undef else \
            len(trace) if trace is not Undef else \
                0
        self.content = trace if trace is not Undef else \
            []
        self._Mem = len(self.content)

    def __iter__(self):
        yield from [elem for elem in self.content[:self.length]]

    def __getitem__(self, item):
        if isinstance(item, int):
            if item >= self.length:
                warnings.warn(WarningInfo)
            return self.content[item]
        elif isinstance(item, slice):
            if item.stop > self.length:
                warnings.warn(WarningInfo)
            return self.content[item]

    def append(self, elem):
        # reuse the memory cache
        if self.length == self._Mem:
            self.length += 1
            self._Mem += 1
            self.content.append(elem)
        elif self.length < self._Mem:
            self.content[self.length] = elem
            self.length += 1

    def new(self, constructor):
        # just can be used for Type `Trace[Contrainer[T]]`
        # reuse the memory cache
        if self.length == self._Mem:
            self.length += 1
            self._Mem += 1
            self.content.append(constructor())
        elif self.length < self._Mem:
            self.content[self.length].length = 0
            self.length += 1

    def pop(self):
        self.length -= 1
        assert self.length >= 0

    def where(self, obj):
        for idx, elem in enumerate(self.content[:self.length]):
            if elem is obj:
                return idx
        return Undef


# =============================
# Pattern Matching
# =============================

def Generate_RegexPatten_From(mode, escape=False):
    import re
    return re.compile(re.escape(mode)) if escape else re.compile(mode)


# The Reason why to repeat myself at the following three functions.
#    `Match_Char_By` `Match_Without_Regex_By`, `Match_With_Regex_By`
"""
    This pattern is the key to speed up the parser framework.
    For sure, I can abstract the way how the input string compares 
    with the parser's memeber `mode`, and then, these codes
        `if value == self.mode`
        `self.mode.fullmatch(value)`
    can be unified to 
        `if someFunc(value, mode)` or `if someFunc(value, self)`

    However, abstraction can have costly results.

"""


def Match_Char_By(self):
    def match(objs, meta, recur=None):
        try:
            value = objs[meta.count]
        except IndexError:
            return Const.UnMatched
        if value is self.mode:
            if value is '\n':
                meta.rdx += 1
            meta.new()
            return value
        return Const.UnMatched

    return match


def Match_Without_Regex_By(self):
    def match(objs, meta, recur=None):
        try:
            value = objs[meta.count]
        except IndexError:
            return Const.UnMatched
        if value == self.mode:
            if value is '\n':
                meta.rdx += 1
            meta.new()
            return value
        return Const.UnMatched

    return match


def Match_With_Regex_By(self):
    def match(objs, meta, recur=None):
        try:
            value = objs[meta.count]
        except IndexError:
            return Const.UnMatched
        if self.mode.fullmatch(value):
            if value is '\n':
                meta.rdx += 1
            meta.new()
            return value
        return Const.UnMatched

    return match


# =============================
# Parser
# =============================

def analyze(ebnf):
    if len(ebnf) is 1 or not all(ebnf): return None

    groups = dict()
    groupOrder = []

    for case in ebnf:
        groupId = case[0].name

        if groupId not in groupOrder:

            groups[groupId] = [case]
            groupOrder.append(groupId)
        else:
            groups[groupId].append(case)

    if len(groupOrder) is 1: return None

    return groups, groupOrder


def grammarRemake(groups, groupOrder):
    return [([groups[groupId][0][0], DependentAstParser(
        *[case[1:] for case in groups[groupId]])]
             if len(groups[groupId]) > 1 else
             groups[groupId][0])
            for groupId in groupOrder]


def optimize(ebnf):
    analyzed = analyze(ebnf)
    if analyzed is None:
        return ebnf
    groups, groupOrder = analyzed
    return grammarRemake(groups, groupOrder)


class Ignore:
    Value = 0
    Name = 1


class BaseParser:
    name = Undef
    has_recur = Undef

    def match(self, objs, meta, recur=Undef):
        raise Exception("There is no access to an abstract method.")
        # incomplete


class CharParser(BaseParser):
    def __init__(self, mode, name=Undef):
        length = len(mode)
        assert length is 1
        self.mode = mode
        self.name = "'{MODE}'".format(MODE=mode) if name is Undef else name
        self.match = Match_Char_By(self)


class StringParser(BaseParser):
    def __init__(self, mode,
                 name=Undef,
                 isRegex=False,
                 ifIsRegexThenEscape=False):
        self.name = name if name is not Undef else "'{MODE}'".format(MODE=mode)
        self.isRegex = isRegex

        if isRegex:
            self.mode = Generate_RegexPatten_From(mode, escape=ifIsRegexThenEscape)
            self.match = Match_With_Regex_By(self)
        else:
            self.mode = mode
            self.match = Match_Without_Regex_By(self)


class NotIn(StringParser):
    def __init__(self, mode,
                 name=Undef):
        self.name = name if name is not Undef else "'{MODE}'".format(MODE=mode)
        self.mode = mode

        def match(objs, meta, recur=None):
            try:
                value = objs[meta.count]
            except IndexError:
                return Const.UnMatched
            if value not in self.mode:
                if value is '\n':
                    meta.rdx += 1
                meta.new()
                return value
            return Const.UnMatched

        self.match = match


class Ref(BaseParser):
    def __init__(self, name): self.name = name


class AstParser(BaseParser):
    def __init__(self, *ebnf, name=Undef, toIgnore=Undef):
        # each in the cache will be processed into a parser.
        self.cache = optimize(ebnf)

        # the possible output types for an series of input tokenized words.
        self.possibilities = []

        # whether this parser will refer to itself.
        self.has_recur = False

        # the identity of a parser.

        self.name = name if name is not Undef else \
            ' | '.join(' '.join(map(lambda parser: parser.name, ebnf_i)) for ebnf_i in ebnf)

        # is this parser compiled, must be False when initializing.
        self.compiled = False

        #  if a parser's name is in this set, the result it output will be ignored when parsing.
        self.toIgnore = toIgnore

    def compile(self, namespace, recurSearcher):
        if self.name in recurSearcher:
            self.has_recur = True
            self.compiled = True
        else:
            recurSearcher.add(self.name)

        if self.compiled:
            return self

        for es in self.cache:
            self.possibilities.append([])

            for e in es:

                if isinstance(e, StringParser) or \
                        isinstance(e, CharParser):
                    self.possibilities[-1].append(e)

                elif isinstance(e, Ref):

                    e = namespace[e.name]

                    if isinstance(e, AstParser):
                        e.compile(namespace, recurSearcher)

                    self.possibilities[-1].append(e)

                    if not self.has_recur and e.has_recur:
                        self.has_recur = True

                elif isinstance(e, AstParser):

                    if e.name not in namespace:
                        namespace[e.name] = e
                    else:
                        e = namespace[e.name]

                    e.compile(namespace, recurSearcher)
                    self.possibilities[-1].append(e)

                    if not self.has_recur and e.has_recur:
                        self.has_recur = True

                else:
                    print(e)
                    raise UnsolvedError("Unknown Parser Type.")

        if hasattr(self, 'cache'):
            del self.cache

        if self.name in recurSearcher:
            recurSearcher.remove(self.name)

        if not self.compiled:
            self.compiled = True

    def match(self, objs, meta, recur=Undef):

        if self.has_recur and self in meta.trace[meta.count]:
            if isinstance(self, SeqParser) or recur is self:
                return Const.UnMatched

            raise RecursiveFound(self)

        meta.branch()

        if self.has_recur:
            meta.trace[meta.count].append(self)

        for possibility in self.possibilities:
            meta.branch()
            result = self.patternMatch(objs, meta, possibility, recur=recur)
            if result is Const.UnMatched:
                meta.rollback()
                continue
            elif isinstance(result, Ast):
                meta.pull()
                break
            elif isinstance(result, RecursiveFound):
                meta.rollback()
                break

        meta.pull()
        return result

    def patternMatch(self, objs, meta, possibility, recur=Undef):

        try:  # Not recur
            result = Ast(meta.clone(), self.name)
            for parser in possibility:
                r = parser.match(objs, meta=meta, recur=recur)

                # if `result` is still empty, it might not allow LR now.
                if isinstance(r, str) or isinstance(r, Ast):
                    resultMerge(result, r, parser, self.toIgnore)

                elif r is Const.UnMatched:
                    return Const.UnMatched

                elif isinstance(r, RecursiveFound):
                    raise r

                else:
                    raise UnsolvedError("Unsolved return type. {}".format(r.__class__))
            else:
                return result

        except RecursiveFound as RecurInfo:
            RecurInfo.add((self, possibility[possibility.index(parser) + 1:]))

            # RecurInfo has a trace of Beginning Recur Node to Next Recur Node with
            # specific possibility.
            if RecurInfo.node is not self:
                return RecurInfo

            return leftRecursion(objs, meta, possibility, RecurInfo)


def resultMerge(result, r, parser, toIgnore):
    if isinstance(parser, SeqParser) or isinstance(parser, DependentAstParser):

        if toIgnore is Undef:
            result.extend(r)
        else:
            result.extend([item for item in r if
                           ((item not in toIgnore[Const.RawFilter])
                            if isinstance(item, str) else
                            (item.name not in toIgnore[Const.NameFilter]))])
    else:
        if toIgnore is Undef:
            result.append(r)
        else:
            if isinstance(r, str):
                if r not in toIgnore[Const.RawFilter]:
                    result.append(r)
            elif r.name not in toIgnore[Const.NameFilter]:
                result.append(r)


def leftRecursion(objs, meta, RecurCase, RecurInfo):
    recur = RecurInfo.node
    for case in recur.possibilities:
        if case is RecurCase: continue
        meta.branch()
        veryFirst = recur.patternMatch(objs, meta, case, recur=recur)
        if isinstance(veryFirst, RecursiveFound) or veryFirst is Const.UnMatched:
            meta.rollback()
            continue
        else:
            meta.pull()
            first = veryFirst
            recurDeepCount = 0
            while True:
                meta.branch()
                for parser, possibility in RecurInfo.possibilities:

                    result = parser.patternMatch(objs, meta, possibility, recur=recur)
                    if result is Const.UnMatched:
                        meta.rollback()
                        return Const.UnMatched if recurDeepCount is 0 else veryFirst
                    elif isinstance(result, Ast):
                        result.appendleft(first)
                    elif isinstance(result, RecursiveFound):
                        raise UnsolvedError("Error occurs : found a new left recursion when handling an other.")
                    else:
                        raise UnsolvedError("Unsolved return from method `patternMatch`.")
                    first = result
                recurDeepCount += 1
                meta.pull()
                veryFirst = first
    else:
        # Fail to match any case.
        return Const.UnMatched


class DependentAstParser(AstParser): pass


class SeqParser(AstParser):
    def __init__(self, *ebnf, name=Undef, atleast=0, atmost=Undef):
        super(SeqParser, self).__init__(*ebnf, name=name)

        if atmost is Undef:
            if atleast is 0:
                self.name = "({NAME})*".format(NAME=self.name)
            else:
                self.name = '({NAME}){{{AT_LEAST}}}'.format(NAME=self.name, AT_LEAST=atleast)
        else:
            self.name = "({NAME}){{{AT_LEAST},{AT_MOST}}}".format(
                NAME=self.name,
                AT_LEAST=atleast,
                AT_MOST=atmost)
        self.atleast = atleast
        self.atmost = atmost

    def match(self, objs, meta, recur=Undef):

        result = Ast(meta.clone(), self.name)

        if meta.count == len(objs):  # boundary cases
            if self.atleast is 0:
                return result
            return Const.UnMatched

        meta.branch()
        matchedNum = 0
        if self.atmost is not Undef:
            """ (ast){a b} """
            while True:
                if matchedNum >= self.atmost:
                    break
                try:
                    r = super(SeqParser, self).match(objs, meta=meta, recur=recur)
                except IndexError:
                    break

                if r is Const.UnMatched:
                    break
                elif isinstance(r, RecursiveFound):
                    raise UnsolvedError("Cannot make left recursions in SeqParser!!!")
                result.extend(r)
                matchedNum += 1
        else:
            """ ast{a} | [ast] | ast* """
            while True:
                try:
                    r = super(SeqParser, self).match(objs, meta=meta, recur=recur)
                except IndexError:
                    break

                if r is Const.UnMatched:
                    break

                elif isinstance(r, RecursiveFound):
                    raise UnsolvedError("Cannot make left recursions in SeqParser!!!")

                result.extend(r)
                matchedNum += 1

        if matchedNum < self.atleast:
            meta.rollback()
            return Const.UnMatched

        meta.pull()
        return result


class MetaInfo:
    def __init__(self, count=0, rdx=0, trace=None, file_name=None):

        self.count = count
        if trace:
            self.trace = trace
        else:
            self.trace = Trace()
            self.trace.append(Trace())
        self.rdx = rdx
        self.history = []
        self.fileName = file_name if file_name else "<input>"

    def new(self):
        self.count += 1
        self.trace.new(Trace)

    def branch(self):
        """
        Save a record of parsing history in order to trace back.
        """
        self.history.append((self.count, self.rdx, self.trace[self.count].length))

    def rollback(self):
        """
        Trace back.
        """
        try:
            count, rdx, length = self.history.pop()
        except IndexError:
            return None
        self.count = count
        self.rdx = rdx
        self.trace.length = count + 1
        self.trace[count].length = length

    def pull(self):
        """
        Confirm the current parsing results.
        Pop a record in parsing history.
        """
        try:
            self.history.pop()
        except IndexError:
            raise Exception("pull no thing")

    def clone(self):
        """
        Get a copy of
                    (RowIdx,
                     NumberOfParsedWords,
                     FileName)
                    from current meta information.
        """
        return self.rdx, self.count, self.fileName

    def __str__(self):
        return """
--------------------
COUNT   : {COUNT}
ROW_IDX : {ROW_DIX}
TRACE   :
{TRACE}
--------------------
""".format(COUNT=self.count,
           ROW_DIX=self.rdx,
           TRACE='\n'.join(
               ['[' + (','.join([item.name for item in unit])) + ']' for unit in self.trace])
           )


class Trace:
    def __init__(self,
                 trace=None,
                 length=None):
        self.length = length if length is not None else \
            len(trace) if trace is not None else \
                0
        self.content = trace if trace is not None else \
            []
        self._Mem = len(self.content)

    def __iter__(self):
        yield from [elem for elem in self.content[:self.length]]

    def __getitem__(self, item):
        if isinstance(item, int):
            if item >= self.length:
                warnings.warn("....")
            return self.content[item]
        elif isinstance(item, slice):
            if item.stop > self.length:
                warnings.warn("....")
            return self.content[item]

    def append(self, elem):
        if self.length == self._Mem:
            self.length += 1
            self._Mem += 1
            self.content.append(elem)
        elif self.length < self._Mem:
            self.content[self.length] = elem
            self.length += 1

    def new(self, constructor):
        if self.length == self._Mem:
            self.length += 1
            self._Mem += 1
            self.content.append(constructor())
        elif self.length < self._Mem:
            self.content[self.length].length = 0
            self.length += 1

    def pop(self):
        self.length -= 1
        assert self.length >= 0

    def where(self, obj):
        for idx, elem in enumerate(self.content[:self.length]):
            if elem is obj:
                return idx


INDENT_UNIT = ' ' * 4


class Ast(list):
    def __init__(self, meta, name):
        super(Ast, self).__init__()
        self.name = name
        self.meta = meta

    def appendleft(self, obj):
        self.reverse()
        self.append(obj)
        self.reverse()

    def __str__(self):
        return self.dump()

    def dump(self, indent=0):
        next_indent = indent + 1
        return """{INDENT}{NAME}[
{CONTENT}
{INDENT}]""".format(INDENT=INDENT_UNIT * indent,
                    NAME=self.name,
                    CONTENT='\n'.join(
                        [
                            "{NEXT_INDENT}\"{STR}\"".format(NEXT_INDENT=INDENT_UNIT * next_indent, STR=node)
                            if isinstance(node, str) else \
                                node.dump(next_indent)

                            for node in self
                        ]))

    def dumpToJSON(self):
        return dict(name=self.name,
                    value=[node if isinstance(node, str) else \
                               node.dumpToJSON()
                           for node in self],
                    meta=self.meta)


class UnsolvedError(Exception):
    pass


import re


def __escape__(tk):
    if tk.startswith('R:'):
        return tk[2:]
    else:
        return re.escape(tk)
