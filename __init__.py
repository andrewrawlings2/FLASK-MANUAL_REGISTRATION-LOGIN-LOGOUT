
#FORMS FOR REGISTRATION AND LOGIN 

class RegistrationForm(FlaskForm):
	name=StringField('Name*', validators=[DataRequired()])
	username=StringField('Username*', validators=[DataRequired()])
	email=StringField('Email*', validators=[DataRequired()])
	password=PasswordField('Password*', validators=[DataRequired()])
	password2=PasswordField('Repeat Password*', validators=[DataRequired(), EqualTo('password')])
	submit=SubmitField('Register')
	
class LoginForm(FlaskForm):
	username=StringField('Username*', validators=[DataRequired()])
	password=PasswordField('Password*', validators=[DataRequired()])
	submit=SubmitField('Sign-In')

#REGISTRATION PAGE PLUS MYSQL INJECTION

@app.route('/register/', methods=['GET', 'POST'])
def register():
	try:
		form=RegistrationForm()
		
		if request.method == "POST" and form.validate():
			name = form.name.data
			username = form.username.data
			email = form.email.data
			password = (str(form.password.data))
			c, conn = connection()
			
			x = c.execute("SELECT * FROM accounts WHERE username = '{}'".format((thwart(username))))
			y = c.execute("SELECT * FROM accounts where email = '{}'".format((thwart(email))))
			
			if int(x) > 0:
				return redirect(url_for('username_error'))
				
			if int(y) > 0:
				return redirect(url_for('email_error'))
			
			else:
				c.execute("INSERT INTO accounts(name, username, email, password) VALUES(%s, %s, %s, %s)", (thwart(name), thwart(username), thwart(email), thwart(password)))
				conn.commit()
				c.close()
				conn.close()
				msg=Message("New User", sender="andrewrawlings2@gmail.com", recipients=["andrewrawlings2@gmail.com"])
				msg.body="New Account Registered\nName:{}\n Username: {}\n Email: {}\n".format(name, username, email)
				mail.send(msg)
				return redirect(url_for('registration_received'))
		return render_template('register.html', title='Register', form=form)
	
	except Exception as e:
		return(str(e))
    
    
#LOGIN PAGE AND MYSQL QUERY

@app.route('/login/', methods=["GET", "POST"])
def login():
	error=''
	try:
		form=LoginForm()
		
		c, conn = connection()
		if request.method == "POST" and form.validate():
		
			password = c.execute("SELECT password FROM accounts WHERE username = '{}'".format(thwart(form.username.data)))
			password = c.fetchone()[0]
			
			name = c.execute("SELECT name FROM accounts WHERE username = '{}'".format(thwart(form.username.data)))
			name = c.fetchone()[0]
			
			email = c.execute("SELECT email FROM accounts WHERE username = '{}'".format(thwart(form.username.data)))
			email = c.fetchone()[0]
			
			if (str(form.password.data)) == str(password):
				session['logged_in']=True
				session['username']= form.username.data
				session['name']=name
				session['email']=email
				return redirect(url_for('index'))
			else:
				return redirect(url_for('invalid_cred'))
			
		return render_template('login.html', title='Login', form=form)
	
	except Exception as e:
		return(str(e))

#LOGOUT

@app.route('/logout/')
def logout():
	session.clear()
	return render_template("logout.html", title="Logout-Success")
