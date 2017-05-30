# encoding: cinje

: from orderedset import OrderedSet
: from marrow.util.url import QueryString

: def render_map_block context, block
: """Render a Google Maps embed."""

# Prepare HTML attributes for later emitting.
: frame_properties = dict(width="100%", height="100%", frameborder=0, allowfullscreen=True)
: frame_properties['src'] = "https://www.google.com/maps/embed/v1/" + block.kind
: frame_query = dict(key='AIzaSyAwxafzh1CdOp5WUltjcsxLIjum2tm9w98', maptype=block.style, language='en', region='ca')
: classes = OrderedSet(block.properties.get('cls', '').split() + ['map', block.kind])

: if 'width' in block.properties
	: classes.add('col-md-' + str(block.properties.width))
: end

: if block.center
	: frame_query['center'] = ",".join(reversed(block.center))
: end

: if block.zoom is not None
	: frame_query['zoom'] = block.zoom
: end

: if block.kind in ("place", "search")
	: frame_query['q'] = block.query

: elif block.kind == "directions"
	: frame_query['origin'] = block.origin
	: frame_query['destination'] = block.destination
	
	: if block.avoid
		: frame_query['avoid'] = block.avoid
	: end

: end

# Construct the final URL.
: frame_properties['src'] = frame_properties['src'] + "?" + QueryString(frame_query).render()

<div&{id=block.properties.get('id', block.id), class_=classes}>
	<iframe&{frame_properties}></iframe>
</div>
