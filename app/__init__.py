from flask_restplus import Api
from flask import Blueprint
from .main.controller.linkedin_controller import api as linkedin
from .main.controller.pitchbook_controller import api as pitchbook
from .main.controller.source_controller import api as Source
# from .main.controller.zoominfo_controller import api as zoominfo
# from .main.controller.dandb_controller import api as dandb
# from .main.controller.zippia_controller import api as zippia
from .main.service.constant_service import ConstantService
from logging.handlers import RotatingFileHandler
import logging

logging.basicConfig(
    handlers=[RotatingFileHandler(ConstantService.log_path() + '/social_media_crawl.log', backupCount=10)],
    level=logging.DEBUG,
    format=f'%(asctime)s %(api_key)s %(pathname)s %(filename)s %(module)s %(funcName)s %(lineno)d %(levelname)s %(message)s'
)

old_factory = logging.getLogRecordFactory()


def record_factory(*args, **kwargs):
    record = old_factory(*args, **kwargs)
    record.api_key = "KV2APP00003"
    return record


logging.setLogRecordFactory(record_factory)

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='Social Media Crawler Microservices',
          version='1.0',
          description='Crawl data from social media'
          )

api.add_namespace(linkedin, path='/linkedin')
api.add_namespace(pitchbook, path='/pitchbook')
api.add_namespace(Source, path='/sdmanager')
# api.add_namespace(zoominfo, path="/zoominfo")
# api.add_namespace(dandb, path='/dandb')
# api.add_namespace(zippia, path='/zippia')
