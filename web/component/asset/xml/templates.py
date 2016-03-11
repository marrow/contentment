# encoding: cinje

:from web.component.asset.xml import get_simple_fields, get_complex_fields, process_field


:INDENT = ' ' * 4


:def process data
	:return _bless(''.join(data))
:end


:def translated_field record, name, field
	:for lang, string in field.items()
<${name} lang="${lang}">${string}</${name}>
		:flush
	:end
:end


:def text_block_content record, name, field
	:for lang, string in field.items()
		:strings = string.splitlines()
<${name} lang="${lang}"><![CDATA[\
		:if len(strings) == 1
${_bless(strings.pop(0))}]]>\
		:end
		:for entry in iterate(strings)
			:if not entry.first
${INDENT}\
			:end
${_bless(entry.value)}
			:if entry.last
				:_buffer.insert(-1, ']]>')
			:end
			:flush
		:end
</${name}>
		:flush
	:end
:end


:def asset record, recursive=False, level=0, root=False
\
	:if root
<?xml version="1.0" encoding="utf-8"?>
<Extract xmlns="https://xml.webcore.io/component/asset/1.0">
		:level += 1
	:end
	:name = record.__class__.__name__
${INDENT * level}<${name}\
	:for simple in get_simple_fields(record)
&{[simple]}\
	:end
>
	:flush
	:for field in get_complex_fields(record, level=level)
		:if not field
			:continue
		:end
${INDENT * (level + 1)}${_bless(field)}\
	:end
	:flush
	:if recursive
		:for child in getattr(record, 'children', [])
			:yield from asset(child, True, level+1)
		:end
	:end
${INDENT * level}</${name}>
	:if root
</Extract>
	:end
:end


:def block record, level
	:for entry in iterate(asset(record, level=1))
		:for ientry in iterate(entry.value.splitlines())
\
			:if not (entry.first and ientry.first)
${INDENT * (level + 1)}\
			:end
${_bless(ientry.value)}
			:flush
		:end
	:end
:end


:def list_field record, name, field, level
:if not field
	:return
:end
<${name}>
	:flush
	:field_obj = record._fields[name].field
	:for fld in field
${process(process_field(fld, field_obj, name, record, level=level, _in_list=True))}\
		:flush
	:end
</${name}>
:end


:def reference_field record, name, field
<${name} collection="${field.collection}" id="${field.id}" />
:end


:def datetime_field record, name, field
:from datetime import datetime
:from . import DATETIME_FORMAT
<${name} at="${field.strftime(DATETIME_FORMAT)}" />
:end


:def embedded_document record, name, field
	:if not getattr(record, name, None)
		:return
	:end
<${name}>
	:for line in field
${_bless(line)} \
	:end
</${name}>
:end
