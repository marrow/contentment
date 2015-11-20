# encoding: cinje

:def properties element
	:for name, data in element._data.items()
<property name="${name}" \
		:if isinstance(data, dict)
&{data} />
		:else
type="${type(data).__name__}">${_bless(data)}</property>
		:end
		:flush
	:end
:end
