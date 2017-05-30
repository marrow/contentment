# encoding: cinje

: from orderedset import OrderedSet
: from marrow.util.url import QueryString

: def render_video_block context, block
: """Render a YouTube video embed."""

: classes = OrderedSet(block.properties.get('cls', '').split() + ['block', 'video'])

: if 'width' in block.properties
	: classes.add('col-md-' + str(block.properties.width))
: end

<div&{id=block.properties.get('id', block.id), class_=classes}>
	<iframe width="560" height="315" src="https://www.youtube.com/embed/${block.video}" frameborder="0" allowfullscreen></iframe>
</div>

