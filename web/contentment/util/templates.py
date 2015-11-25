# encoding: cinje

:from marrow.package.canonical import name as module_name

:def properties element
\
	:dict_data = {}
	:for name, data in element._data.items()
		:if isinstance(data, str)
			:dict_data[name] = data
			:continue
		:end
<property name="${name}" \
		:if isinstance(data, dict)
&{data} />
		:else
type="${module_name(data)}">${_bless(data)}</property>
		:end
		:flush
	:end
	:if dict_data
<property&{dict_data} />
	:end
:end
