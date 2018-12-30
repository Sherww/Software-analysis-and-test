import ast,csv
from git import Repo
import Levenshtein

class CodeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.nodes = []
    
    def generic_visit(self, node):
        self.nodes.append(node)
        ast.NodeVisitor.generic_visit(self, node)

def nodes_sim(nodes1, nodes2):
    names1 = " ".join([type(node).__name__ for node in nodes1])
    names2 = " ".join([type(node).__name__ for node in nodes2])
   # print(names1)
    #print(names2)
    print('-------start distance--------')
    edit_dis=Levenshtein.distance(names1, names2)
   # print (edit_dis)
    return edit_dis


def parsefile(ast_str1,ast_str2):
    visitor1 = CodeVisitor()
    visitor2 = CodeVisitor()
    visitor1.visit(ast_str1)
    visitor2.visit(ast_str2)
    edit_dis=nodes_sim(visitor1.nodes, visitor2.nodes)
    return edit_dis


def readfile():
    repo=Repo('numpy')
    git=repo.git
    sha_old=''
    sha_new=''
    with open('/home/cyl/Downloads/course/csvfiles/v1.15.0.csv',encoding='utf-8') as f:
        contents=csv.reader(f)
        for  i ,line in enumerate(contents):
            print('-----%d-----'%i)
            sha=line[0]
            print(sha)
            #if(i<98):
             #   continue
            if(i<2000):
                continue
            if i==2000:
                sha_new=sha
                if len(line)>2:
                    files=line[2:]
                continue
            else:
                sha_old=sha
                sum_sim=0
                len_file={}
                print(sha_old,sha_new)
                #print(files)
                for filec in files:
                    if filec.endswith('.py'):
                        print(filec)
                        #print(git.show(sha,filec))
                        #with open('numpy/'+filec) as fc:
                            #contentsc=fc.readlines()
                        if i==0:
                            sha_new=sha
                            break
                        else:
                            sha_old=sha
                            try:
                                git.checkout(sha_old,filec)
                                filepath='numpy/'+filec
                                with open(filepath) as fc:
                                    contentsc1=fc.read()
                                git.checkout(sha_new,filec)
                                with open(filepath) as fc:
                                    contentsc2=fc.read()
                                ast_str1=ast.parse(contentsc1)
                                ast_str2=ast.parse(contentsc2)
                                edit_dis=parsefile(ast_str1,ast_str2)
                                sha_old=sha
                                sum_sim += edit_dis
                                len_file[filec]=edit_dis
                            except Exception:
                                print('has not files',filec)
                print(sum_sim)
                print(len_file)
                cons=sha_new+','+str(sum_sim)+','+str(len(len_file))+","
                for a,b in len_file.items():
                    cons=cons+str(a)+','+str(b)
                print(cons,file=open("edit_dis.txt",'a',encoding='utf-8')) 
                sha_new=sha
            if len(line)>2:
                    files=line[2:]
            else:
                files=[]  
if __name__=='__main__':
    readfile()
