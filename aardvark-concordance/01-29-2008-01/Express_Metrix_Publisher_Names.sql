SELECT     kbmanufacturer.name, kbapps.name AS AppName
FROM         kbmanufacturer LEFT OUTER JOIN
                      kbapps ON kbmanufacturer.manufacturerid = kbapps.manufacturerid
ORDER BY AppName