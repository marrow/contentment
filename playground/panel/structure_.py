# encoding: cinje

: def wc_panel_structure context

# <a href="#" style="display: inline-block; margin: -10px;"><sup style="display: inline-block; padding: 10px 10px 0;"><i class="fa fa-question-circle small"></i></sup></a>

<li class="list-group-item">
	<h4>
		Site Structure
	</h4>
	<menu class="list-unstyled wc-cfg-flist">
		: from web.component.asset.model import Asset
		: for child in Asset.objects.only('id').get(path='/careers.illicohodes.com').children
			<li>
				<a href="${child.path[24:]}">
					<i class="fa fa-${child.__icon__} fa-lg fa-fw"></i>
					${child.title['en']}
				</a>
				: if child.children.count()
				<menu class="list-unstyled">
				: for descendant in child.children
					<a href="${descendant.path[24:]}">
						<i class="fa fa-${descendant.__icon__} fa-lg fa-fw"></i>
						${descendant.title['en']}
					</a>
					: if descendant.children.count()
					<menu class="list-unstyled">
					: for d2 in descendant.children
						<a href="${d2.path[24:]}">
							<i class="fa fa-${d2.__icon__} fa-lg fa-fw"></i>
							${d2.title['en']}
						</a>
					: end
					</menu>
					: end
				: end
				</menu>
				: end
			</li>
		: end
	</menu>
</li>