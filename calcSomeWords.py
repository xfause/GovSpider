import os
from pprint import pprint
import codecs
count = 0
decode_set=["utf-8",'ANSI','gb18030', 'ISO-8859-2','gb2312',"gbk","Error" ]#编码集

WORD_LIST = ['开除公职', '开除党籍', '双开', '移送', '取消退休待遇','待遇']
WITHOUT_WORD_LIST = ['开除党籍', '移送']

def read_unknow_encoding_file(directions):
    for k in decode_set:#编码集循环
        try:
            file = open(directions,"r",encoding=k)
            #打开路径中的文本
            readfile = file.readlines()#这步如果解码失败就会引起错误，跳到except。
            # print("open file %s with encoding %s" %(directions,k))#打印读取成功
            # readfile = readfile.encode(encoding="utf-8",errors="replace")#若是混合编码则将不可编码的字符替换为"?"。
            return readfile
        except:
            if k=="Error":#如果碰到这个程序终止运行
                raise Exception("%s had no way to decode"%directions)
            continue
        # print("done!")

def walkFolder(file, obj):
    for root, dirs, files in os.walk(file):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        # 遍历所有的文件夹
        for d in dirs:
                dir_path = os.path.join(root, d)
                if (dir_path.find('../../GovSpider\GovSpider') >= 0 or dir_path.find('../../GovSpider\ForCopy') >= 0 or dir_path == '../../GovSpider'):
                    continue
                if (dir_path.find('data') > 0):
                    # if (dir_path == '../../GovSpider\Changchun\data'):
                        walkFile(dir_path, obj)

def checkWithoutFile(file_path):
    for word in WITHOUT_WORD_LIST:
        out_file_name = './without_{}'.format(word)
        out_file_content = open(out_file_name,'a',encoding="utf-8")
        flag = False
        for line in read_unknow_encoding_file(file_path):
            if (line.find(word)>0):
                flag = True
                break
        if (flag == False):
            out_file_content.write(file_path + '\n')

def walkFile(folder, obj):
    for root, dirs, files in os.walk(folder):
        for f in files:
            # print(files,f)
            file_path = os.path.join(root, f)
            # print(file_path, file_path.find('.txt'), file_path.find('data.txt'), file_path.find('_total.txt'))
            if (file_path.find('.txt')> 0 and file_path.find('data.txt')< 0 and file_path.find('_total.txt')<0):
                global count
                count += 1
                # CALC WITHOUT WORD FILE
                checkWithoutFile(file_path)

                # CALC INCLUDE WORD FILE
                for idx, word in enumerate(WORD_LIST):
                    for line in read_unknow_encoding_file(file_path):
                        if (line.find(word)>0):
                            obj[idx] += 1
                            break


if __name__ == '__main__':
    obj = {
        0:0,
        1:0,
        2:0,
        3:0,
        4:0,
        5:0
    };
    walkFolder(r"../../GovSpider", obj)
    print(count)
    for key in obj:
        # print(key)
        print(WORD_LIST[key],':', obj[key])