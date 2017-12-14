
Stardust
==================

I just want to write codes in the best way.


## LaTexDSL

---------------

- Requirements:

  - MiKTeX 2.9.6300
  - PyInstaller for cpy3
  - python

Just see  how the source codes transformed to the target...

- test.tex

```latex

  \documentclass[UTF8]{ctexart}
  \usepackage{amsmath,amssymb,latexsym}
  \begin{document}
  @:func a b[ r"{a}\left( {b} \right)".format(a=a,b=b)]
  @:div a b [r"{a}/{b}".format(a=a,b=b)]

  \noindent proof 1.1 Exercise (1)  turn
  $\forall y \in func f A \cap func f B $, turn
  $ y \in func f A \wedge y \in func f B  \rightarrow$
  $$ \exists x_1 \in A , func f x_1 = y \wedge \exists x_2 \in B , func f x_2 =y ,  \rightarrow $$
  $$ x=x_1=x_2 \rightarrow x \in A \cup B \rightarrow y = func f x \in func f <<A \cup B>> $$
  []
  turn
  turn
  \noindent proof 1.1 Exercise (2) turn
  $\forall y \in  div <<func f X>> <<func f A>> $, turn
  $y \in func f X \wedge y \notin func f A $, turn
  $\exists x_1 \in X , func f x_1 = y \wedge \forall  x \in func f A, func f x \not= y \rightarrow$,
  $$y = func f <<\overline x>>, x \in X \wedge x \notin A \rightarrow $$
  $$y \in func f <<div X A>> $$
  []

```

- target.tex

```latex

  \documentclass[UTF8]{ctexart}
  \usepackage{amsmath,amssymb,latexsym}
  \begin{document}
  \noindent proof 1.1 Exercise (1) \\
  $\forall y \in f\left( A \right) \cap f\left( B \right) $, \\
  $ y \in f\left( A \right) \wedge y \in f\left( B \right) \rightarrow$
  $$ \exists x_1 \in A , f\left( x_1 \right) = y \wedge \exists x_2 \in B , f\left( x_2 \right) =y , \rightarrow $$
  $$ x=x_1=x_2 \rightarrow x \in A \cup B \rightarrow y = f\left( x \right) \in f\left( A \cup B \right) $$
  []
  \\
  \\
  \noindent proof 1.1 Exercise (2) \\
  $\forall y \in f\left( X \right)/f\left( A \right) $, \\
  $y \in f\left( X \right) \wedge y \notin f\left( A \right) $, \\
  $\exists x_1 \in X , f\left( x_1 \right) = y \wedge \forall x \in f\left( A \right), f\left( x \right) \not= y \rightarrow$,
  $$y = f\left( \overline x \right), x \in X \wedge x \notin A \rightarrow $$
  $$y \in f\left( X/A \right) $$
  []
  \end{document}

```

Uh... I think it help a lot with my homework...  
Just pack `startex.py` to `.exe`  in Windows, and then 

```
startex  <tagfile>  <outputfile>
```

## Pattern Matching
---------------

It must be boring to be involved with the arguments like "which is the best programming language?".

For sure it seems most likely that the answer is Haskell.

- Guard:

```
  sampleFunc:: Int->Int->String
  sampleFunc x y
    | x<10 = "digit"
    | (x>10)&&(y<20) = "teens"
    | (x%10==0) = "tens"
    | otherwise = "tens and digit"
```

But in some degree, it's not practicable for me to use Haskell as my main weapon, as the result of there're quite many comprehensive libraries writing in Python available.

Also, using Python can be somewhat a tradition in Scientific Researching.

Uh, maybe the most important point is that I'm not clever at all. And I does have a coding style with both OO and FP,
which is not pure at all.


But I cannot live without pattern matching yet...  
So..

```python

  >>patMatch({1,2,3},{1,2,3},partial=False)
  >>True
  >>patMatch({1,2},{1,2,3})
  >>True
  >>patMatch({1,2},{1,2,3},partial=False)
  >>False
  >>patMatch([1,2,Any(int)],[1,2,3])
  >>True

  # and more examples can be given.
  patMatch([1,2,Seq(int,atleast=2),0.5],[1,2,3,10,0.5]) #->True

  patMatch([1,2,Seq(float,atleast=2),0.5],[1,2,3,10,0.5]) #->True

  patMatch((1,2,Seq(float)),[1,2]) # -> True

  patMatch((1,2,Seq(float,atleast=2)),[1,2]) # -> False

  patMacth([[1,2,3],[Seq(int),[Seq(int)]]],[[1,2,3],[1,[1]]] ) #->True

  patMatch([Any(dict)],[dict(a=[1,2,3],b=[2,3,4])]) # ->True

  dictionary= {'a':1,'b':20}

  patMatch(dict(a=Any(int),b=20),dictionary) #-> True


  class sampleClass:
      def __init__(self,a,b,c):
          self.a=a
          self.b=b
          self.c=c
      def func(self):
          dosomething

  instance=sampleClass(1,15,20)
  patMatch(sampleClass(1,Any(int),Any(int)),instance) # -> True

```

Use this module conveniently:

```python
  from Stardust import *
  matcher0=PM([1,"2",2])
  print (matcher.match([1,Any(str),2])) #->True

  matcher1=PM([1,2,3,4,""])
  print (matcher2.match([1,Seq(int),""])) #-> True

  class sample:
    def __init__(self,a,b,c):
      self.a=a
      self.b=b
      self.c=c
    def dosome(self):pass

  matcher2=PM([[sample(1,2,3),dict(a=2,c=5,d=7)],[],[]])
  matcher2.match([[sample(Any(),*[Any(int)]*2,dict(a=2)],Seq(list)],partial=True) #->True

```

And more examples can be found in [runsamples.py](https://github.com/thautwarm/Stardust/blob/master/runsamples.py)

Welcome to find out the bugs in this tiny library.

If you use Python and you want to code in a more rational style, hope you can benefit from my works.


## Strict Type in Python

If you prefer languages which is more likely to do type checking and you have to write python sometimes, try this.

```python

@strict.args(int,int)
@strict.ret(float)
def f(a,b):
    return a*b*1.0


>> f(1.0, 2.0)
TypeError: Type of argnument 0 should <class 'int'>

>> f(1, 2)
>> 2.0

@strict.args(str, int , name = str)
@strict.ret(str)
def repeat(a, b, name = '<unknown>' ):
    print(f'in closure : {name}')
    return a*b

>> repeat("2", 3)
in closure : <unknown>
>> '222'

>> repeat("2","2")
TypeError: Type of argnument 1 should <class 'int'>

```

And there're many nice properties to use the `strict` you can find it for yourself.
The source codes is tiny, you can see it [here](https://github.com/thautwarm/Stardust/blob/master/typepy.py)  
Making some extensions based on it might be something very very interesting!

## TCO in CPython
------------------
See [tco.ipynb](./tco.ipynb).  
```python
import functools
from collections import namedtuple
param_struct = namedtuple('param_struct', ['args', 'kwargs'])
def tco(func):
    def call(*args, **kwargs):
        try:
            old = func.__globals__[func.__name__] 
            func.__globals__[func.__name__] = lambda *args, **kwargs : param_struct(args, kwargs)
            res = param_struct(args, kwargs)
            while True:
                res = func(*res.args, **res.kwargs)
                if isinstance(res, param_struct):
                    continue
                break
            func.__globals__[func.__name__] = old
            return res
        except Exception as e:
            func.__globals__[func.__name__] = old
            raise e
    return call
```
I'm so glad to see that `tail call optimization` could be put into actual use in Python.



