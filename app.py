from flask import Flask, render_template, request, redirect, url_for,session,flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from email.message import EmailMessage
from pytz import timezone
import smtplib
import os


UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
app.secret_key = os.urandom(24)  # Random 24-byte key
# ✅ Configurations 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rangaatma.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ✅ DB object
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# ✅ Database model
class CommonCRA(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50)) # 'carousel', 'why_rangatma', 'about_us', 'testimonial'
    img = db.Column(db.String(255))
    title = db.Column(db.String(100), nullable=True)
    subtitle = db.Column(db.String(150), nullable=True)
    description = db.Column(db.Text, nullable=True)


class WeServe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    img = db.Column(db.String(255))  # store relative static path
    sort_order = db.Column(db.Integer)

class OurProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    img = db.Column(db.String(255))  # store relative static path
    sort_order = db.Column(db.Integer)

class OurClient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    img = db.Column(db.String(255))
    sort_order = db.Column(db.Integer)

class Gallery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))      # Image title or name
    img = db.Column(db.String(255))        # Image file path (under /static/)
    sort_order = db.Column(db.Integer)     # For manual sorting

class AboutContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))            # 'about_us', 'competency', 'vision', 'mission', 'management_team'
    title = db.Column(db.String(255))          # Used for 'competency' only
    img1 = db.Column(db.String(255))           # Used for all types
    img2 = db.Column(db.String(255))           # Only for 'about_us'
    img3 = db.Column(db.String(255))           # Only for 'about_us'
    description = db.Column(db.Text)
    position = db.Column(db.Text)            # Used for all types founder and co-founder desk

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    img = db.Column(db.String(255))  # store relative static path
    sort_order = db.Column(db.Integer)

class MaterialsProcure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    img = db.Column(db.String(255))  
    sort_order = db.Column(db.Integer)

class ManufacturingFacility(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    main_title = db.Column(db.Text)
    title = db.Column(db.Text)
    description = db.Column(db.Text) 
    sort_order = db.Column(db.Integer)


class InspectionFacility(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    main_title = db.Column(db.Text)
    title = db.Column(db.Text)
    description = db.Column(db.Text) 
    sort_order = db.Column(db.Integer)

class WhyRangaatma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    description = db.Column(db.Text) 
    
class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    img = db.Column(db.Text) 
    description = db.Column(db.Text) 
    sort_order = db.Column(db.Integer)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.Text)
    email = db.Column(db.Text) 
    phone = db.Column(db.Text) 
    location = db.Column(db.Text)

class Capabilities(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    sort_order = db.Column(db.Integer, default=0)

class Footer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Text)
    title = db.Column(db.Text)
    icon = db.Column(db.Text) 
    link = db.Column(db.Text) 
    address = db.Column(db.Text)
    email = db.Column(db.Text) 
    phone = db.Column(db.Text) 
    
class CompanyCulture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    top_description = db.Column(db.Text, nullable=False)
    bottom_description = db.Column(db.Text, nullable=False)
    title = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text, nullable=False)
    sort_order = db.Column(db.Integer, default=0)

class WeAreHiring(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(255), nullable=False)
    qualification = db.Column(db.String(500), nullable=False)
    experience = db.Column(db.String(255), nullable=False)
    job_description = db.Column(db.Text, nullable=False)
    responsibilities = db.Column(db.Text)
    key_skills = db.Column(db.Text)

class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(256))

class EmailConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))


class CustomerQuery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(15))
    service = db.Column(db.String(200))
    message = db.Column(db.Text)
    submitted_at = db.Column(db.DateTime, server_default=db.func.now())
    is_read = db.Column(db.Boolean, default=False) 


# ......................................
# ✅ Check if filename is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# .........................................
@app.route('/create_db')
def create_db():
    db.create_all()
    return "Database & Tables created!"


# @app.route('/')
# def home():
#     carousel_data = CommonCRA.query.filter_by(type='carousel').all()
#     about_us = CommonCRA.query.filter_by(type='about_us').first()
#     why_rangatma = CommonCRA.query.filter_by(type='why_rangatma').first()
#     testimonials = CommonCRA.query.filter_by(type='testimonial').all() 
#     products = OurProduct.query.order_by(OurProduct.sort_order.asc()).all() 
#     weserve = WeServe.query.order_by(WeServe.sort_order.asc()).all()
#     clients = OurClient.query.order_by(OurClient.sort_order.asc()).all()

#     return render_template(
#         "index.html",
#         carousel_data=carousel_data,
#         about_us=about_us,
#         why_rangatma=why_rangatma,
#         testimonials=testimonials,
#         products=products,
#         weserve=weserve,
#         clients=clients
#     )

@app.route('/', methods=['GET', 'POST'])
def home():
    # Fetch display data
    carousel_data = CommonCRA.query.filter_by(type='carousel').all()
    about_us = CommonCRA.query.filter_by(type='about_us').first()
    why_rangatma = CommonCRA.query.filter_by(type='why_rangatma').first()
    testimonials = CommonCRA.query.filter_by(type='testimonial').all() 
    products = OurProduct.query.order_by(OurProduct.sort_order.asc()).all() 
    weserve = WeServe.query.order_by(WeServe.sort_order.asc()).all()
    clients = OurClient.query.order_by(OurClient.sort_order.asc()).all()

    # ✅ Handle contact form submit
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            service = request.form['service']
            message = request.form['message']

            # Save to DB
            new_query = CustomerQuery(
                name=name,
                email=email,
                phone=phone,
                service=service,
                message=message
            )
            db.session.add(new_query)
            db.session.commit()

            # Background email thread
            def send_email_background(app, name, email, phone, service, message):
                with app.app_context():
                    try:
                        config = EmailConfig.query.first()
                        hr_email = config.email
                        hr_password = config.password

                        msg = EmailMessage()
                        msg['Subject'] = f"New Contact Query from {name}"
                        msg['From'] = hr_email
                        msg['To'] = hr_email
                        msg.set_content(f"""
New Contact Form Submission:

Name    : {name}
Email   : {email}
Phone   : {phone}
Service : {service}

Message:
{message}
                        """)

                        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                            smtp.login(hr_email, hr_password)
                            smtp.send_message(msg)

                    except Exception as e:
                        print(f"❌ Email sending failed: {str(e)}")

            # Start email thread
            threading.Thread(target=send_email_background, args=(app, name, email, phone, service, message)).start()

            flash("✅ Message sent successfully!", "success")

        except Exception as e:
            db.session.rollback()
            flash(f"❌ Error: {str(e)}", "danger")

        return redirect(url_for('home'))

    return render_template(
        "index.html",
        carousel_data=carousel_data,
        about_us=about_us,
        why_rangatma=why_rangatma,
        testimonials=testimonials,
        products=products,
        weserve=weserve,
        clients=clients
    )





# @app.route('/about')
# def about():
#     return render_template("about.html", active_page='about')

@app.route('/about')
def about():
    # Fetch data by type
    about_us = AboutContent.query.filter_by(type='about_us').first()
    core_values = AboutContent.query.filter_by(type='core_value').all()
    competency = AboutContent.query.filter_by(type='competency').all()
    management = AboutContent.query.filter_by(type='management_team').first()
    vision = AboutContent.query.filter_by(type='vision').first()
    mission = AboutContent.query.filter_by(type='mission').first()
    
    return render_template(
        "about.html",
        active_page='about',
        about_us=about_us,
        core_values=core_values,
        competency=competency,
        management=management,
        vision=vision,         
        mission=mission 
    )

@app.route('/co_founder')
def co_founder():
    co_founder = AboutContent.query.filter_by(type='co_founder').first()
    return render_template("co_founder.html", active_page='co_founder',co_founder=co_founder,)


@app.route('/founder')
def founder():
    founder = AboutContent.query.filter_by(type='founder').first()
    return render_template("founder.html", active_page='founder',founder=founder,)



@app.route('/product')
def product():
    product_list = Products.query.order_by(Products.sort_order.asc()).all() 
    return render_template("product.html", active_page='product', products=product_list)


@app.route('/materials_procure')
def materials_procure():
    product_list = MaterialsProcure.query.order_by(MaterialsProcure.sort_order.asc()).all() 
    return render_template("materials_procure.html", active_page='materials_procure',products=product_list)



@app.route('/facilities')
def facilities():
    intro = ManufacturingFacility.query.filter(ManufacturingFacility.main_title != "").first()
    introtwo = InspectionFacility.query.filter(InspectionFacility.main_title != "").first()
    items = ManufacturingFacility.query.filter(ManufacturingFacility.sort_order != None).order_by(ManufacturingFacility.sort_order).all()
    itemstwo = InspectionFacility.query.filter(InspectionFacility.sort_order != None).order_by(InspectionFacility.sort_order).all()
    return render_template("facilities.html", active_page='facilities', intro=intro, items=items, introtwo=introtwo, itemstwo=itemstwo)


@app.route('/why_rangaatma')
def why_rangaatma():
    items = WhyRangaatma.query.all()
    return render_template("why_rangaatma.html", active_page='why_rangaatma', items=items)



@app.route('/achievements')
def achievements():
    items = Achievement.query.order_by(Achievement.sort_order.asc()).all()
    return render_template("achievements.html", active_page='achievements',items=items)


# @app.route('/career')
# def career():
#     return render_template("career.html", active_page='career')

# @app.route('/career')
# def career():
#     # Get top and bottom descriptions from row with id = 1
#     desc_row = CompanyCulture.query.filter_by(id=1).first()

#     # Get all items that have both title and description (excluding id=1)
#     points = CompanyCulture.query.filter(
#         CompanyCulture.title != None,
#         CompanyCulture.description != None,
#         CompanyCulture.id != 1
#     ).order_by(CompanyCulture.sort_order.asc()).all()

#     # ✅ Get all job posts
#     job_posts = WeAreHiring.query.order_by(WeAreHiring.id.desc()).all()

#     return render_template(
#         "career.html",
#         active_page='career',
#         top_desc=desc_row.top_description if desc_row else '',
#         bottom_desc=desc_row.bottom_description if desc_row else '',
#         points=points,
#         job_posts=job_posts 
#     )

import threading  # 🔄 Add this at the top (if not already)
@app.route('/career', methods=['GET', 'POST'])
def career():
    if request.method == 'POST':
        try:
            # ✅ Form data
            name = request.form['name']
            email = request.form['email']
            number = request.form['number']
            skill = request.form['skill']
            experience = request.form['experience']
            job = request.form['job']
            file = request.files['attachment']

            # ✅ Get HR Email & Password from DB
            config = EmailConfig.query.first()
            hr_email = config.email
            hr_password = config.password

            # ✅ Save uploaded resume temporarily
            resume_path = os.path.join('static/resumes', secure_filename(file.filename))
            file.save(resume_path)

            # ✅ Compose the Email
            msg = EmailMessage()
            msg['Subject'] = f"New Job Application - {job}"
            msg['From'] = hr_email
            msg['To'] = hr_email

            msg.set_content(f"""
Dear HR,

You have received a new job application.

Name       : {name}
Email      : {email}
Contact No.: {number}
Skills     : {skill}
Experience : {experience}
Applied For: {job}

The resume is attached with this email.

Regards,
Your Job Portal
            """)

            with open(resume_path, 'rb') as f:
                file_data = f.read()
                file_name = file.filename
                msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

            # ✅ Background email sending
            def send_email_in_background(msg, hr_email, hr_password, resume_path):
                try:
                    import smtplib
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                        smtp.login(hr_email, hr_password)
                        smtp.send_message(msg)
                except Exception as e:
                    print(f"❌ Failed to send email: {str(e)}")
                finally:
                    if os.path.exists(resume_path):
                        os.remove(resume_path)

            threading.Thread(target=send_email_in_background, args=(msg, hr_email, hr_password, resume_path)).start()

            flash("✅ Application submitted successfully!", "success")

        except Exception as e:
            flash(f"❌ Something went wrong: {str(e)}", "danger")

        return redirect(url_for('career'))

    # GET request handling
    desc_row = CompanyCulture.query.filter_by(id=1).first()

    points = CompanyCulture.query.filter(
        CompanyCulture.title != None,
        CompanyCulture.description != None,
        CompanyCulture.id != 1
    ).order_by(CompanyCulture.sort_order.asc()).all()

    job_posts = WeAreHiring.query.order_by(WeAreHiring.id.desc()).all()

    return render_template(
        "career.html",
        active_page='career',
        top_desc=desc_row.top_description if desc_row else '',
        bottom_desc=desc_row.bottom_description if desc_row else '',
        points=points,
        job_posts=job_posts
    )






# @app.route('/contact')
# def contact():
#     contact_info = Contact.query.first()
#     return render_template("contact.html", active_page='contact',contact_info=contact_info)


import threading

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    contact_info = Contact.query.first()

    if request.method == 'POST':
        try:
            # ✅ 1. Get form data
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            service = request.form['service']
            message = request.form['message']

            # ✅ 2. Save to database
            new_query = CustomerQuery(
                name=name,
                email=email,
                phone=phone,
                service=service,
                message=message
            )
            db.session.add(new_query)
            db.session.commit()

            # ✅ 3. Background email sending function
            def send_email_background(app, name, email, phone, service, message):
                with app.app_context():
                    try:
                        config = EmailConfig.query.first()
                        hr_email = config.email
                        hr_password = config.password

                        msg = EmailMessage()
                        msg['Subject'] = f"New Contact Query from {name}"
                        msg['From'] = hr_email
                        msg['To'] = hr_email
                        msg.set_content(f"""
New Contact Form Submission:

Name    : {name}
Email   : {email}
Phone   : {phone}
Service : {service}

Message:
{message}
                        """)

                        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                            smtp.login(hr_email, hr_password)
                            smtp.send_message(msg)

                    except Exception as e:
                        print(f"❌ Email sending failed: {str(e)}")

            # ✅ 4. Start thread
            threading.Thread(target=send_email_background, args=(app, name, email, phone, service, message)).start()

            # ✅ 5. Flash success immediately
            flash("✅ Message sent successfully!", "success")

        except Exception as e:
            db.session.rollback()
            flash(f"❌ Error: {str(e)}", "danger")

        return redirect(url_for('contact'))

    return render_template("contact.html", active_page='contact', contact_info=contact_info)




@app.route('/capabilities')
def capabilities():
    capabilities = Capabilities.query.order_by(Capabilities.sort_order.asc()).all()
    return render_template("capabilities.html", active_page='capabilities',capabilities=capabilities)

@app.route('/gallery')
def gallery():
    images = Gallery.query.order_by(Gallery.sort_order.asc()).all()
    return render_template("gallery.html", active_page='gallery',images=images)


@app.route('/our_client')
def our_client():
    return render_template("our_client.html", active_page='our_client')

#footer fetch data 
@app.context_processor
def inject_footer_data():
    footer_data = Footer.query.all()
    contact_info = Contact.query.first()  
    return dict(footer_data=footer_data, contact_info=contact_info)


#gmail send to company 







# Admin Home
from functools import wraps
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in first.", "warning")
            return redirect(url_for('admin_login'))  # or your login route
        return f(*args, **kwargs)
    return decorated_function




@app.route('/ms_admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users.query.filter_by(username=username).first()

        if not user:
            flash("Invalid username", "danger")
            return render_template("ms_admin/index.html")

        if not check_password_hash(user.password, password):
            flash("Incorrect password", "danger")
            return render_template("ms_admin/index.html")

        session['user_id'] = user.id
        # flash("Login successful", "success")
        return redirect(url_for("notification_data"))
    
    return render_template("ms_admin/index.html")


from datetime import datetime
from pytz import timezone, utc

@app.route('/notification_data')
@login_required
def notification_data():
    if 'user_id' not in session:
        flash("Please login first", "warning")

    queries = CustomerQuery.query.order_by(CustomerQuery.submitted_at.desc()).all()

    # Convert each query timestamp to IST
    ist = timezone('Asia/Kolkata')
    for q in queries:
        if q.submitted_at:
            q.submitted_at_ist = q.submitted_at.replace(tzinfo=utc).astimezone(ist)

    return render_template("ms_admin/notification_data.html", queries=queries)



@app.route('/edit_query/<int:query_id>', methods=['POST'])
def edit_query(query_id):
    query = CustomerQuery.query.get_or_404(query_id)
    query.name = request.form['name']
    query.email = request.form['email']
    query.phone = request.form['phone']
    query.service = request.form['service']
    query.message = request.form['message']
    db.session.commit()
    # flash("Query updated successfully", "success")
    return redirect(url_for('notification_data'))

@app.route('/delete_query/<int:query_id>', methods=['POST'])
def delete_query(query_id):
    query = CustomerQuery.query.get_or_404(query_id)
    db.session.delete(query)
    db.session.commit()
    # flash("Query deleted", "danger")
    return redirect(url_for('notification_data'))


@app.route('/mark-as-read/<int:query_id>', methods=['POST'])
def mark_as_read(query_id):
    query = CustomerQuery.query.get_or_404(query_id)
    query.is_read = True
    db.session.commit()
    return '', 204


@app.context_processor
def inject_unread_count():
    unread_count = CustomerQuery.query.filter_by(is_read=False).count()
    return dict(unread_count=unread_count)




@app.route('/password', methods=['GET', 'POST'])
@login_required
def password():
    if 'user_id' not in session:
        flash('Please login first', 'warning')
        return redirect(url_for('admin_login'))

    user = users.query.get(session['user_id'])

    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        # Old password check
        if not check_password_hash(user.password, old_password):
            flash('Old password is incorrect.', 'danger')
            return redirect(url_for('password'))

        # New and confirm match
        if new_password != confirm_password:
            flash('New and Confirm password do not match.', 'warning')
            return redirect(url_for('password'))

        # Update password
        user.password = generate_password_hash(new_password)
        db.session.commit()
        flash('Password updated successfully!', 'success')
        return redirect(url_for('password'))

    return render_template('ms_admin/password.html')



@app.route('/logout')
def logout():
    session.clear()  # Clears all session data
    flash("You have been logged out successfully.", "success")
    return redirect(url_for('admin_login'))  # Redirect to login page








# @app.route('/notification_data', methods=['GET', 'POST'])
# def notification_data():

#     return render_template('ms_admin/notification_data.html') 



# Home > Submenu
@app.route('/our_product', methods=['GET', 'POST'])
@login_required
def our_product():
    product_data = OurProduct.query.order_by(OurProduct.sort_order).all()
    return render_template('ms_admin/our_product.html', product_data=product_data)


@app.route('/ms_admin/our-product/add', methods=['POST'])
def add_our_product():
    title = request.form['title']
    file = request.files['img']
    filename = secure_filename(file.filename)
    filepath = os.path.join('static/uploads/', filename)
    file.save(filepath)

    # Step 1: Increase sort_order of all existing records
    existing_items = OurProduct.query.order_by(OurProduct.sort_order).all()
    for item in existing_items:
        item.sort_order += 1

    # Step 2: Insert new product at top
    new = OurProduct(title=title, img='uploads/' + filename, sort_order=1)
    db.session.add(new)
    db.session.commit()
    return redirect(url_for('our_product'))


@app.route('/ms_admin/our-product/update/<int:id>', methods=['POST'])
def update_our_product(id):
    row = OurProduct.query.get(id)
    row.title = request.form['title']
    if 'img' in request.files and request.files['img'].filename:
        file = request.files['img']
        filename = secure_filename(file.filename)
        filepath = os.path.join('static/uploads/', filename)
        file.save(filepath)
        row.img = 'uploads/' + filename
    db.session.commit()
    return redirect(url_for('our_product'))

@app.route('/ms_admin/our-product/delete/<int:id>')
def delete_our_product(id):
    OurProduct.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('our_product'))

@app.route('/ms_admin/our-product/update-order', methods=['POST'])
def update_our_product_order():
    order = request.get_json()
    for item in order:
        row = OurProduct.query.get(int(item['id']))
        row.sort_order = item['sort_order']
    db.session.commit()
    return jsonify({'status': 'success'})






@app.route('/we_serve', methods=['GET', 'POST'])
@login_required
def we_serve():
    data = WeServe.query.order_by(WeServe.sort_order).all()
    return render_template('ms_admin/we_serve.html', we_serve_data=data)

@app.route('/ms_admin/we-serve/add', methods=['POST'])
def add_we_serve():
    title = request.form['title']
    file = request.files['img']
    filename = secure_filename(file.filename)
    filepath = os.path.join('static/uploads/', filename)
    file.save(filepath)

    # Step 1: Push existing items down by 1
    existing_items = WeServe.query.order_by(WeServe.sort_order).all()
    for item in existing_items:
        item.sort_order += 1

    # Step 2: Add new item at sort_order = 1
    new = WeServe(title=title, img='uploads/' + filename, sort_order=1)
    db.session.add(new)
    db.session.commit()
    return redirect(url_for('we_serve'))


@app.route('/ms_admin/we-serve/update/<int:id>', methods=['POST'])
def update_we_serve(id):
    row = WeServe.query.get(id)
    row.title = request.form['title']
    if 'img' in request.files and request.files['img'].filename:
        file = request.files['img']
        filename = secure_filename(file.filename)
        filepath = os.path.join('static/uploads/', filename)
        file.save(filepath)
        row.img = 'uploads/' + filename
    db.session.commit()
    return redirect(url_for('we_serve'))

@app.route('/ms_admin/we-serve/delete/<int:id>')
def delete_we_serve(id):
    WeServe.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('we_serve'))

@app.route('/ms_admin/we-serve/update-order', methods=['POST'])
def update_we_serve_order():
    order = request.get_json()
    for item in order:
        row = WeServe.query.get(int(item['id']))
        row.sort_order = item['sort_order']
    db.session.commit()
    return jsonify({'status': 'success'})








@app.route('/our_clients', methods=['GET', 'POST'])
@login_required
def our_clients():
    client_data = OurClient.query.order_by(OurClient.sort_order).all()
    return render_template('ms_admin/our_clients.html', client_data=client_data)

@app.route('/ms_admin/our-clients/add', methods=['POST'])
def add_our_client():
    name = request.form['name']
    file = request.files['img']
    filename = secure_filename(file.filename)
    filepath = os.path.join('static/uploads/', filename)
    file.save(filepath)

    # Step 1: Shift existing clients' sort_order down by 1
    clients = OurClient.query.order_by(OurClient.sort_order).all()
    for c in clients:
        c.sort_order += 1

    # Step 2: Add new client at sort_order = 1
    new = OurClient(name=name, img='uploads/' + filename, sort_order=1)
    db.session.add(new)
    db.session.commit()
    return redirect(url_for('our_clients'))


@app.route('/ms_admin/our-clients/update/<int:id>', methods=['POST'])
def update_our_client(id):
    row = OurClient.query.get(id)
    row.name = request.form['name']
    
    if 'img' in request.files and request.files['img'].filename:
        file = request.files['img']
        filename = secure_filename(file.filename)
        filepath = os.path.join('static/uploads/', filename)
        file.save(filepath)
        row.img = 'uploads/' + filename

    db.session.commit()
    return redirect(url_for('our_clients'))

@app.route('/ms_admin/our-clients/delete/<int:id>')
def delete_our_client(id):
    OurClient.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('our_clients'))

@app.route('/ms_admin/our-clients/update-order', methods=['POST'])
def update_our_clients_order():
    order = request.get_json()
    for item in order:
        row = OurClient.query.get(int(item['id']))
        row.sort_order = item['sort_order']
    db.session.commit()
    return jsonify({'status': 'success'})





@app.route('/testimonials', methods=['GET', 'POST'])
@login_required
def testimonials():
    testimonial_data = CommonCRA.query.filter_by(type='testimonial').all()
    return render_template('ms_admin/testimonials.html', testimonial_data=testimonial_data)

@app.route('/update_testimonial/<int:id>', methods=['POST'])
def update_testimonial(id):
    row = CommonCRA.query.get_or_404(id)
    row.title = request.form['title']
    row.subtitle = request.form['subtitle']
    row.description = request.form['description']
    db.session.commit()
    return redirect(url_for('testimonials'))





@app.route('/c_r_about', methods=['GET', 'POST'])
@login_required
def c_r_about():
    carousel_data = CommonCRA.query.filter_by(type='carousel').all()
    why_data = CommonCRA.query.filter_by(type='why_rangatma').all()
    about_data = CommonCRA.query.filter_by(type='about_us').all()
    return render_template('ms_admin/c_r_about.html',
                           carousel_data=carousel_data,
                           why_data=why_data,
                           about_data=about_data)
    # return render_template('ms_admin/c_r_about.html')

# ---------- Update Routes ----------
# @app.route('/update_carousel/<int:id>', methods=['POST'])
# def update_carousel(id):
#     row = CommonCRA.query.get_or_404(id)
#     row.title = request.form['title']
#     row.subtitle = request.form['subtitle']

#     # Handle Image Upload
#     file = request.files.get('img')
#     if file and file.filename != '' and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         row.img = os.path.join(app.config['UPLOAD_FOLDER'], filename)

#     db.session.commit()
#     return redirect(url_for('c_r_about'))

@app.route('/update_carousel/<int:id>', methods=['POST'])
def update_carousel(id):
    row = CommonCRA.query.get_or_404(id)
    row.title = request.form['title']
    row.subtitle = request.form['subtitle']

    if 'img' in request.files and request.files['img'].filename:
        file = request.files['img']
        filename = secure_filename(file.filename)
        file.save(os.path.join('static/uploads/', filename))
        row.img = 'uploads/' + filename

    db.session.commit()
    return redirect(url_for('c_r_about'))

# @app.route('/update_why/<int:id>', methods=['POST'])
# def update_why(id):
#     row = CommonCRA.query.get_or_404(id)
#     row.description = request.form['description']

#     file = request.files.get('img')
#     if file and file.filename != '' and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         row.img = os.path.join(app.config['UPLOAD_FOLDER'], filename)

#     db.session.commit()
#     return redirect(url_for('c_r_about'))

@app.route('/update_why/<int:id>', methods=['POST'])
def update_why(id):
    row = CommonCRA.query.get_or_404(id)
    row.description = request.form['description']

    if 'img' in request.files and request.files['img'].filename:
        file = request.files['img']
        filename = secure_filename(file.filename)
        file.save(os.path.join('static/uploads/', filename))
        row.img = 'uploads/' + filename

    db.session.commit()
    return redirect(url_for('c_r_about'))

# @app.route('/update_about/<int:id>', methods=['POST'])
# def update_about(id):
#     row = CommonCRA.query.get_or_404(id)
#     row.description = request.form['description']

#     file = request.files.get('img')
#     if file and file.filename != '' and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         row.img = os.path.join(app.config['UPLOAD_FOLDER'], filename)

#     db.session.commit()
#     return redirect(url_for('c_r_about'))

@app.route('/update_about/<int:id>', methods=['POST'])
def update_about(id):
    row = CommonCRA.query.get_or_404(id)
    row.description = request.form['description']

    if 'img' in request.files and request.files['img'].filename:
        file = request.files['img']
        filename = secure_filename(file.filename)
        file.save(os.path.join('static/uploads/', filename))
        row.img = 'uploads/' + filename

    db.session.commit()
    return redirect(url_for('c_r_about'))




# About > Submenu
@app.route('/fetch_about_us', methods=['GET', 'POST'])
@login_required
def fetch_about_us():
    about_us = AboutContent.query.filter_by(type='about_us').first()
    competency = AboutContent.query.filter_by(type='competency').all()
    vision = AboutContent.query.filter_by(type='vision').first()
    mission = AboutContent.query.filter_by(type='mission').first()
    core_values = AboutContent.query.filter_by(type='core_value').all()
    management = AboutContent.query.filter_by(type='management_team').first()

    return render_template('ms_admin/fetch_about_us.html',
                           about_us=about_us,
                           competency=competency,
                           vision=vision,
                           mission=mission,
                           core_values = core_values,
                           management=management)

@app.route('/update_about_us', methods=['POST'])
def update_about_us():
    about_type = request.form.get('type')

    if about_type == 'competency':
        record_id = request.form.get('id')
        record = AboutContent.query.get(int(record_id))
        if record:
            record.title = request.form.get('title', record.title)
            record.description = request.form.get('description', record.description)
    elif about_type == 'core_value':
        record_id = request.form.get('id')
        if record_id:
            record = AboutContent.query.get(int(record_id))
            if record:
                record.title = request.form.get('title', record.title)
                record.description = request.form.get('description', record.description)

    else:
        record = AboutContent.query.filter_by(type=about_type).first()

        if not record:
            # flash("Record not found!", "danger")
            return redirect(url_for('fetch_about_us'))

        record.description = request.form.get('description', record.description)

        if about_type == 'management_team':
            record.title = request.form.get('title', record.title)
            record.position = request.form.get('position', record.position)

        if 'img1' in request.files and request.files['img1'].filename:
            img1 = request.files['img1']
            filename1 = secure_filename(img1.filename)
            filepath1 = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
            img1.save(filepath1)
            record.img1 = 'uploads/' + filename1

        if about_type == 'about_us':
            for img_key in ['img2', 'img3']:
                if img_key in request.files and request.files[img_key].filename:
                    img_file = request.files[img_key]
                    filename = secure_filename(img_file.filename)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    img_file.save(filepath)
                    setattr(record, img_key, 'uploads/' + filename)

    db.session.commit()
    # flash("Updated successfully!", "success")
    return redirect(url_for('fetch_about_us'))








@app.route('/fetch_founder', methods=['GET', 'POST'])
@login_required
def fetch_founder():
    founder = AboutContent.query.filter_by(type='founder').first()
    return render_template('ms_admin/fetch_founder.html',founder=founder)

@app.route('/admin/founder/edit/<int:id>', methods=['POST'])
def edit_founder(id):
    founder = AboutContent.query.get_or_404(id)
    founder.title = request.form['name']
    founder.position = request.form['position']
    founder.description = request.form['description']

    image_file = request.files.get('image')
    if image_file and image_file.filename:
        filename = secure_filename(image_file.filename)
        image_path = os.path.join('static/uploads', filename)
        image_file.save(image_path)
        founder.img1 = 'uploads/' + filename  

    db.session.commit()
    # flash("Founder updated successfully!", "success")
    return redirect(url_for('fetch_founder'))






@app.route('/fetch_co_founder', methods=['GET', 'POST'])
def fetch_co_founder():
    co_founder = AboutContent.query.filter_by(type='co_founder').first()
    return render_template('ms_admin/fetch_co_founder.html',co_founder=co_founder)

@app.route('/admin/co-founder/edit/<int:id>', methods=['POST'])
def edit_co_founder(id):
    record = AboutContent.query.get_or_404(id)
    record.title = request.form['name']
    record.position = request.form['position']
    record.description = request.form['description']

    file = request.files.get('image')
    if file and file.filename:
        filename = secure_filename(file.filename)
        file.save(os.path.join('static/uploads', filename))
        record.img1 = 'uploads/' + filename 

    db.session.commit()
    return redirect(url_for('fetch_co_founder'))







# Other Direct Pages
@app.route('/fetch_product', methods=['GET', 'POST'])
@login_required
def fetch_product():
    data = Products.query.order_by(Products.sort_order).all()
    return render_template('ms_admin/fetch_product.html',products_data=data)

@app.route('/ms_admin/fetch_product/add', methods=['POST'])
def add_products():
    title = request.form['title']
    file = request.files['img']
    filename = secure_filename(file.filename)
    filepath = os.path.join('static/uploads/', filename)
    file.save(filepath)

    # Step 1: Shift existing products' sort_order down by 1
    products = Products.query.order_by(Products.sort_order).all()
    for p in products:
        p.sort_order += 1

    # Step 2: Add new product with sort_order = 1
    new = Products(
        title=title,
        img='uploads/' + filename,
        sort_order=1
    )
    db.session.add(new)
    db.session.commit()
    return redirect(url_for('fetch_product'))


@app.route('/ms_admin/fetch_product/update/<int:id>', methods=['POST'])
def update_products(id):
    row = Products.query.get(id)
    row.title = request.form['title']
    if 'img' in request.files and request.files['img'].filename:
        file = request.files['img']
        filename = secure_filename(file.filename)
        filepath = os.path.join('static/uploads/', filename)
        file.save(filepath)
        row.img = 'uploads/' + filename
    db.session.commit()
    return redirect(url_for('fetch_product'))

@app.route('/ms_admin/fetch_product/delete/<int:id>')
def delete_products(id):
    Products.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('fetch_product'))

@app.route('/ms_admin/fetch_product/update-order', methods=['POST'])
def update_products_order():
    order = request.get_json()
    for item in order:
        row = Products.query.get(int(item['id']))
        row.sort_order = item['sort_order']
    db.session.commit()
    return jsonify({'status': 'success'})






@app.route('/fetch_materials_procure', methods=['GET', 'POST'])
@login_required
def fetch_materials_procure():
    data = MaterialsProcure.query.order_by(MaterialsProcure.sort_order).all()
    return render_template('ms_admin/fetch_materials_procure.html',materials_procure_data=data)

@app.route('/ms_admin/fetch_materials_procure/add', methods=['POST'])
def add_materials_procure():
    title = request.form['title']
    file = request.files['img']
    filename = secure_filename(file.filename)
    filepath = os.path.join('static/uploads/', filename)
    file.save(filepath)

    # Step 1: Shift all existing items down by 1
    existing_items = MaterialsProcure.query.order_by(MaterialsProcure.sort_order).all()
    for item in existing_items:
        item.sort_order += 1

    # Step 2: Add new item at top (sort_order = 1)
    new = MaterialsProcure(title=title, img='uploads/' + filename, sort_order=1)
    db.session.add(new)
    db.session.commit()
    return redirect(url_for('fetch_materials_procure'))


@app.route('/ms_admin/fetch_materials_procure/update/<int:id>', methods=['POST'])
def update_materials_procure(id):
    row = MaterialsProcure.query.get(id)
    row.title = request.form['title']
    if 'img' in request.files and request.files['img'].filename:
        file = request.files['img']
        filename = secure_filename(file.filename)
        filepath = os.path.join('static/uploads/', filename)
        file.save(filepath)
        row.img = 'uploads/' + filename
    db.session.commit()
    return redirect(url_for('fetch_materials_procure'))

@app.route('/ms_admin/fetch_materials_procure/delete/<int:id>')
def delete_materials_procure(id):
    MaterialsProcure.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('fetch_materials_procure'))

@app.route('/ms_admin/fetch_materials_procure/update-order', methods=['POST'])
def update_materials_procure_order():
    order = request.get_json()
    for item in order:
        row = MaterialsProcure.query.get(int(item['id']))
        row.sort_order = item['sort_order']
    db.session.commit()
    return jsonify({'status': 'success'})





# Facilities > Submenu
# @app.route('/manufacturing_facility', methods=['GET', 'POST'])
# def manufacturing_facility():
#     return render_template('ms_admin/manufacturing_facility.html')


# ------------------- Main View & Add -------------------
@app.route('/manufacturing_facility', methods=['GET', 'POST'])
@login_required
def manufacturing_facility():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        new_entry = ManufacturingFacility(title=title, description=description, sort_order=0)
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('manufacturing_facility'))

    main_title = ManufacturingFacility.query.get(1)
    data = ManufacturingFacility.query.filter(ManufacturingFacility.id != 1).order_by(ManufacturingFacility.sort_order).all()
    return render_template('ms_admin/manufacturing_facility.html', data=data, main_title=main_title)


# ------------------- Edit Main Title Only -------------------
# Update main title
@app.route('/manufacturing-facility/update-main-title', methods=['POST'])
def update_main_title():
    main = ManufacturingFacility.query.get(1)
    if main:
        main.main_title = request.form.get('main_title')
        db.session.commit()
    return redirect(url_for('manufacturing_facility'))

# ------------------- Edit Record -------------------
@app.route('/manufacturing-facility/edit/<int:id>', methods=['POST'])
def edit_facility(id):
    facility = ManufacturingFacility.query.get_or_404(id)
    facility.title = request.form.get('title')
    facility.description = request.form.get('description')
    db.session.commit()
    return redirect(url_for('manufacturing_facility'))

# ------------------- Delete Record -------------------
@app.route('/manufacturing-facility/delete/<int:id>', methods=['POST'])
def delete_facility(id):
    facility = ManufacturingFacility.query.get_or_404(id)
    db.session.delete(facility)
    db.session.commit()
    return redirect(url_for('manufacturing_facility'))

# ------------------- Sort Records -------------------
# Sortable
@app.route('/manufacturing-facility/sort', methods=['POST'])
def sort_facilities():
    if request.is_json:
        order = request.get_json().get('order')
        for index, item_id in enumerate(order):
            facility = ManufacturingFacility.query.get(item_id)
            if facility:
                facility.sort_order = index
        db.session.commit()
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': 'Invalid data'}), 400









# @app.route('/inspection_facility', methods=['GET', 'POST'])
# def inspection_facility():
#     return render_template('ms_admin/inspection_facility.html')

# ------------------- Main View & Add -------------------
@app.route('/inspection_facility', methods=['GET', 'POST'])
@login_required
def inspection_facility():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        new_entry = InspectionFacility(title=title, description=description, sort_order=0)
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('inspection_facility'))

    main_title = InspectionFacility.query.get(1)
    data = InspectionFacility.query.filter(InspectionFacility.id != 1).order_by(InspectionFacility.sort_order).all()
    return render_template('ms_admin/inspection_facility.html', data=data, main_title=main_title)


# ------------------- Edit Main Title Only -------------------
# Update main title
@app.route('/inspection-facility/update-main-title', methods=['POST'])
def update_inspection_main_title():
    main = InspectionFacility.query.get(1)
    if main:
        main.main_title = request.form.get('main_title')
        db.session.commit()
    return redirect(url_for('inspection_facility'))

# ------------------- Edit Record -------------------
@app.route('/inspection-facility/edit/<int:id>', methods=['POST'])
def edit_inspection_facility(id):
    facility = InspectionFacility.query.get_or_404(id)
    facility.title = request.form.get('title')
    facility.description = request.form.get('description')
    db.session.commit()
    return redirect(url_for('inspection_facility'))

# ------------------- Delete Record -------------------
@app.route('/inspection-facility/delete/<int:id>', methods=['POST'])
def delete_inspection_facility(id):
    facility = InspectionFacility.query.get_or_404(id)
    db.session.delete(facility)
    db.session.commit()
    return redirect(url_for('inspection_facility'))

# ------------------- Sort Records -------------------
# Sortable
@app.route('/inspection-facility/sort', methods=['POST'])
def sort_inspection_facilities():
    if request.is_json:
        order = request.get_json().get('order')
        for index, item_id in enumerate(order):
            facility = InspectionFacility.query.get(item_id)
            if facility:
                facility.sort_order = index
        db.session.commit()
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': 'Invalid data'}), 400






# Other Direct Pages
@app.route('/fetch_why_rangaatma', methods=['GET', 'POST'])
@login_required
def fetch_why_rangaatma():
    data = WhyRangaatma.query.all()
    return render_template('ms_admin/fetch_why_rangaatma.html', data=data)

@app.route('/why-rangaatma/edit/<int:id>', methods=['POST'])
def edit_why_rangaatma(id):
    item = WhyRangaatma.query.get_or_404(id)
    item.title = request.form['title']
    item.description = request.form['description']
    db.session.commit()
    return redirect(url_for('fetch_why_rangaatma'))








# @app.route('/fetch_achievements', methods=['GET', 'POST'])
# def fetch_achievements():
#     return render_template('ms_admin/fetch_achievements.html')


# ---------------------------------------
# Route: Fetch achievements
# ---------------------------------------
@app.route('/fetch_achievements', methods=['GET'])
@login_required
def fetch_achievements():
    achievements = Achievement.query.order_by(Achievement.sort_order).all() 
    return render_template('ms_admin/fetch_achievements.html', achievements=achievements)

# ---------------------------------------
# Route: Add new achievement
# ---------------------------------------
@app.route('/ms_admin/achievement/add', methods=['POST'])
def add_achievement():
    title = request.form['title']
    description = request.form['description']
    file = request.files['img']  # 👈 Get uploaded image
    filename = secure_filename(file.filename)
    filepath = os.path.join('static/uploads/', filename)
    file.save(filepath)

    # ✅ Step 1: Increment sort_order of existing records
    all_items = Achievement.query.order_by(Achievement.sort_order).all()
    for item in all_items:
        item.sort_order += 1

    # ✅ Step 2: Add new item with sort_order = 1
    new = Achievement(
        title=title,
        description=description,
        img='uploads/' + filename,  # 👈 Save relative image path
        sort_order=1
    )
    db.session.add(new)
    db.session.commit()
    return redirect(url_for('fetch_achievements'))


# ---------------------------------------
# Route: Update existing achievement
# ---------------------------------------
@app.route('/ms_admin/achievement/update/<int:id>', methods=['POST'])
def update_achievement(id):
    ach = Achievement.query.get_or_404(id)
    ach.title = request.form['title']
    ach.description = request.form['description']

    if 'img' in request.files and request.files['img'].filename:
        file = request.files['img']
        filename = secure_filename(file.filename)
        filepath = os.path.join('static/uploads/', filename)
        file.save(filepath)
        ach.img = 'uploads/' + filename

    db.session.commit()
    return redirect(url_for('fetch_achievements'))



# ---------------------------------------
# Route: Delete achievement
# ---------------------------------------
@app.route('/ms_admin/achievement/delete/<int:id>')
def delete_achievement(id):
    Achievement.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('fetch_achievements'))


# ---------------------------------------
# Route: Update sort order (drag and drop)
# ---------------------------------------
@app.route('/ms_admin/achievement/update-order', methods=['POST'])
def update_achievement_order():
    order = request.get_json()
    for item in order:
        row = Achievement.query.get(int(item['id']))
        row.sort_order = item['sort_order']
    db.session.commit()
    return jsonify({'status': 'success'})







# Route: Show all gallery items
@app.route('/fetch_gallery', methods=['GET', 'POST'])
@login_required
def fetch_gallery():
    gallery_data = Gallery.query.order_by(Gallery.sort_order).all()
    return render_template('ms_admin/fetch_gallery.html', gallery_data=gallery_data)

# Route: Add new gallery image
@app.route('/ms_admin/gallery/add', methods=['POST'])
def add_gallery():
    title = request.form['title']
    file = request.files['img']
    filename = secure_filename(file.filename)
    filepath = os.path.join('static/uploads/', filename)
    file.save(filepath)

    # Step 1: Shift existing items' sort_order down by 1
    galleries = Gallery.query.order_by(Gallery.sort_order).all()
    for g in galleries:
        g.sort_order += 1

    # Step 2: Insert new image at top (sort_order = 1)
    new = Gallery(
        title=title,
        img='uploads/' + filename,
        sort_order=1
    )
    db.session.add(new)
    db.session.commit()
    return redirect(url_for('fetch_gallery'))


# Route: Update existing gallery item
@app.route('/ms_admin/gallery/update/<int:id>', methods=['POST'])
def update_gallery(id):
    row = Gallery.query.get(id)
    row.title = request.form['title']
    if 'img' in request.files and request.files['img'].filename:
        file = request.files['img']
        filename = secure_filename(file.filename)
        filepath = os.path.join('static/uploads/', filename)
        file.save(filepath)
        row.img = 'uploads/' + filename
    db.session.commit()
    return redirect(url_for('fetch_gallery'))

# Route: Delete gallery item
@app.route('/ms_admin/gallery/delete/<int:id>')
def delete_gallery(id):
    Gallery.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('fetch_gallery'))

# Route: Update sort order of gallery items
@app.route('/ms_admin/gallery/update-order', methods=['POST'])
def update_gallery_order():
    order = request.get_json()
    for item in order:
        row = Gallery.query.get(int(item['id']))
        row.sort_order = item['sort_order']
    db.session.commit()
    return jsonify({'status': 'success'})






@app.route('/fetch_contact', methods=['GET', 'POST'])
@login_required
def fetch_contact():
    data = Contact.query.first()  # Only one row expected
    return render_template('ms_admin/fetch_contact.html',data=data)

@app.route('/ms_admin/contact/update', methods=['POST'])
def update_contact():
    row = Contact.query.first()
    if row:
        row.address = request.form['address']
        row.email = request.form['email']
        row.phone = request.form['phone']
        row.location = request.form['location']
    else:
        # Insert first row if not present
        row = Contact(
            address=request.form['address'],
            email=request.form['email'],
            phone=request.form['phone'],
            location=request.form['location']
        )
        db.session.add(row)
    
    db.session.commit()
    return redirect(url_for('fetch_contact'))




@app.route('/fetch_capabilities', methods=['GET', 'POST'])
@login_required
def fetch_capabilities():
    items = Capabilities.query.order_by(Capabilities.sort_order).all()
    return render_template('ms_admin/fetch_capabilities.html',items=items)

@app.route('/admin/capabilities/add', methods=['POST'])
def add_capability():
    title = request.form['title']
    count = Capabilities.query.count()
    new = Capabilities(title=title, sort_order=count + 1)
    db.session.add(new)
    db.session.commit()
    return redirect(url_for('fetch_capabilities'))

@app.route('/admin/capabilities/update/<int:id>', methods=['POST'])
def update_capability(id):
    item = Capabilities.query.get(id)
    item.title = request.form['title']
    db.session.commit()
    return redirect(url_for('fetch_capabilities'))

@app.route('/admin/capabilities/delete/<int:id>', methods=['POST'])
def delete_capability(id):
    item = Capabilities.query.get(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('fetch_capabilities'))

@app.route('/admin/capabilities/sort', methods=['POST'], endpoint='sort_capabilities')
def sort_capabilities():
    data = request.json
    for index, item_id in enumerate(data['order']):
        item = Capabilities.query.get(item_id)
        item.sort_order = index + 1
    db.session.commit()
    return jsonify({'message': 'Updated'})






# Career Submenu
# @app.route('/we_are_hiring', methods=['GET', 'POST'])
# @login_required
# def we_are_hiring():
#     return render_template('ms_admin/we_are_hiring.html')

@app.route('/we_are_hiring', methods=['GET', 'POST'])
@login_required
def we_are_hiring():
    jobs = WeAreHiring.query.order_by(WeAreHiring.id.desc()).all()
    return render_template('ms_admin/we_are_hiring.html', jobs=jobs)

@app.route('/add_we_are_hiring', methods=['POST'])
@login_required
def add_we_are_hiring():
    job_title = request.form['job_title']
    qualification = request.form['qualification']
    experience = request.form['experience']
    job_description = request.form['job_description']
    responsibilities = request.form['responsibilities']
    key_skills = request.form['key_skills']

    new_job = WeAreHiring(
        job_title=job_title,
        qualification=qualification,
        experience=experience,
        job_description=job_description,
        responsibilities=responsibilities,
        key_skills=key_skills,
    )
    db.session.add(new_job)
    db.session.commit()
    # flash("New job added successfully.", "success")
    return redirect(url_for('we_are_hiring'))

@app.route('/edit_we_are_hiring/<int:id>', methods=['POST'])
@login_required
def edit_we_are_hiring(id):
    job = WeAreHiring.query.get_or_404(id)
    job.job_title = request.form['job_title']
    job.qualification = request.form['qualification']
    job.experience = request.form['experience']
    job.job_description = request.form['job_description']
    job.responsibilities = request.form['responsibilities']
    job.key_skills = request.form['key_skills']

    db.session.commit()
    # flash("Job updated successfully.", "success")
    return redirect(url_for('we_are_hiring'))

@app.route('/delete_we_are_hiring/<int:id>', methods=['POST'])
@login_required
def delete_we_are_hiring(id):
    job = WeAreHiring.query.get_or_404(id)
    db.session.delete(job)
    db.session.commit()
    # flash("Job deleted successfully.", "success")
    return redirect(url_for('we_are_hiring'))








# @app.route('/company_culture', methods=['GET', 'POST'])
# @login_required
# def company_culture():
#     return render_template('ms_admin/company_culture.html')

@app.route('/company_culture')
@login_required
def company_culture():
    top = db.session.query(CompanyCulture.top_description).first()
    bottom = db.session.query(CompanyCulture.bottom_description).first()
    data = CompanyCulture.query.filter(CompanyCulture.title != '').order_by(CompanyCulture.sort_order).all()
    return render_template('ms_admin/company_culture.html',
                           top_description=top.top_description if top else '',
                           bottom_description=bottom.bottom_description if bottom else '',
                           data=data)

@app.route('/update_top_bottom_description', methods=['POST'])
@login_required
def update_top_bottom_description():
    dtype = request.form['type']
    value = request.form['description']

    row = db.session.query(CompanyCulture).first()
    if not row:
        row = CompanyCulture(title='', description='', sort_order=0, top_description='', bottom_description='')
        db.session.add(row)

    if dtype == 'top':
        row.top_description = value
    else:
        row.bottom_description = value

    db.session.commit()
    return redirect(url_for('company_culture'))

@app.route('/add_culture_point', methods=['POST'])
@login_required
def add_culture_point():
    title = request.form['title']
    description = request.form['description']
    max_sort = db.session.query(db.func.max(CompanyCulture.sort_order)).scalar() or 0
    new = CompanyCulture(title=title, description=description, sort_order=max_sort + 1,
                         top_description='', bottom_description='')
    db.session.add(new)
    db.session.commit()
    return redirect(url_for('company_culture'))

@app.route('/update_culture_point/<int:id>', methods=['POST'])
@login_required
def update_culture_point(id):
    row = CompanyCulture.query.get_or_404(id)
    row.title = request.form['title']
    row.description = request.form['description']
    db.session.commit()
    return redirect(url_for('company_culture'))

@app.route('/delete_culture_point/<int:id>')
@login_required
def delete_culture_point(id):
    row = CompanyCulture.query.get_or_404(id)
    db.session.delete(row)
    db.session.commit()
    return redirect(url_for('company_culture'))

@app.route('/sort_culture_points', methods=['POST'])
@login_required
def sort_culture_points():
    order = request.form.getlist('order[]')
    for idx, id in enumerate(order):
        row = CompanyCulture.query.get(int(id))
        if row:
            row.sort_order = idx
    db.session.commit()
    return '', 204








# footer page 
@app.route('/fetch_footer', methods=['GET', 'POST'])
@login_required
def fetch_footer():
    text_data = Footer.query.filter_by(type='text').all()
    contact_data = Footer.query.filter_by(type='contact').all()
    quick_links = Footer.query.filter_by(type='quick_links').all()
    our_services = Footer.query.filter_by(type='our_services').all()
    all_icons = Footer.query.filter_by(type='all_icon').all()
    
    return render_template(
        'ms_admin/fetch_footer.html',
        text_data=text_data,
        contact_data=contact_data,
        quick_links=quick_links,
        our_services=our_services,
        all_icons=all_icons
    )

@app.route('/footer/update', methods=['POST'])
def update_footer():
    id = request.form['id']
    type_ = request.form['type']

    if type_ == 'text':
        db.session.query(Footer).filter_by(id=id).update({
            'title': request.form['title']
        })

    elif type_ == 'contact':
        db.session.query(Footer).filter_by(id=id).update({
            'address': request.form['address'],
            'email': request.form['email'],
            'phone': request.form['phone']
        })

    elif type_ == 'quick_links' or type_ == 'our_services':
        db.session.query(Footer).filter_by(id=id).update({
            'title': request.form['title'],
            'link': request.form['link']
        })

    elif type_ == 'all_icon':
        db.session.query(Footer).filter_by(id=id).update({
            'icon': request.form['icon'],
            'link': request.form['link']
        })

    db.session.commit()
    return redirect('/fetch_footer')





#.................Gmail change .........
@app.route("/email-config", methods=["GET", "POST"])
@login_required
def email_config():
    config = EmailConfig.query.get(1)

    if request.method == "POST":
        config.email = request.form["email"]
        config.password = request.form["password"]
        db.session.commit()
        flash("Email and password updated successfully!", "success")
        return redirect(url_for("email_config"))

    return render_template("ms_admin/email_config.html", config=config)

# @app.route('/password', methods=['GET', 'POST'])
# def password():
#     return render_template('ms_admin/password.html')

# @app.route('/notification_data', methods=['GET', 'POST'])
# def notification_data():
#     return render_template('ms_admin/notification_data.html')





# ........................
from sqlalchemy import inspect, text

def delete_unused_images():
    used_images = set()
    inspector = inspect(db.engine)

    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        image_columns = [
            col['name'] for col in columns
            if 'img' in col['name'].lower() or 'image' in col['name'].lower() or col['name'] in ('img1', 'img2', 'img3')
        ]

        if image_columns:
            query = f"SELECT {', '.join(image_columns)} FROM {table_name}"
            result = db.session.execute(text(query))
            for row in result.fetchall():
                for value in row:
                    if value:
                        # ⬇️ ensure all values start with uploads/ (if not, add it)
                        path = value.replace('\\', '/').strip()
                        if not path.startswith('uploads/'):
                            path = f"uploads/{path}"
                        used_images.add(path)

    upload_folder = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    all_uploads_files = os.listdir(upload_folder)

    deleted_count = 0
    used_count = 0
    unused_count = 0

    for img in all_uploads_files:
        img_path = f"uploads/{img}".replace('\\', '/')
        full_img_path = os.path.join(upload_folder, img)

        if img_path in used_images:
            used_count += 1
        else:
            os.remove(full_img_path)
            deleted_count += 1
            unused_count += 1

    return used_count, unused_count, deleted_count






@app.route('/delete_unused_photos')
def delete_unused_photos():
    used, unused, deleted = delete_unused_images()
    return f'''
    Used Images: {used}<br>
    Unused Images: {unused}<br>
    {deleted} unused images deleted.
    '''





# ..............................


# local server use 
# if __name__ == '__main__':
#     with app.app_context(): 
#         db.create_all()
#     app.run(debug=True)


# Only for live server (OPTIONAL)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
