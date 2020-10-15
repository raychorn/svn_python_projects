from os.path import join

PREFIX     = "/usr"
LIBDIR     = "/usr/lib"
DATADIR    = "/usr/share"
DOCDIR     = "/usr/share/doc/cherokee"
WWWROOT    = "/var/www"
SYSCONFDIR = "/etc"
LOCALSTATE = "/var"
VERSION    = "0.99.7"

CHEROKEE_SERVER     = join (PREFIX, "sbin/cherokee")
CHEROKEE_WORKER     = join (PREFIX, "sbin/cherokee-worker")
CHEROKEE_ADMINDIR   = join (PREFIX, "share/cherokee/admin")
CHEROKEE_ICONSDIR   = join (PREFIX, "share/cherokee/icons")
CHEROKEE_THEMEDIR   = join (PREFIX, "share/cherokee/themes")
CHEROKEE_PANIC_PATH = join (PREFIX, "share/cherokee/cherokee-panic")
CHEROKEE_PLUGINDIR  = join (LIBDIR, "cherokee")
CHEROKEE_DATADIR    = join (DATADIR, "cherokee")
CHEROKEE_DEPSDIR    = join (DATADIR, "cherokee/deps")
CHEROKEE_CONFDIR    = join (SYSCONFDIR, "cherokee")
CHEROKEE_VAR_RUN    = join (LOCALSTATE, "run")
