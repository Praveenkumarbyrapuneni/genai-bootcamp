import azure.functions as func
import logging
from api.main import app
import nest_asyncio

# Allow nested event loops (needed for Azure Functions)
nest_asyncio.apply()

# Create Azure Functions app
func_app = func.AsgiFunctionApp(app=app, http_auth_level=func.AuthLevel.ANONYMOUS)

logging.info('CareerPath AI Azure Function initialized')
