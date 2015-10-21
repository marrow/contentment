# Contentment Dispatch

1. Determine the Site root node.
	* `HOST_NAME` search through `Site.domain.host`, or just Asset.name (with '' as a fallback).
2. Calculate potential paths from `SCRIPT_NAME` and `root.name`.
	* A combination of the requested path trimmed to every depth, deepest first.
3. Search for all possible matches.
	* Ordered by '-path' and limited to one to return the deepest node first.
	* No node, boom.
4. Consume all matching path elements.  (Leave unmatched.)
5. Combine (from the `parents` list) and evaluate the ACL.
6. Load the `handler` object.  The handler may be a reference to another asset, but must eventually resolve to a Python class.
7. Continue with standard dispatch (on the remaining path elements) from the discovered controller.
