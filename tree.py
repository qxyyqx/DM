
from __future__ import print_function
import sys
import os
import csv
from sklearn import svm


sys.path.extend(['.', '..'])

from pycparser import c_parser, c_ast,parse_file

class FuncCallVisitor(c_ast.NodeVisitor):
    def __init__(self, funcname):
        self.funcname = funcname
        self.count=0

    def visit_FuncCall(self, node):
        if node.name.name == self.funcname:
            self.count+=1
            #print('%s called at %s' % (self.funcname, node.name.coord))

def LineSum(filename):
    count=0
    for line in open(filename):
        if(line!='\n'):
            count+=1
    #print count
    return count

def _num_of_func_called_(filename, funcname):
    ast = c_parser.CParser().parse(filename, filename='<none>')
    v = FuncCallVisitor(funcname)
    v.visit(ast)
    return  v.count

def AST(_filename):
    dict1 = {"FuncDef": 0, "For": 0, "Decl": 0, "If": 0, "While": 0,"scanf":0,"printf":0,"gets":0}
    _file_vector = ["FuncDef", "For", "Decl", "If", "While","scanf","printf","gets"]

    _file=open(_filename)
    _pack_=_file.read()
    dict1["scanf"]= (_num_of_func_called_(_pack_,"scanf"))
    dict1["printf"]= (_num_of_func_called_(_pack_,"printf"))
    dict1["gets"]= (_num_of_func_called_(_pack_,"gets"))

    _file.close()
    parser1=c_parser.CParser()
    ast1=parser1.parse(_pack_,filename='<none>')
    f1=open("print1.txt","w+")
    ast1.show(f1)
    f1.close() #from txt to make AST

    #file2 = open(filename2)
    #content2 = file2.read()
    #dict2["scanf"] = (_num_of_func_called_(content2, "scanf"))
    #dict2["printf"] = (_num_of_func_called_(content2, "printf"))
    #dict2["gets"] = (_num_of_func_called_(content2, "gets"))
    #file2.close()
    #parser2 = c_parser.CParser()
    #ast2 = parser2.parse(content2, filename='<none>')
    #f2 = open("print2.txt", "w+")
    #ast2.show(f2)
    #f2.close()  #from txt to make AST


    for line in open("print1.txt"):
        name=line.split(":")[0].strip()
        if(not  name in _file_vector):
            continue
        dict1[name]+=1
    result={"input":0,"ruc":0,"output":0,"FuncDef":0,"LineSum":0}
    result["input"]=abs(dict1["gets"]+dict1["scanf"])
    result["ruc"]=abs(dict1["For"]+dict1["While"])
    result["output"]=abs(dict1["printf"])
    result["FuncDef"]=abs(dict1["FuncDef"])
    result["LineSum"]=LineSum(_filename)
    return [item[1] for item in sorted(result.items(),key=lambda e:e[0])] #FuncDef,LineSun,input.output,ruc


def gen_file_vectorVector(file):
    #str=readFile(file)
    re=[]
    try:
        x=AST(file)
    except:
        raise ValueError
    else:
        re.extend(x)
        return re

def makeTest(): #shengcheng suoyou test de vector
    path="test//"
    sum=0
    test={}
    for filename in os.listdir(path):
       #if(sum<=3):
        sum+=1
        print (sum)
        test[filename]=gen_file_vectorVector(path+filename)
    print (test)
    return test #shi yi ge dictionary

def makeTrain():
    path="train//"
    all={}
    key=[]
    value=[]
   # key.append("jj")
    #key.append("eee")
    #value.append(1)
    #value.append(2)
    print (key)
    print (value)
    count=0
    number=50
    for filename in os.listdir(path):
        sum=0
        count+=1
        t = []
        for file in os.listdir(path+filename):
          sum+=1
          if(sum<=number): #gaicheng 200 jiushi 20*200
              t.append(gen_file_vectorVector(path+filename+"//"+file))
          else:
              break
        all[count]=t
    i=1
    while i<=1:
        if i in all:
            j=0
            while j<number:
                k = j + 1
                while k<number:
                    t=[]
                    for ii in range(5):
                        t.append(abs(all[i][k][ii] - all[i][j][ii]))
                    key.append(t)
                    value.append(1)
                  #  print (t)
                  # print (key)
                  #  print (value)
                    k+=1
                j+=1
        i+=1
    i=1
    while i<=20:
        if i in all:
            j=i+1
            while j<=20:
                if j in all:
                    for k in range(10):
                        for m in range(10):
                            t=[]
                            for n in range(5):
                                t.append(abs(all[i][k][n]-all[j][m][n]))
                            key.append(t)
                            value.append(0)
                j+=1
        i+=1
    #print (all)
    #print (len(all))
    return key,value



print (AST("train//043e/0005efff92534ede.txt"))
a=makeTest()
key,value=makeTrain()
clf=svm.SVC()
print ("length of key:")
print (len(key))
print ("length of value:")
print (len(value))

clf.fit(key,value)
sum = 1
csv_reader = csv.reader(open('sample_submission.csv'))
writer = csv.writer(open('new.csv', 'wb'))
for row in csv_reader:
    if (sum == 1):
        writer.writerow(row)
    else:
        t = row
        temp = row[0]
        #print temp
        csv1 = temp.split('_')[0] + '.txt'
        csv2 = temp.split('_')[1] + '.txt'
        t[1] = 0
        m=[]
        if csv1 in a and csv2 in a:
            for n in range(5):
                m.append(abs(a[csv1][n]-a[csv2][n]))
            t[1]=clf.predict([m])[0]
        writer.writerow(t)
    sum = sum + 1
