

Stardust
==================

It sounds a strange name as a result of my thinking during last night.
I just want to write codes in the best way, I think.


LaTexDSL
---------------

- Requirements:
  - MiKTeX 2.9.6300
  - PyInstaller for cpy3
  - python

just see  how the source codes transformed to the target...
.. code:: LaTex
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

.. code:: LaTex
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



  Uh... I think it help a lot with my homework...
  just pack the file startex.py to .exe in Windows, and then
.. code:: shell
  startex <tagfile> <outputfile>




PatternMatching
---------------

It must be boring to be involved with the arguments like "which is the best programming language?".

For sure it seems most likely that the answer is Haskell.

.. code:: Haskell

  sampleFunc:: Int->Int->String
  sampleFunc x y
    | x<10 = "digit"
    | (x>10)&&(y<20) = "teens"
    | (x%10==0) = "tens"
    | otherwise = "tens and digit"


But in some degree it's not practicable for me to use Haskell as my main weapon,
the reasons for which are lying in the aspects about the available and comprehensive libraries in Python and
the traditions in Scientific Researching.

Uh, maybe the most important one is that I'm not clever at all. And I does have a coding style with both OO and FP,
which is not pure at all.


But I cannot live without pattern matching yet...
So...

.. code:: Python
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

.. code:: Python

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


And more examples can be found in `runsamples.py <https://github.com/thautwarm/Stardust/blob/master/runsamples.py>`_.

Welcome to find out the bugs in this tiny library.

If you use Python as you main weapon but you want to code in a more rational style, hope you can benefit from my work.
