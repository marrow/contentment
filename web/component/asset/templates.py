# encoding: cinje

:from web.component.asset.util import get_simple_fields, get_complex_fields, process_field


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


:def list_field record, name, field
<${name}>
	:flush
	:field_obj = record._fields[name].field
	:for fld in field
${INDENT}${process(process_field(fld, field_obj, name, record))}\
		:flush
	:end
</${name}>
:end


:def asset record, recursive, level=0
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
:end
