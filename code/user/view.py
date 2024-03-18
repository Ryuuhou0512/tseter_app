from flask import render_template,request,redirect,url_for,Blueprint
from user.model import user
from . import user_bp
from app import db,login_manager
from sqlalchemy import func
from flask_login import login_user,UserMixin,current_user,login_required




@user_bp.route('/login_view',methods = ['GET'])
def login_view():
    return render_template('login.html')


@user_bp.route('/login',methods = ['POST'])
def login():

    username = request.form['username']
    password = request.form['password']
    
    if username == 'admin' and password == 'admin':
        print(username)
        print(password)
        loginuser = user.query.filter_by(name=username).first()

        login_user(loginuser)
        print('登入成功')

        return redirect(url_for('user_bp.CRUD_view'))
    
    else:
        error_message = '帳號密碼錯誤，預設帳號密碼皆為admin(沒有透過資料庫進行比對，如果更改資料庫也還是admin)'
        return render_template('login.html',error=error_message)

@user_bp.route('/',methods=['GET'])
def base_view():
    return render_template('login.html')

@user_bp.route('/CRUD_view',methods=['GET','POST'])
@login_required
def CRUD_view():
    data = user.query.all()
    return render_template('CRUD.html',data=data)

@user_bp.route('/add_view',methods=['GET','POST'])
@login_required
def add_view():
    max_serial_number = user.query.with_entities(func.max(user.serial_number)).scalar()
    data = {'max_serial_number':max_serial_number+10,'text':''}
    return render_template('insert.html',data=data)


@user_bp.route('/add_user',methods=['POST'])
def add_user():
    username = request.form['username']
    password = request.form['password']
    serial_number = request.form['serial_number']

    new_user = user(name=username, password=password, serial_number=serial_number)
    db.session.add(new_user)
    db.session.commit()

    max_serial_number = user.query.with_entities(func.max(user.serial_number)).scalar()
    data = {'max_serial_number':max_serial_number+10,'text':'新增完成'}

    return render_template('insert.html',data=data)

@user_bp.route('/select_user',methods=['GET','POST'])
def select_user():
    keyword = request.args.get('keyword')
    if not keyword:
        data = user.query.all()
    else:
        data = user.query.filter(user.name.like(f"%{keyword}%")).all()

    return render_template('CRUD.html',data=data)

@user_bp.route('/edit_user',methods=['POST'])
def edit_user():
    update_data = request.get_json()
    for item in update_data:
        name = item.get('name')
        new_value = item.get('value')
        
        # 查询符合条件的用户
        user_to_update = user.query.filter_by(name=name).first()
        
        
        if user_to_update:
            user_to_update.password = new_value
    
    
    db.session.commit()
    
    data = user.query.all()

    return redirect(url_for('user_bp.select_user',data=data))


@user_bp.route('/delete_user',methods=['POST'])
def delete_user():
    update_data = request.get_json()

    for item in update_data:
        name = item.get('name')
        new_value = item.get('value')
        
        # 查询符合条件的用户
        user_to_update = user.query.filter_by(name=name).first()
        
        
        if user_to_update:

            user_to_update.is_deleted = new_value
    
    
    db.session.commit()
    
    data = user.query.all()

    return redirect(url_for('user_bp.select_user',data=data))


