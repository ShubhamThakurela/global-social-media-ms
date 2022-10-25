from flask_restplus import Namespace, fields


class LnkedininDto:
    api = Namespace('Linkedin', description='Semi-Structured data from linkedin')
    linkedin = api.model('linkedin', {})


class PitchbookDto:
    api = Namespace('Pitchbook', description='Semi-Structured data from pitchbook')
    pitchbook = api.model('pitchbook', {})

class SourceDto:
    api = Namespace('Source', description='Scrapped Download Manager')
    source = api.model('source', {})

class OwlerDto:
    api = Namespace('Owler', description='Semi-Structured data from owler')
    website = api.model('owler', {})

class ZoominfoDto:
    api = Namespace('Zoominfo', description='Semi-Structured data from zoominfo')
    zoominfo = api.model('zoominfo', {})


class DandBDto:
    api = Namespace('DnB', description='Semi-Structured data from DnB')
    dandb = api.model('DnB', {})

class ZippiaDto:
    api = Namespace('Zippia', description='Semi-Structured data from zippia')
    website = api.model('zippia', {})
