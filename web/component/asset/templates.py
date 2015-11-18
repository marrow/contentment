# encoding: cinje

:from web.component.asset.util import get_simple_fields, get_complex_fields


:def process data
	:return _bless(''.join(data))
:end


:def translated_field record, name, field
	:_buff = []
	:for lang, string in field.items()
<${name} lang="${lang}">${string}</${name}>\
		:_buff.extend(_buffer)
	:end
	:_buffer = _buff
:end


:INDENT = ' ' * 4
:def asset record, recursive, level=0
	:name = record.__class__.__name__
	:simple = {fn: fv for fn, fv in get_simple_fields(record)}
${INDENT * level}<${name}&{simple}>
	:flush
	:for field in get_complex_fields(record)
${INDENT * (level + 1)}${process(field)}
	:end
	:flush
	:if recursive
		:for child in record.children
			:yield from asset(child, True, level+1)
		:end
	:end
${INDENT * level}</${name}>
:end
