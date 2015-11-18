# encoding: cinje

:def properties element
	:_buff = []
	:for name, data in element._data.items()
<property name="${name}" &{data} />
		:_buff.extend(_buffer)
	:end
	:_buffer = _buff
:end
