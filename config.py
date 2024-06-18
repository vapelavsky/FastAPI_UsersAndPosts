from environs import Env

env = Env()
env.read_env()

webserver_port = env.int("WEBSERVER_PORT", 8000)
debug_mode_flag = env.bool("DEBUG_MODE", False)
secret_key = env.str("SECRET_KEY")
exp_time = env.int("EXP_TIME")
algorithm = env.str("ALGORITHM")
db_user = env("DB_USER")
db_password = env("DB_PASSWORD")
db_host = env("DB_HOST")
db_port = env.int("DB_PORT")
db_name = env("DB_NAME")
db_driver = env("DB_DRIVER", "mysql+mysqlconnector")
arguments = env("DB_CONN_ARGUMENTS", "")
