import os

def getEnviromentVariable(env_var_name:str)->str:
    env =  os.getenv(env_var_name)
    if env is None:
        raise ValueError(f"Missing required environment variable: {env_var_name}")
    return env