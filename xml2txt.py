import os
import xml.etree.ElementTree as ET

dirpath = 'D:\College_Innovation_entrepreneurship\PyQt5_Yolo\Image1'  # 原来存放xml文件的目录
newdir = 'D:\College_Innovation_entrepreneurship\PyQt5_Yolo\Imagell'  # 修改label后形成的txt目录

if not os.path.exists(newdir):
    os.makedirs(newdir)

nameList = ['box','bag']  # 按顺序设置成自己数据集的类别

for fp in os.listdir(dirpath):

    root = ET.parse(os.path.join(dirpath, fp)).getroot()

    xmin, ymin, xmax, ymax = 0, 0, 0, 0
    sz = root.find('size')
    width = float(sz[0].text)
    height = float(sz[1].text)
    filename = root.find('filename').text

    for child in root.findall('object'):  # 找到图片中的所有框

        sub = child.find('bndbox')  # 找到框的标注值并进行读取
        xmin = float(sub[0].text)
        ymin = float(sub[1].text)
        xmax = float(sub[2].text)
        ymax = float(sub[3].text)

        name = child.find('name').text

        if name not in nameList:
            nameList.append(name)

        idx = nameList.index(name)

        try:  # 转换成yolov3的标签格式，需要归一化到（0-1）的范围内
            x_center = (xmin + xmax) / (2 * width)
            y_center = (ymin + ymax) / (2 * height)
            w = (xmax - xmin) / width
            h = (ymax - ymin) / height

        except ZeroDivisionError:
            print(filename, '的 width有问题')

        with open(os.path.join(newdir, fp.split('.')[0] + '.txt'), 'a+') as f:
            f.write(' '.join([str(idx), str(x_center), str(y_center), str(w), str(h) + '\n']))

print(nameList)