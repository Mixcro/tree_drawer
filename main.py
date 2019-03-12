import os
import re
from PIL import Image, ImageDraw, ImageFont

# config
max_length = 20  # 每行最大字符数
font_size = 24  # 字体大小
line_color = (0,192,192)  # 导引线颜色
sign_list = ['，', '。', '；', '：', '‘', '’', '“', '”', '！', '？', ',', '.', ';', ':']


def color(level):
    '''根据层级划分颜色'''
    if level >= 4:
        return((0, 192, 0))
    else:
        return((255, 255, 255))

def read_file(path):
    '''读取txt'''
    text_list = []
    with open(path, 'rt', encoding='utf-8') as f:
        for line in f.readlines():
            level = 0
            line = re.sub(r'\n' ,'', line)
            # 清洗空行层级
            if "".join(line.split()) == '':
                line = ''
            # 判断层级
            while line[:4] == '    ':
                level += 1
                line = line[4:]
            text_list.append([level, line[:max_length]])
            line = 'sub' + line[max_length:]
            while line != 'sub':
                # 把标点符号弄回上行行末
                while line[3:4] in sign_list:
                    text_list[-1][1] += line[3:4]
                    line = line[:3] + line[4:]
                if line == 'sub':
                    break
                # 自动换行
                text_list.append([level, line[:max_length+3]])
                # 添加换行标识
                line = 'sub' + line[max_length+3:]
    return(text_list)

def draw_image(text_list):
    '''绘图'''
    height = int(font_size*3/2)
    rows = len(text_list)
    cows = max([x[0]*2+len(x[1]) for x in text_list])+1
    font = ImageFont.truetype('old_song.ttf', font_size)
    # creat image area
    image = Image.new('RGB', (font_size*cows, height*rows), (0, 0, 0))
    draw = ImageDraw.Draw(image)
    for i in range(0, len(text_list)):  # 此处i为行数
        line = text_list[i]
        # 输出行文字
        if line[1][:3] != 'sub':
            draw.text((font_size*(line[0]*2+1), i*height+int((height-font_size)/2)), line[1], font=font, fill=color(line[0]))
        else:
            draw.text((font_size*(line[0]*2+1), i*height+int((height-font_size)/2)), line[1][3:], font=font, fill=color(line[0]))
        # 绘制导引线
        if line[0] > 0:
            if line[1][:3] != 'sub':
                # 绘制水平导引线
                y = height * i + int(height/2-1)  # 理论上应在中间，不过上移1px似乎舒服些
                for _y in range(y, y+2):
                    for _x in range(font_size*(line[0]*2-1)+int(font_size/3), font_size*(line[0]*2+1)-int(font_size/4)):
                        draw.point((_x, _y), fill=line_color)
                # 绘制竖直导引线
                while i > 0:
                    i = i - 1  # 定位到其上一行
                    x = font_size*(line[0]*2-1)+int(font_size/3)
                    if text_list[i][0] < line[0]:
                        # 上一行为父级，绘制不完整竖直引导线并终止循环
                        y = height * i + height   # 重新定位y
                        for _x in range(x, x+2):
                            for _y in range(y, y+int(height/2)):
                                draw.point((_x, _y), fill=line_color)
                        break
                    else:
                        y = height * i + int(height/2-1)  # 重新定位y至上一行水平引导线处
                        for _x in range(x, x+2):
                            for _y in range(y, y+height+1):
                                draw.point((_x, _y), fill=line_color)
    return(image)

def save_image(image, path):
    '''保存结果'''
    image.save(path, 'png')

if __name__ == '__main__':
    print('Hello world.')
    input_path = './input'
    output_path = './output'
    for item in os.listdir(input_path):
        text_list = read_file(os.path.join(input_path, item))
        image = draw_image(text_list)
        #image.show()
        save_image(image, os.path.join(output_path, '%s.png'%item[:-4]))
    print('Bye world.')