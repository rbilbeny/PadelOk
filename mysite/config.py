from getpass import getuser

# Database setup
username = getuser()        # you may put your username instead
password = "c00kieMonst3r"  # use your MySQL password
hostname = f"{username}.mysql.pythonanywhere-services.com"
databasename = f"{username}$asyncinweb"

SQLALCHEMY_DATABASE_URI = (
    f"mysql://{username}:{password}@{hostname}/{databasename}"
)
SQLALCHEMY_ENGINE_OPTIONS = {"pool_recycle": 299}
SQLALCHEMY_TRACK_MODIFICATIONS = False