SELECT     publishers.name AS PublisherName, packages.name AS PackageName
FROM         publishers LEFT OUTER JOIN
                      packages ON publishers.app_dictionary_id = packages.app_dictionary_id