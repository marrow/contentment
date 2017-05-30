# encoding: cinje

: import traceback
: from marrow.package.canonical import name

: log = __import__('logging').getLogger(__name__)


: def render_page_panel context, page, wrap
	: from web.component.asset.render import render_asset_panel
	: using render_asset_panel context, page, True
		<li class="list-group-item" id="wc-blocks">
			<h4>
				Block Structure
				<a href="#" style="display: inline-block; margin: -10px;"><sup style="display: inline-block; padding: 10px 10px 0;"><i class="fa fa-question-circle small"></i></sup></a>
			</h4>
			
			<menu class="" id="wc-page-blocks" data-asset="${context.asset.path}">
				: for block in page.content
					: use block._block_list_item
				: end
			</menu>
		</li>
	: end
: end


: def render_block context, page, block
	: try
		: use block.__html_stream__ context
	: except
		: log.exception("Error processing block: " + repr(block), extra=dict(block=block.id, page=page.id))
		: if __debug__
			<pre class="text-error"><code>${traceback.format_exc()}</code></pre>
		: else
			<b class="text-error">An unknown error occurred.</b>
		: end
	: end
: end


: def render_page_content context, page
	# Load page content if not already loaded.
	: content = page.content if page.content else page.__class__.objects.scalar('content').get(id=page.id)
	
	: columns = False
	: width = 12
	
	: for block in page.content
		: size = block.properties.get('width', 12)
		: width -= size
		
		: if width and not columns
			: columns = True
<div class="container row-fluid clearfix">
		: end
		
		: use render_block context, page, block

		: if width <= 0
			: width = 12
			: if columns
				: columns = False
</div>
			: end
		: end
	: end

	: if columns
</div>
	: end
	
	: end
: end


: def render_page context, asset

	# First, we work out what the title should look like.
	: title = [str(asset), str(context.croot)]
	: if context.croot.properties.get('direction', 'rtl') == 'ltr'
		: title.reverse()
	: end
	: title = context.croot.properties.get('separator', ' - ').join(title)
	: title = title.upper() if context.croot.properties.get('titlecase', 'normal') == 'upper' else title
	: classes = set()
	: classes.update(context.croot.properties.get('cls', '').split())
	: classes.update(asset.properties.get('cls', '').split())
	: styles = context.croot.properties.get('styles', 'site').split()
	: styles = ['/public/css/{}.css'.format(i) for i in styles]
	: scripts = context.croot.properties.get('scripts', 'site').split()
	: scripts = ['/public/js/{}.js'.format(i) for i in scripts]
	
	: using context.theme context, title=title, styles=styles, scripts=scripts, lang=context.lang, class_=classes

<article data-theme="${name(context.theme)}">

	: flush

	: for chunk in asset.__html_stream__(context)
		: yield chunk
	: end

</article>

	: if not __debug__ and 'ua' in context.croot.properties
<script>
(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
})(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

ga('create', '${context.croot.properties.ua}', 'auto');
ga('send', 'pageview');
</script>
	: end

	: end

	: flush
: end
