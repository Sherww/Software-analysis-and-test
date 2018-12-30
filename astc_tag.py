import ast,csv,os,re
from git import Repo
import Levenshtein
import getFileList

class CodeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.nodes = []
    
    def generic_visit(self, node):
#         print(type(node).__name__)
        self.nodes.append(node)
        ast.NodeVisitor.generic_visit(self, node)

def nodes_sim(nodes1, nodes2):
    names1 = " ".join([type(node).__name__ for node in nodes1])
    names2 = " ".join([type(node).__name__ for node in nodes2])
    #print('-------start distance--------')
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
    #git=repo.git
    #there are something wrong because the tags are set to be ordered by dictory but they should be ordered by time(date)
    #tags=repo.tags
    tag_old=''
    tag_new=''
    with open('vers.txt',encoding='utf-8') as f:
        tags=f.readlines()
        for i,tag in enumerate(tags):
            print(tag)
            if i<1:
                continue
            if i==1:
                tag_old=tag
            else:
                tag_new=tag
                sum_sim=0
                print(str(tag_new),str(tag_old))
                os.chdir('/home/cyl/Downloads/course/ast/numpy/')
                os.system('git reset --hard '+str(tag_new))
                os.chdir('/home/cyl/Downloads/course/ast/numpyc/')
                os.system('git reset --hard '+str(tag_old))
                pathName_project = "/home/cyl/Downloads/course/ast/numpy";  # 文件路径
                level = 1;  # 目录层级
                path_initial = pathName_project;  # 在递归时需要计算减去，和初始文件路径名一致
                fileList = [];  # 存储读出的文件
                allFileNum = [0];  # 存储文件总数
                
                # 获取项目文件列表
                getFileList.getFileList(level, pathName_project, path_initial, fileList, allFileNum);
                print ('总文件数 =', allFileNum)
                changed_file=[]
                for filep in fileList:
                    if filep.endswith('.py'):    
                        filepath=filep.replace("/home/cyl/Downloads/course/ast/numpy","/home/cyl/Downloads/course/ast/numpyc",1)
                        
                        if os.path.exists(filepath):
                            try:
                                with open(filep,encoding='utf-8') as fc:
                                    contentsc1=fc.read()
                                with open(filepath,encoding='utf-8') as fc:
                                    contentsc2=fc.read()
                            except Exception:
                                continue
                        else:
                            with open(filep) as fc:
                                contentsc1=fc.read()
                            contentsc2=""
                            print(tag_new,'->',tag_old,filep)
                            print(tag_new,'->',tag_old,filep,file=open('add_log.txt','a',encoding='utf-8'))
                        try:
                            #print(contentsc1)
                            ast_str2=ast.parse(contentsc2)
                            ast_str1=ast.parse(contentsc1)
                            #ast_str2=ast.parse(contentsc2)
                            edit_dis=parsefile(ast_str1,ast_str2)
                            print(filepath,edit_dis)
                            changed_file.append(filep+','+str(edit_dis))
                            sum_sim += edit_dis
                        except Exception:
                            print ('cylerror--------')
                cons=str(tag_new)+'->'+str(tag_old)+','+str(sum_sim)+','+str(len(changed_file))+','
                for tem in changed_file:
                    cons=cons+tem
                tag_old=tag
                print(cons)
                print(cons,file=open("/home/cyl/Downloads/course/ast/edit_vers_dis.txt",'a',encoding='utf-8')) 
                    
            #return
if __name__=='__main__':
    readfile()
