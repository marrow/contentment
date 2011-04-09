## encoding: utf-8
<?xml version="1.0" encoding="UTF-8" ?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
# for node in nodes:
    <url>
        <loc>http://${web.request.host_url}${node.path}${'/' if isinstance(node, Folder) else ''}</loc>
        <priority>${max(1.0 - (len(node.parents) * 0.1, 0.1))}</priority>
        <lastmod>${(node.modified or node.created).strftime('%Y-%m-%d')}</lastmod>
##      <changefreq>monthly</changefreq> # TODO: Determine this from average change history.
    </url>
# endfor
</urlset>