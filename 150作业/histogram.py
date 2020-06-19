import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_excel('book.xlsx')

xx = data.head(6)['小说名']
x = [i for i in xx]

yy = data.head(6)['评分人数']
y = [i for i in yy]


# 设置柱状图上面的值
def auto_label(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 1.5 - 0.2, 1.03 * height, '%s' % int(height))


plt.rcParams['figure.figsize'] = (15.0, 8.0)  # 尺寸
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.title('评价人数统计')
a = plt.bar(x, y)
auto_label(a)

plt.savefig("result.png")
plt.show()
