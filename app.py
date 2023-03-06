from flask import Flask, render_template, request
from data import salary_list

# 保存数据函数
def save_fun():
    with open('/DevOps/flaskproject/data.py', 'w') as f:
        f.write('salary_list=' + str(salary_list))

# 创建Flask对象
app = Flask(__name__)


# 登录页面
@app.route('/')
def hello_index():
    return render_template('index.html')


# 显示页面
@app.route('/login', methods=["POST"])
def hello_login():
    # 获取页面数据
    username = request.form.get('username')
    password = request.form.get('password')

    # 判断用户名和密码
    li = []
    for i in salary_list:
        if i['name'] == username and i['password'] == password:
            result = 'success'
            li.append(result)
        else:
            result = 'fail'
            li.append(result)

    if 'success' in li:
        if username == 'admin':
            return render_template('admin.html', salary_list=salary_list)
        else:
            for u in salary_list:
                if u['name'] == username:
                    return render_template('user.html', salary_list=[u])
    else:
        return render_template('index.html', error='用户名或密码错误，请重新输入！')

# 删除页面
@app.route('/delete/<name>')
def hello_delete(name):
    # 删除逻辑,前端返回用户名,遍历文件数据库查看用户是否存在,存在则删除并退出,返回admin.html页面
    for user in salary_list:
        if user['name'] == name:
            salary_list.remove(user)
            break

    save_fun()
    return render_template('admin.html', salary_list=salary_list)


# admin用户修改页面
@app.route('/change/<name>')
def hello_change(name):
    # 修改逻辑, 前端返回用户名,遍历查看用户是否存在,存在则返回修改页面
    for user in salary_list:
        if user['name'] == name:
            return render_template('change.html', user=user)


@app.route('/change_save/<name>', methods=["POST"])
def hello_change_save(name):
    # 修改保存逻辑,找到用户,并将用户信息修改为前端输入的,返回admin.html页面
    for user in salary_list:
        if user['name'] == name:
            user['name'] = request.form.get('username')
            user['age'] = request.form.get('age')
            user['birth_date'] = request.form.get('birth_date')
            user['join_date'] = request.form.get('join_date')
            user['password'] = request.form.get('password')

    save_fun()
    return render_template('admin.html', salary_list=salary_list)


# 普通用户修改页面
@app.route('/user_change/<name>')
def hello_user_change(name):
    # 修改逻辑, 前端返回用户名,遍历查看用户是否存在,存在则返回修改页面
    for user in salary_list:
        if user['name'] == name:
            return render_template('user_change.html', user=user)


@app.route('/user_change_save/<name>', methods=["POST"])
def hello_user_change_save(name):
    # 修改保存逻辑,找到用户,并将用户信息修改为前端输入的,返回admin.html页面
    for user in salary_list:
        if user['name'] == name:
            user['name'] = request.form.get('username')
            user['age'] = request.form.get('age')
            user['birth_date'] = request.form.get('birth_date')
            user['join_date'] = request.form.get('join_date')
            user['password'] = request.form.get('password')

    save_fun()

    # 判断修改后的用户名是否和网页上的用户名是否相同,相同则返回user.html页面
    for u in salary_list:
        if u['name'] == request.form.get('username'):
            return render_template('user.html', salary_list=[u])

# 添加页面
@app.route('/add_user')
def hello_add():
    # 添加逻辑，跳转到添加页面
    return render_template('add.html')


@app.route('/add_save', methods=["POST"])
def hello_add_save():
    # 添加保存逻辑,将用户信息保存为字典插入data.py中并返回admin.html页面
    new_user = {}
    new_user['name'] = request.form.get('username')
    new_user['age'] = request.form.get('age')
    new_user['birth_date'] = request.form.get('birth_date')
    new_user['join_date'] = request.form.get('join_date')
    new_user['password'] = request.form.get('password')

    salary_list.insert(0, new_user)

    save_fun()
    return render_template('admin.html', salary_list=salary_list)


if __name__ == '__main__':
    app.run()
