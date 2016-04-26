# encoding: utf-8

import json
import logging
from web.core import local

from pygments import highlight
from pygments.formatters import Terminal256Formatter
from pygments.lexers.data import JsonLexer

from datetime import datetime

from pytz import utc

import cinje

try:
	bytes = bytes
except:
	bytes = str
	str = unicode


log = logging.getLogger(__name__)


def utcnow():
	return datetime.utcnow().replace(microsecond=0, tzinfo=utc)


def D_(trn, lang=None, fallback='en'):
	context = getattr(local, 'context', {})
	lang = getattr(context, 'lang', fallback) if lang is None else lang
	
	try:
		return trn.get(lang, trn.get(fallback, next(iter(trn.values()))))
	except StopIteration:
		if __debug__:
			log.debug("Missing language value for " + lang + ": " + repr(trn))
			# 1/0
			return "(!MISSING!)"
		return ""


def _(s):
	return s

def L_(s):
	return s


def annotate(_obj=None, **kw):
	def inner(obj):
		for key in kw:
			setattr(obj, key, kw[key])
		
		return obj
	
	if _obj is None:
		return inner
	
	return inner(_obj)


class JSONFormatter(logging.Formatter):
	REPR_FAIL_PLACEHOLDER = 'REPR_FAILED'
	BASE_TYPES = (int, float, bool, bytes, str, list, dict)
	
	default_exclude_attrs = {
		# python 2/3
		'args', 'name', 'msg', 'levelname', 'levelno', 'pathname', 'filename',
		'module', 'exc_info', 'exc_text', 'lineno', 'funcName', 'created',
		'msecs', 'relativeCreated', 'thread', 'threadName', 'processName',
		'process', 'getMessage', 'message', 'asctime',
		
		# python 3
		'stack_info',
	}

	def __init__(self, pretty=True, limit_keys_to=None, force_keys=None, **kwargs):
		super(JSONFormatter, self).__init__(**kwargs)
		self.limit_keys_to = limit_keys_to
		if force_keys:
			self.exclude_attrs = self.default_exclude_attrs - set(force_keys)
		else:
			self.exclude_attrs = self.default_exclude_attrs
		self.pretty = pretty

	def get_json(self, record, **kw):
		extra = {}
		for attr, value in record.__dict__.items():
			if ((self.limit_keys_to and attr in self.limit_keys_to) or
					(not self.limit_keys_to and attr not in self.exclude_attrs)):
				if isinstance(value, self.BASE_TYPES):
					extra[attr] = value
				else:
					try:
						extra[attr] = repr(value)
					except Exception:
						extra[attr] = self.REPR_FAIL_PLACEHOLDER
		if extra:
			try:
				return json.dumps(extra, **kw)
			except Exception as e:
				return json.dumps({
					'formatter_error': repr(e),
				}, **kw)
		return ''
	
	def format(self, record):
		formatted = logging.Formatter.format(self, record)
		json_string = self.get_json(record, indent='\t', separators=(',', ': '), sort_keys=True, skipkeys=True)
		
		if json_string:
			json_string = json_string.replace('\n', '\n\t')
			
			if self.pretty:
				return '\n\t'.join([formatted, highlight(json_string, JsonLexer(tabsize=4), Terminal256Formatter(style='monokai')).strip()])
			
			return '\n'.join([formatted, json_string]).strip()
		
		return formatted
