# encoding: cinje

: def render_asset_panel context, asset, wrap=False
	<li class="list-group-item">
		<h4>
			General
			<a href="#" style="display: inline-block; margin: -10px;"><sup style="display: inline-block; padding: 10px 10px 0;"><i class="fa fa-question-circle small"></i></sup></a>
		</h4>
		<dl>
			<dt>Name</dt>
			<dd>${context.asset.name}</dd>
			<dt>Title</dt>
			<dd>${context.D(context.asset.title)}</dd>
			<dt>Description</dt>
			: if context.asset.description.get(context.lang, None)
			<dd>${context.asset.title[context.lang]}</dd>
			: else
			<dd><em>None entered.</em></dd>
			: end
			<dt>Tags</dt>
			: if context.asset.tags
			<dd>${','.join(context.asset.tags)}</dd>
			: else
			<dd><em>None entered.</em></dd>
			: end
			<dt>Created</dt>
			<dd>${context.asset.created.isoformat()}</dd>
			<dt>Modified</dt>
			<dd>${context.asset.modified.isoformat()}</dd>
		</dl>
	</li>
	: if wrap
		: yield
	: end
:


