# encoding: cinje

:def properties element
	:for name, data in element._data.items()
<property name="${name}" &{data} />
		:flush
	:end
:end
