# encoding: cinje

:from marrow.package.canonical import name as module_name

:def properties element
	:for name, data in element._data.items()
<property name="${name}" \
		:if isinstance(data, dict)
&{data} />
		:else
type="${module_name(data)}">${_bless(data)}</property>
		:end
		:flush
	:end
:end
