import random
from flask import Flask, render_template, request, flash
from spider import spider

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcdef'


@app.route('/', methods=['GET', 'POST'])
def search():
    ran = random.randint(1, 20000)
    keyword = request.form.get('keyword')
    em_dict = spider(keyword)
    # 如果没输入关键词，就提示：请输入关键词~
    if not keyword:
        flash('请输入关键词~')
        return render_template('index.html', em_dict=em_dict, ran=ran)

    return render_template('index.html', em_dict=em_dict, ran=ran)


if __name__ == '__main__':
    # 程序运行入口，host本机ip，端口5000，调试模式打开
    app.run(host='127.0.0.1', port=5000, debug=True)
