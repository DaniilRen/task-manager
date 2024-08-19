import os, sys

user_name = "" # place here user name from host
domen = "" # place here website domen

activate_this = f"/home/{user_name}/python/bin/activate_this.py"
with open(activate_this) as f:
   exec(f.read(), {'__file__': activate_this})
sys.path.insert(0, os.path.join(f"/home/{user_name}/domains/{domen}/public_html/"))
from main import app as application

if __name__ == "__main__":
    application.run()
