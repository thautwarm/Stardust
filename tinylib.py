# -*- coding: utf-8 -*-
from collections import Iterable,defaultdict
import re
def tail_call(RetDeal=None):
    """
    tail-call optimization
    """
    def wrapper1(func):
        def wrapper2(*args,**kwargs):
            tail=func(*args,**kwargs)
            while True:
                try:
                    tail=next(tail)
                except:
                    return tail if not RetDeal else RetDeal(tail)
        return wrapper2
    return wrapper1

class Any(object):
    def __init__(self,family=object):
        self.family=family
    def __eq__(self,var):
        if isinstance(var,Any):
            return var.family==self.family
        return isinstance(var,self.family)
    def __hash__(self):
        return hash((self.family,...))
class Seq(Any):
    def __init__(self,family=object,atleast=0):
        self.family=family
        self.least=atleast
def AlgebraDiv(iterator,func):
    subStructures=defaultdict(set)
    for item in iterator:
        subStructures[func(item)].add(item)
    return subStructures

@tail_call(RetDeal=lambda var:var==True)
def checkSeq(val,var):
    """
    check the sequential data-type like tuple and list and the subclasses inherit them.
    it supports the nd-array in NumPy.
    """
    if len(val)==0 :
        yield len(val)==0 and len(var)==0
    elif isinstance(val[0],Seq):
        catchNum = 0
        for var_i in var:
            if val[0] == var_i:
                catchNum += 1
            else:break
        if catchNum>=val[0].least:
            yield checkSeq(val[1:],var[catchNum:])
        else:
            yield False
    elif isinstance(val[0],Iterable):
        yield checkSeq(val[0],var[0])  and isinstance(val[0],Iterable)and checkSeq(val[1:],var[1:])
    else:
        yield False if val[0]!=var[0] else checkSeq(val[1:],var[1:])


def partMatch(val,var,partial=True,expected=False):
    if isinstance(val,Iterable):
        try:
            if issubclass(val.__class__,set):
                subStructures=AlgebraDiv(val,
                    lambda item: isinstance(item,Any))
                NormalDefined,GeneralDefined =subStructures[False],subStructures[True]
                judge_one= len(NormalDefined&var)== len(NormalDefined)
                if not judge_one:return False
                for idx,item in enumerate(var):
                    if item in val:
                        val.remove(item)
                    else:
                        #there is not any instance of "Any", however there is atleast 1 item left in "var".
                        if not GeneralDefined:return True if partial else False

                        toRemove=None.__class__
                        for genItem in GeneralDefined:
                            if genItem==item:
                                toRemove=genItem
                                break
                        if toRemove!=None.__class__:
                            GeneralDefined.remove(toRemove)
                        else:
                            # An item does not match any instance of "Any" left,
                            #       which means the "val"  not equaled with "var".
                            if not partial:
                                return False
                return not GeneralDefined and (True if partial else (idx+1)==len(var))
            elif issubclass(val.__class__,dict):
                if not partial and len(val.keys())!=len(var.key()):
                    return False
                for key in val.keys():
                    if val[key]!=var[key]:
                        return False
                return True
            else:
                return checkSeq(val,var)
        except:
                if expected:return ValueError
                return False
    else:
        attrs=dir(val)
        for attr in attrs:
            if not re.findall('__.*__',attr).index(attr):continue
            if  not (hasattr(var,attr) and getattr(var,attr)==getattr(val,attr)):
                return False
        return True
