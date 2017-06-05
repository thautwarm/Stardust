# -*- coding: utf-8 -*-
from . import PatternMatching as PM,Any,Seq

x=PM([2,3,3])
print(x.match([Seq(int)]))

x=PM({1.0,2.0,3.0})
print(x.match({Seq(float)}))
print(x.match({Any(float),Any(float),Any(float)}))

# Any() matches any type as well as Seq() matches any  *[type]*N 
x=PM(dict(a='sss',sss='instance'))
print( x.match(dict(a=Any(),sss=Any(str) )))

class myobj:    
    def __init__(self,v,g,f):
        self.v=v
        self.g=g
        self.f=f
    def somemethod(self):
        pass
x=PM(myobj(1,[23,""],2))
print(x.match( myobj(1,Any(list),2)))




