import bcrypt
import hashlib
import pymysql

def register_user(name, email, password):
  """Registers a new user on the e-commerce platform.

  Args:
    name: The user's name.
    email: The user's email address.
    password: The user's password.

  Returns:
    True if the user was successfully registered, False otherwise.
  """

  # Validate the user's input.
  if not name or not email or not password:
    return False

  # Check if the user already exists.
  db = pymysql.connect(host='localhost', user='root', password='', db='ecommerce')
  cursor = db.cursor()
  cursor.execute('SELECT COUNT(*) FROM users WHERE email = %s', (email,))
  user_count = cursor.fetchone()[0]
  db.close()

  if user_count > 0:
    # The user already exists.
    return False

  # Hash the user's password.
  hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

  # Insert the user's data into the database table.
  db = pymysql.connect(host='localhost', user='root', password='', db='ecommerce')
  cursor = db.cursor()
  cursor.execute('INSERT INTO users (name, email, password) VALUES (%s, %s, %s)', (name, email, hashed_password))
  db.commit()
  db.close()

  return True