import matplotlib.pyplot as plt  # Matplotlib 是一个 Python 的 2D绘图库，它以各种硬拷贝格式和跨平台的交互式环境生成出版质量级别的图形。
from matplotlib import font_manager   # 设置字体的库

my_font = font_manager.FontProperties(fname="simsun.ttc")  # 字体库，放在同一个项目同一层
fig = plt.figure(figsize=(20, 8), dpi=80)  # 指定图像的宽和高，单位为英寸，dpi参数指定绘图对象的分辨率，即每英寸多少个像素，缺省值为80


def draw_pic_test():
    '''
    作图
    '''
    # x轴数据
    month_list = ['201803', '201804', '201805', '201806', '201807', '201808', '201809', '201810', '201811', '201812',
                  '201901', '201902', '201903', '201904', '201905', '201906', '201907', '201908']
    # y轴数据
    mat = [
        [151, 157, 142, 129, 122, 146, 166, 144, 145, 156, 144, 135, 171, 151, 143, 164, 160, 168],
        [112, 117, 102, 109, 102, 106, 106, 104, 105, 106, 104, 105, 111, 121, 113, 104, 100, 108],
        [101, 107, 102, 109, 102, 106, 106, 104, 105, 106, 104, 105, 101, 101, 103, 104, 100, 106]
    ]

    plt.plot(month_list, mat[0], "x-", label="物价指数")  # plt.plot()函数的本质就是根据点连接线。根据x(数组或者列表) 和 y(数组或者列表)组成点，然后连接成线。
    plt.plot(month_list, mat[1], "x-", label="CPI")
    plt.plot(month_list, mat[2], "x-", label="PPI")


    # plt.xlabel('横坐标', fontproperties=my_font)
    # plt.ylabel('纵坐标', fontproperties=my_font)
    plt.title('中国经济任务物价指数', fontproperties=my_font)  # 标题
    plt.legend(prop=my_font)  # 给图像加上图例

    # plt.grid()  # 生成网格
    plt.show()


if __name__ == '__main__':
    draw_pic_test()
