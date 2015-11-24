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
<${name} lang="${lang}"><![CDATA[${_bless(string)}]]></${name}>
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
	:simple = {fn: fv for fn, fv in get_simple_fields(record)}
${INDENT * level}<${name}&{simple}>
	:flush
	:for field in get_complex_fields(record)
		:if not field
			:continue
		:end
${INDENT * (level + 1)}${process(field)}\
	:end
	:flush
	:if recursive
		:for child in record.children
			:yield from asset(child, True, level+1)
		:end
	:end
${INDENT * level}</${name}>
	:if root
</Extract>
	:end
:end


:def block record
	:yield from asset(record)
:end


:def list_field record, name, field
:if not field
	:return
:end
<${name}>
	:flush
	:field_obj = record._fields[name].field
	:for fld in field
${INDENT}${process(process_field(fld, field_obj, name, record))}\
		:flush
	:end
</${name}>
:end


:def reference_field record, name, field
<dbref collection="${field.collection}" id="${field.id}" />
:end


:def datetime_field record, name, field
:from datetime import datetime
:from . import DATETIME_FORMAT
<${name} at="${field.strftime(DATETIME_FORMAT)}" />
:end
