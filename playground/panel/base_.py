# encoding: cinje

: def wc_tabset context, panels

<div class="wc-properties panel" role="tabpanel">
	<ul class="wc-tabs" role="tablist">
		: for first, last, index, total, panel in iterate(panels)
		<li role="presentation"&{class="active" if first else None}>
			: identity = 'wc-cfg-' + panel.name
			<a role="tab" data-toggle="tab"&{href='#' + identity, aria_controls=identity, title=panel.title}>
				<i class="fa fa-${panel.icon} fa-lg"></i>
				<span class="sr-only">${panel.title}</span>
			</a>
		</li>
		: end
	</ul>
	<div class="tab-content">
		: for first, last, index, total, panel in iterate(panels):
		: classes = ['tab-pane', 'list-group'] + (['active'] if first else [])
		<ul role="tabpanel"&{id='wc-cfg-' + panel.name, class_=classes}>
			: use panel context
		</ul>
		: end
	</div>
</div>
