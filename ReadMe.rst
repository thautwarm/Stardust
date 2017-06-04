

Stardust
==================

It sounds a strange name as a result of my thinking during last night.
I just want to write codes in the best way, I think.

Comparison With Haskell
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


  >>patMatch({1,2,3},{1,2,3},part=False)
  >>True
  >>patMatch({1,2},{1,2,3})
  >>True
  >>patMatch({1,2},{1,2,3},part=False)
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


this library is not complete at this time, but I'll finish it soon.

If you use Python as you main weapon but you want to code in a more rational style, hope you can benefit from my work.
