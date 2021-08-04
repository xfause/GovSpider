import os
count = 0
import codecs

decode_set=["utf-8",'ANSI','gb18030', 'ISO-8859-2','gb2312',"gbk","Error" ]#编码集

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

def walkFolder(file):
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
                    print(dir_path)
                    walkFile(dir_path)


def walkFile(folder):
    for root, dirs, files in os.walk(folder):
        for f in files:
            global count
            count += 1
            file_path = os.path.join(root, f)

            analyse_data_folder_path = os.path.exists(
                './data/{}'.format(folder.split('\\')[1]))
            if not analyse_data_folder_path:
                os.makedirs('./data/{}'.format(folder.split('\\')[1]))
            genTotalTitle(folder, file_path, './data/{}'.format(folder.split('\\')[1]))
            genTotalContent(folder, file_path, './data/{}'.format(folder.split('\\')[1]))
    print("文件数量一共为:", count)


def cleanTitle(title):
    return title.replace('title:', '').rstrip().replace('\n', '').replace(' ', '')

def cleanContent(title):
    return title.rstrip().replace('\n', '').replace(' ', '')

def genTotalTitle(folder_path, file_path, save_file_path):
    # for line in codecs.open(file_path,'r','utf-8'):
    for line in read_unknow_encoding_file(file_path):
        total_title_file = open(os.path.join(save_file_path, 'title_total.txt'), 'a', encoding="utf-8")
        # print(line)
        if (line.find('title:') >= 0):
            total_title_file.write(cleanTitle(line))
            total_title_file.write("\n")
        total_title_file.close()
    return


def genTotalContent(folder_path, file_path, save_file_path):
    # for line in codecs.open(file_path,'r','utf-8'):
    for line in read_unknow_encoding_file(file_path):
        total_content_file = open(os.path.join(save_file_path, 'content_total.txt'), 'a', encoding="utf-8")
        tmp = line.rstrip().replace('\n', '').replace(' ', '')
        if (tmp != '' and tmp.find('title:') < 0):
            total_content_file.write(cleanContent(line))
            total_content_file.write("\n")
        total_content_file.close()
    return


if __name__ == '__main__':
    walkFolder(r"../../GovSpider")
