from app import app
from flask import render_template, request, redirect, url_for, flash
from .forms import UserCreationForm, LoginForm, ProductForm, EditProfileForm
from .models import User, Product, Cart
from flask_login import login_user, logout_user, current_user, login_required

import os




@app.route('/')
def homePage():
    people = ['jackie','baileigh','bailey']
    
    return render_template('index.html', people=people)

@app.route('/about')
def aboutPage():
    return render_template('about.html')


   


@app.route('/signup', methods=["GET", "POST"])
def signUpPage():
    sign_up_form = UserCreationForm()
    if request.method == 'POST':
        if sign_up_form.validate():
            username = sign_up_form.username.data
            email = sign_up_form.email.data
            password = sign_up_form.password.data

            user = User(username, email, password)
            user.saveToDB()

            flash("Account made successfully!", category='success')
            return redirect(url_for('aboutPage'))

    return render_template('signup.html', sign_up_form = sign_up_form )

@app.route('/login', methods=["GET", "POST"])
def loginPage():
    login_form = LoginForm()
    if request.method == "POST":
        if login_form.validate():
            username = login_form.username.data
            password = login_form.password.data

            user = User.query.filter_by(username=username).first()
            if user:
                if user.password == password:
                    login_user(user)
                    flash(f'Successfully logged in! Welcome back {user.username}!', category='success')
                    return redirect(url_for('getPosts'))
                else:
                    flash("wrong password", category='danger')
            else:
                flash("user does not exist", category='danger')
    return render_template('login.html', login_form = login_form)

@app.route('/logout', methods=["GET"])
@login_required
def logoutRoute():
    logout_user()
    flash('Successfully logged out. See you soon!', category='success')
    return redirect(url_for('loginPage'))

@app.route('/admin', methods=["GET","POST"])
def adminPage():
    return render_template('admin.html')

@app.route("/profile", methods=["GET", "POST"])
def profile():
    edit_profile_form = EditProfileForm()
    user = User.query.filter_by(id = current_user.id).first()
    return render_template("profile.html", edit_profile_form = edit_profile_form, current_user = current_user)

@app.route("/editprofile", methods=["GET", "POST"])
@login_required
def editProfileForm():
    edit_profile_form = EditProfileForm()
    user = User.query.filter_by(id = current_user.id).first()
    
    if request.method == "POST":
        username = edit_profile_form.username.data
        email = edit_profile_form.email.data
        password = edit_profile_form.password.data
        if username != "":
            user.username = username
        if email != "":
            user.email = email
        if password != "":
            user.password = password
        user.saveChanges()
        return render_template('editdeleteprofile.html', edit_profile_form = edit_profile_form, current_user = current_user )
    return render_template('editdeleteprofile.html', edit_profile_form = edit_profile_form, current_user = current_user )

@app.route("/profile/editdelete", methods=["GET", "POST"])
@login_required
def delProfile():
    user = User.query.filter_by(id = current_user.id).first()
    if request.method == "POST":
        if user:
            user.deleteFromDB()
            return redirect(url_for("signUpPage"))
    return render_template("editdeleteprofile.html") 



@app.route('/products/create', methods=["GET","POST"])
@login_required
def createProduct():
    product_form = ProductForm()
    if current_user.username == 'admin':
        if request.method == "POST":
            if product_form.validate():
                product_name = product_form.product_name.data
                price = product_form.price.data
                img_file = product_form.img_file.data
                description = product_form.description.data

                img_file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],img_file.filename))
                flash("FILE HAS BEEN UPLOADED", category='success')
                
                product_post = Product(product_name, price, img_file.filename, description, current_user.id)
                product_post.saveToDB()
    else: 
        return redirect(url_for("homePage"))
            

    return render_template('createproduct.html', product_form = product_form)

@app.route('/posts', methods=["GET"])
def getPosts():
    posts = Product.query.all()
    return render_template('products.html', posts = posts )

@app.route('/posts/<int:post_id>', methods=["GET"])
def getPost(post_id):
    post = Product.query.get(post_id)
    return render_template('singleproduct.html', post = post )

@app.route('/posts/<int:post_id>/update', methods=["GET", "POST"])
@login_required
def updateProduct(post_id):
    post = Product.query.get(post_id)

    product_update_form = ProductForm()

    if current_user.username == 'admin':
        if request.method == "POST":
            if product_update_form.validate():
                product_name = product_update_form.product_name.data
                price = product_update_form.price.data
                img_file = product_update_form.img_file.data
                description = product_update_form.description.data
                post.product_name = product_name
                post.img_file = img_file
                post.description = description
                post.saveChanges()
                return redirect(url_for('getPost', post_id=post.id))
    else: 
        return redirect(url_for('homePage'))

    return render_template('updateproduct.html', post = post, product_update_form = product_update_form) 

@app.route("/posts/<int:post_id>/delete", methods=["GET"])
@login_required
def deleteProduct(post_id):
    post = Product.query.get(post_id)
    if current_user.username == 'admin':
        post.deleteFromDB()
    
    return redirect(url_for('getPosts'))

@app.route("/cart", methods=["GET"])
@login_required
def cart(user_id):
    product = Product.query.filter_by(user_id == current_user.id)
    return render_template('cart.html', product = product)

@app.route("/cart/<int:product_id>/add", methods=["GET","POST"])
@login_required
def addToCart(product_id):
    product = Product.query.get(product_id)
    product = Product.query.filter_by(Product.id == product_id).first()
    add_to_cart = Cart(current_user.id, product.id)
    add_to_cart.saveToDB()
    if request.method == 'POST':
        add_to_cart.saveToDB()

    return redirect(url_for('getPosts'))

