svn update --non-interactive --username molten_deploy --password 33uGudra /local/var/www/apps/molten4/_django_0_96_2

svn update --non-interactive --username molten_deploy --password 33uGudra /local/var/www/apps/molten4/pyro

chmod 0754 /local/var/www/apps/molten4/pyro/start-ns.sh
chmod 0754 /local/var/www/apps/molten4/pyro/start-server.sh

flip -u /local/var/www/apps/molten4/pyro/start-ns.sh
flip -u /local/var/www/apps/molten4/pyro/start-server.sh

svn update --non-interactive --username molten_deploy --password 33uGudra /local/var/www/apps/molten4/magma_molten_4
