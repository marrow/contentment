# encoding: cinje

: from .common_ import base_block_list_item

: def reference_block_list_item block, wrap=False
	: using base_block_list_item block, True
		<a&{href=block.target.path, class_={'fa', 'fa-bullseye'}, title=block.target.path}></a>
	: end
: end


: def render_reference_block context, block, content
: classes = set(block.properties.get('cls', '').split())

: if 'width' in block.properties
	: classes.add('col-md-' + str(block.properties.width))
: end

<div&{id=block.properties.get('id', block.id), class_=classes}>
: if callable(content)
	: use content context
: else
	: _buffer.extend(content)
: end
</div>
