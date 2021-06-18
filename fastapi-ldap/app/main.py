# Import dependencies
import uvicorn
from fastapi.responses import ORJSONResponse
from fastapi import FastAPI, Depends, status, Request, Query, Body, Response, Header

# Get version from static file
try:
    with open(".version") as reader:
        APP_VERSION = reader.read()
except:
    APP_VERSION = "0.0.0"
    print(".version doesn't exist !")

app = FastAPI(titre="Ldap API",
              description="This is a simple API",
              default_response_class=ORJSONResponse,  # Optimize JSON response
              version=APP_VERSION,
              )

if __name__ == "__main__":
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["default"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    log_config["formatters"]["default"]["datefmt"] = "%Y-%m-%d %H:%M:%S"
    log_config["formatters"]["access"]["datefmt"] = "%Y-%m-%d %H:%M:%S"
    uvicorn.run(app, host="0.0.0.0", port=80, log_level="info", log_config=log_config)
