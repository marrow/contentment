# encoding: utf-8

import logging

from datetime import datetime

from pymongo.errors import PyMongoError
from mongoengine.errors import OperationError, NotUniqueError, ValidationError

from mongoengine import EmbeddedDocument, DynamicEmbeddedDocument, Document
from mongoengine import IntField, StringField, DateTimeField


class LogRuntime(EmbeddedDocument):
	identifier = IntField(db_field='i')
	name = StringField(db_field='n')
	

class LogLocation(EmbeddedDocument):
	path = StringField(db_field='p')
	line = IntField(db_field='l')
	module = StringField(db_field='o')
	function = StringField(db_field='f')


class LogException(EmbeddedDocument):
	message = StringField(db_field='m')
	trace = StringField(db_field='t')


class logData(DynamicEmbeddedDocument):
	pass


class Log(Document):
	meta = dict(
			collection = 'log',
			max_documents = 65535,
			max_size = 100 * 1024 * 1024,
			indexes = [
					('time', 'service', 'level')
				]
		)
	
	DEFAULT_PROPERTIES = logging.LogRecord('', '', '', '', '', '', '', '').__dict__.keys()
	
	service = StringField(db_field='s', default='__main__')
	level = IntField(db_field='l', default=logging.INFO)
	message = StringField(db_field='m')
	
	time = DateTimeField(db_field='w', default=datetime.utcnow)
	process = EmbeddedDocumentField(LogRuntime, db_field='p', default=None)
	thread = EmbeddedDocumentField(LogRuntime, db_field='t', default=None)
	location = EmbeddedDocumentField(LogLocation, db_field='o', default=LogLocation)
	exception = EmbeddedDocumentField(LogException, db_field='e', default=None)
	
	data = EmbeddedDocumentField(LogData, db_field='d', default=LogData)


class MongoEngineFormatter(logging.Formatter):
	def format(self, record):
		"""Formats LogRecord into a MongoEngine Log instance."""
		
		document = Log(
				service = record.name,
				level = record.levelno,
				message = record.getMessage(),  # TODO: Raw w/ positional if possible.
				
				time = datetime.fromtimestamp(record.created),
				process = LogRuntime(identifier=record.process, name=record.processName),
				thread = LogRuntime(identifier=record.thread, name=record.threadName),
				location = LogLocation(
						path = record.pathname,
						line = record.lineno,
						module = record.module,
						function = record.funcName
					)
			)
		
		if record.exc_info is not None:
			document.exception = LogException(
					message = str(record.exc_info[1]),
					trace = self.formatException(record.exc_info)
				)
		
		# Standard document decorated with extra contextual information
		
		if len(Log.DEFAULT_PROPERTIES) != len(record.__dict__):
			extras = set(record.__dict__).difference(set(Log.DEFAULT_PROPERTIES))
			for name in extras:
				setattr(document.data, name, record.__dict__[name])
		
		return document


class MongoEngineHandler(logging.Handler):
	def __init__(self, level=logging.NOTSET, concern=None, formatter=None, **options):
		"""Setting up mongo handler, initializing mongo database connection via pymongo."""
		super(MongoEngineHandler, self).__init__(level)
		
		self.buffer = []
		self.concern = concern or dict(w=0)
		self.formatter = formatter or MongoEngineFormatter()
		self.options = options
	
	def emit(self, record):
		"""Inserting new logging record to mongo database."""
		
		try:
			document = self.format(record)
		except:
			self.handleError(record)
		
		try:
			document.save(force_insert=True, validate=False, write_concern=self.concern)
			
			if self.buffer:
				Log.objects.insert(self.buffer, load_bulk=False, write_concern=self.concern)
				self.buffer = None  # Disable buffering of messages after startup.
		
		except (PyMongoError, OperationError, NotUniqueError, ValidationError):
			if self.buffer is None:  # Buffering is disabled.
				self.handleError(record)
			
			# During startup there might not be a DB connection yet, so we buffer messages until at least one can be
			# written, then we dump the buffer.
			self.buffer.append(document)
