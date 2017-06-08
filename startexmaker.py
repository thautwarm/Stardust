import sys,re,os
#from Stardust import PM,Any,Seq
def mainfunc():
    arg=sys.argv[1]
    if len(sys.argv)<3:
        o=arg.replace("tex",'stx.tex')
    else:
        o=sys.argv[2]
    with open(arg,'r') as f:
        string=f.read()
    with open(o ,'w') as f:
        f.write(compile(string))
    os.system("latex %s"%o)
token = re.compile(' |<<|>>|\$+|\P|\\\\[\w]+|[\w]+|[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]+')

class Parser:
    def __init__(self):
        self.macros=dict() #dict(macroname=(argnumber, lambda))
    def makeing(self,sentence):
        defines =dict(list(map(self.makedefine, re.findall("@:(.+)\[(.+)\]",sentence))))
        self.macros.update(defines)
        words=token.findall(re.sub('@:.+\[.*\]','',sentence))
        words=self._parsing(words)
        return self.parsing(words)
    def _parsing(self,words):
        new_words=[]
        words.reverse()
        while words:            
            word=words.pop()   
            if '<<' == word:
                ad=1
                recu=[]
                word=words.pop()
                while True:
                    if word=='>>':
                        ad-=1
                        if ad==0:break
                    elif word=='<<':
                        ad+=1
                    recu.append(word)
                    word=words.pop()
                new_words.append(self._parsing(recu))
            else:
                new_words.append(word)
        return new_words
    def parsing(self,words):
        if isinstance(words,str):
            return words
        new_words=[]
        words.reverse()
        while words:       
            word=words.pop()  
            if isinstance(word,str) and word in self.macros:
                num,macro=self.macros[word]
                i=1
                args=[]
                while i<=num: 
                    w=words.pop()
                    if  isinstance(w,str) and w==' ':continue
                    i+=1
                    args.append(self.parsing(w))
                new_words.append(macro(*args))
            else:
                new_words.append(self.parsing(word))
        return ''.join(new_words)
    def makedefine(self,define):
        DefArgs, Lambda=define
        DefArgs=list(filter(None,DefArgs.split(" ")))
        funcname=DefArgs[0]
        argnumber=len(DefArgs)-1
        Lambda ="lambda "+ ','.join(DefArgs[1:])+':'+Lambda
        return    (funcname , (argnumber, eval(Lambda)))
def compile(string):
    processor=Parser()
    string=re.sub(" {1,}"," ",string)
    sentences=string.splitlines()
    retList=[]
    for sentence in sentences:
        retList.append(processor.makeing(sentence))
    return '\n'.join(retList).replace('turn','\\\\')

    pass
if __name__=='__main__':
    
    mainfunc()

    #
