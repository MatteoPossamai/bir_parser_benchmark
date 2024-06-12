from pyparsing import Keyword, Word, nums, oneOf, OneOrMore, ZeroOrMore, Suppress, Literal, Forward, alphanums, Combine, White, Or
from typing import Union

LBRACE, RBRACE = map(Suppress, "()")

# Predicates
BIExp_Equal = Keyword('BIExp_Equal')
BIExp_NotEqual = Keyword('BIExp_NotEqual')
BIExp_LessThan = Keyword('BIExp_LessThan')
BIExp_SignedLessThan = Keyword('BIExp_SignedLessThan')
BIExp_LessOrEqual = Keyword('BIExp_LessOrEqual')
BIExp_SignedLessOrEqual = Keyword('BIExp_SignedLessOrEqual')

# Unary Operators
BIExp_Not = Keyword('BIExp_Not')
BIExp_ChangeSign = Keyword('BIExp_ChangeSign')

# Binary Operators
BIExp_And = Keyword('BIExp_And')
BIExp_Or = Keyword('BIExp_Or')
BIExp_Xor = Keyword('BIExp_Xor')
BIExp_Plus = Keyword('BIExp_Plus')
BIExp_Minus = Keyword('BIExp_Minus')
BIExp_Mult = Keyword('BIExp_Mult')
BIExp_Div = Keyword('BIExp_Div')
BIExp_SignedDiv = Keyword('BIExp_SignedDiv')
BIExp_Mod = Keyword('BIExp_Mod')
BIExp_SignedMod = Keyword('BIExp_SignedMod')
BIExp_LeftShift = Keyword('BIExp_LeftShift')
BIExp_RightShift = Keyword('BIExp_RightShift')
BIExp_SignedRightShift = Keyword('BIExp_SignedRightShift')

# Binary Cast
BIExp_UnsignedCast = Keyword('BIExp_UnsignedCast')
BIExp_SignedCast = Keyword('BIExp_SignedCast')
BIExp_HighCast = Keyword('BIExp_HighCast')
BIExp_LowCast = Keyword('BIExp_LowCast')

# Class definitions for each node in the AST.
class Node(object):
    def __init__(self, tokens):
        self._tokens = tokens

# Main operators
BExp_UnaryExp = Keyword('BExp_UnaryExp')
BExp_BinExp = Keyword('BExp_BinExp')
BExp_BinPred = Keyword('BExp_BinPred')
BExp_Const = Keyword('BExp_Const')
BExp_IfThenElse = Keyword('BExp_IfThenElse')
BExp_Den = Keyword('BExp_Den')
BExp_Load = Keyword('BExp_Load')
BExp_Store = Keyword('BExp_Store')
BExp_Cast = Keyword('BExp_Cast')

# Endian format
BEnd_LittleEndian = Keyword('BEnd_LittleEndian')
BEnd_BigEndian = Keyword('BEnd_BigEndian')
BEnd_NoEndian = Keyword('BEnd_NoEndian')

# Bit dimensions
Bit1 = Keyword('Bit1')
Bit8 = Keyword('Bit8')
Bit16 = Keyword('Bit16')
Bit32 = Keyword('Bit32')
Bit64 = Keyword('Bit64')
Bit128 = Keyword('Bit128')

# Var keyword
BVar = Keyword('BVar')

# Aggregators
buop = [BIExp_Not, BIExp_ChangeSign]
bop = [BIExp_And, BIExp_Or, BIExp_Xor, BIExp_Plus, BIExp_Minus, BIExp_Mult, BIExp_Div, BIExp_SignedDiv, BIExp_Mod, BIExp_SignedMod, BIExp_LeftShift, BIExp_RightShift, BIExp_SignedRightShift]
bpred = [BIExp_Equal, BIExp_NotEqual, BIExp_LessThan, BIExp_SignedLessThan, BIExp_LessOrEqual, BIExp_SignedLessOrEqual]
bimmt = [Bit1, Bit8, Bit16, Bit32, Bit64, Bit128]
bcast = [BIExp_UnsignedCast, BIExp_SignedCast, BIExp_HighCast, BIExp_LowCast]
endians = [BEnd_LittleEndian, BEnd_BigEndian, BEnd_NoEndian]

bv_val = Combine(ZeroOrMore(LBRACE) + ZeroOrMore(White()) + Literal('bv') + OneOrMore(White())+ OneOrMore(Word(nums)) + OneOrMore(White()) + \
    oneOf(' '.join(str(keyword)[1:-1] for keyword in bimmt)) + ZeroOrMore(White()) + ZeroOrMore(RBRACE))
var_val = Combine(ZeroOrMore(LBRACE) +  OneOrMore(Word(alphanums)) + ZeroOrMore(RBRACE))
value = OneOrMore(Word(nums))
typ = Literal('bv')


class Constant(Node):
    typ: str
    val: int
    data_type: str

    def __init__(self, tokens):
        self.typ = tokens[0]
        self.val = tokens[1]
        self.data_type = tokens[2]
        if self.val == "#":
            pass
        else:
            self.val = int(self.val)
            if self.val > 2**int(self.data_type[3:]) - 1:
                raise Exception("Number out of bounds for the given data type.")

    def __str__(self) -> str:
        return f"({self.typ} {self.val} {self.data_type})"

    def __repr__(self) -> str:
        return f"({self.typ} {self.val} {self.data_type})"

    def __eq__(self, value: object) -> bool:
        return self.typ == value.typ and self.val == value.val and self.data_type == value.data_type


class Variable(Node):
    reference: str

    def __init__(self, tokens):
        self.reference = tokens[1]

    def __str__(self) -> str:
        return f"{self.reference}"

    def __repr__(self) -> str:
        return f"{self.reference}"

    def __eq__(self, value: object) -> bool:
        return self.reference == value.reference


def build_const_value():
    bs_expr = (
        ZeroOrMore(LBRACE) + typ + ZeroOrMore(value) + ZeroOrMore(Literal("#")) + oneOf(' '.join(str(keyword)[1:-1] for keyword in bimmt)) + ZeroOrMore(RBRACE)
    )

    bs_expr.setParseAction(Constant)
    return bs_expr


def build_variable_expr():
    bs_expr = (
        ZeroOrMore(LBRACE) + BVar + var_val + ZeroOrMore(RBRACE)
    )

    bs_expr.setParseAction(Variable)
    return bs_expr

ALLOWED_DEN_VALUES = {"MEM"}
HIGHEST_REGISTER = 16

# Expressions
class BEXP(Node):
    keyword: str
    repr: str
    value: Union[str, int, 'BEXP', Constant]
    value2: Union[str, int, None, 'BEXP', Constant]
    operation: str | None
    predicate: str | None
    condition: Union['BEXP', None]
    reference: str | None
    data_type: str | None
    address: Union[str, int, 'BEXP', Constant]

    def __init__(self, tokens):
        self.keyword = tokens[0]
        if self.keyword == BExp_Const:
            self.value = tokens[1]
            self.repr = f"{self.keyword} ({self.value})"
        elif self.keyword == BExp_UnaryExp: # Unary Expression Parsing
            self.operation = tokens[1]
            self.value = tokens[2]
            self.repr = f"{self.keyword} {self.operation} {self.value}"
        elif self.keyword == BExp_BinExp: # Binary Expression Parsing 
            self.operation = tokens[1]
            self.value = tokens[2]
            self.value2 = tokens[3]
            self.repr = f"{self.keyword} {self.operation} {self.value}"
        elif self.keyword == BExp_BinPred: # Binary Predicate Parsing 
            self.predicate = tokens[1]
            self.value = tokens[2]
            self.value2 = tokens[3]
            self.repr = f"{self.keyword} {self.predicate} {self.value} {self.value2}"
        elif self.keyword == BExp_IfThenElse: # If Then Else Parsing
            self.condition = tokens[1]
            self.value = tokens[2]
            self.value2 = tokens[3]
            self.repr = f"{self.keyword} {self.condition} {self.value} {self.value2}"
        elif self.keyword == BExp_Den:
            if tokens[1].reference in ALLOWED_DEN_VALUES or (tokens[1].reference.startswith("R") and (int(tokens[1].reference[1:]) <= HIGHEST_REGISTER and int(tokens[1].reference[1:]) >= 0)):
                self.reference = tokens[1]
                self.repr = f"{self.keyword} {self.reference}"
            else:
                raise Exception("Invalid variable/memory/register value.")
        elif self.keyword == BExp_Load:
            self.reference = tokens[2]
            self.value = tokens[3] 
            self.repr = " ".join(str(token) for token in tokens)
        elif self.keyword == BExp_Cast: # Cast Parsing
            self.operation = tokens[1]
            self.value = tokens[2]
            self.data_type = tokens[-1]
            self.repr = f"{self.keyword} {self.operation} {self.value} {self.data_type}"
        elif self.keyword == BExp_Store:
            self.address = tokens[3]
            self.value = tokens[5]
            self.repr = " ".join(str(token) for token in tokens) 

    def __str__(self) -> str:
        return self.repr

    def __repr__(self) -> str:
        return self.repr

    def __eq__(self, value: object) -> bool:
        return self.repr == value.repr

def build_expr():
    bs = Forward()
    const_val = build_const_value()
    var_expr = build_variable_expr()

    bs_expr = ( 
        ZeroOrMore(LBRACE) + BExp_Const + const_val + ZeroOrMore(RBRACE) |
        ZeroOrMore(LBRACE) + BExp_UnaryExp + oneOf(' '.join(str(keyword)[1:-1] for keyword in buop)) + bs + ZeroOrMore(RBRACE) |
        ZeroOrMore(LBRACE) + BExp_BinExp + oneOf(' '.join(str(keyword)[1:-1] for keyword in bop)) + bs + bs + ZeroOrMore(RBRACE) | 
        ZeroOrMore(LBRACE) + BExp_BinPred + oneOf(' '.join(str(keyword)[1:-1] for keyword in bpred)) + bs + bs + ZeroOrMore(RBRACE) |
        ZeroOrMore(LBRACE) + BExp_IfThenElse + bs + bs + bs + ZeroOrMore(RBRACE) |
        ZeroOrMore(LBRACE) + BExp_Den + var_expr + ZeroOrMore(RBRACE) | 
        ZeroOrMore(LBRACE) + BExp_Load + ZeroOrMore(LBRACE) + BExp_Den + var_expr + ZeroOrMore(RBRACE) + bs + oneOf(' '.join(str(keyword)[1:-1] for keyword in endians)) + oneOf(' '.join(str(keyword)[1:-1] for keyword in bimmt)) + ZeroOrMore(RBRACE) | 
        ZeroOrMore(LBRACE) + BExp_Cast + ZeroOrMore(LBRACE) + oneOf(' '.join(str(keyword)[1:-1] for keyword in bcast)) + ZeroOrMore(RBRACE) + bs + ZeroOrMore(LBRACE) + oneOf(' '.join(str(keyword)[1:-1] for keyword in bimmt)) + ZeroOrMore(RBRACE) + ZeroOrMore(RBRACE) |
        ZeroOrMore(LBRACE) + BExp_Store + ZeroOrMore(LBRACE) + BExp_Den + var_expr + ZeroOrMore(RBRACE) + bs + oneOf(' '.join(str(keyword)[1:-1] for keyword in endians)) + bs + ZeroOrMore(RBRACE)  
    )

    bs << ( ZeroOrMore(LBRACE) + bs_expr + ZeroOrMore(RBRACE))
    bs.setParseAction(BEXP)
    return bs_expr


class BIRParser:

    def __init__(self) -> None:
        pass

    def parse(self, cexpr): 
        expr = build_expr()
        e = expr.parseString(cexpr)

        if len(e) > 1:
            e = [BEXP(e)]

        # print("FINAL PARSING", e)
        return e[0]