## encoding: utf-8
<?xml version="1.0" encoding="UTF-8" ?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
% for asset in nodes:
    <url>
        <loc>${web.request.host_url}${asset.path}${'/' if isinstance(node, Folder) else ''}</loc>
        <priority>${max(1.0 - len(asset.parents) * 0.1, 0.1)}</priority>
        <lastmod>${(asset.modified or asset.created).strftime('%Y-%m-%d')}</lastmod>
##      <changefreq>monthly</changefreq> # TODO: Determine this from average change history.
    </url>
% endfor
</urlset>