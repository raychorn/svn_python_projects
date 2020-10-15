#!/usr/bin/env perl

use perlux;
perlux::eval <<'EOF';
  print('Hello Lux, I am Perlite')
  dofile('run.lux')
EOF
