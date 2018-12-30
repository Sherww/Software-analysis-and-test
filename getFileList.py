# -*- coding:utf-
import os


# allFileNum = 0
def getFileList(level, path, path_initial, fileList, allFileNum):  # 使用堆上的匿名参数来实现一个累加器
#     global allFileNum
    '''
    打印一个目录下的所有文件夹和文件 
    '''   
    # 所有文件
    fileList_onlyFileName = []
    # 返回一个列表，其中包含在目录条目的名称
    files = os.listdir(path)
    for f in files:
        temp = path + '/' + f
        if(os.path.isdir(temp)):         
            if(f[0] != '.'):  # 排除隐藏文件夹。因为可能会有隐藏文件夹
                print ('-' * level, f)
                # 打印目录下的所有文件夹和文件，目录级别+1
                getFileList((level + 1), temp, path_initial, fileList, allFileNum)  # recursion
        if(os.path.isfile(temp)):
            # 添加文件
            fileList_onlyFileName.append(f)
            filefullName = temp.replace(path_initial, "" , 1)
            fileList.append(filefullName)
    for fl in fileList_onlyFileName:
        # 打印文件
        print ('-' * level, fl)
        # 顺便计算一下有多少个文件
        allFileNum[0] = allFileNum[0] + 1
        # int(allFileNum[0])


if __name__ == '__main__':
    
    pathName_project = "/home/cyl/Downloads/course/ast/numpy";  # 文件路径
    level = 1;  # 目录层级
    path_initial = pathName_project;  # 在递归时需要计算减去，和初始文件路径名一致
    fileList = [];  # 存储读出的文件
    allFileNum = [0];  # 存储文件总数
    
    # 获取项目文件列表
    getFileList(level, pathName_project, path_initial, fileList, allFileNum);
    print ('总文件数 =', allFileNum)
