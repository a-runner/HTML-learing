import binascii
KEYS = [0x80, 0x40, 0x20, 0x10, 0x08, 0x04, 0x02, 0x01]


#初始化16*16的点阵位置，每个汉字需要16*16=256个点来表示
rect_list = [] * 16
for i in range(16):
    rect_list.append([] * 16)
#拿“赞”字来演示
text = "赞"
#获取中文的编码
gb2312 = text.encode('gb2312')
hex_str = binascii.b2a_hex(gb2312)
result = str(hex_str, encoding='utf-8')
#根据编码计算“赞”在汉字库中的位置
area = eval('0x' + result[:2]) - 0xA0
index = eval('0x' + result[2:]) - 0xA0
offset = (94 * (area-1) + (index-1)) * 32
font_rect = None
#读取HZK16汉字库文件中“赞”字数据
with open("/font_library/字库/16x16/hzk16s", "rb") as f:
    f.seek(offset)
    font_rect = f.read(32)
#根据读取到HZK中数据给我们的16*16点阵赋值
for k in range(len(font_rect) // 2):
    row_list = rect_list[k]
    for j in range(2):
        for i in range(8):
            asc = font_rect[k * 2 + j]
            flag = asc & KEYS[i]
            row_list.append(flag)
#根据获取到的16*16点阵信息，打印到控制台
for row in rect_list:
    for i in row:
        if i:
            #前景字符（即用来表示汉字笔画的输出字符）
            print('0', end=' ')
        else:
            #背景字符（即用来表示背景的输出字符）
            print('.', end=' ')
    print()
