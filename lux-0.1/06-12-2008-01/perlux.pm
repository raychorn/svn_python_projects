# perlux.pm -- Perl script interface to the perlux extension

package perlux;

use strict;
use vars qw($VERSION @ISA @EXPORT @EXPORT_OK);

require Exporter;
require DynaLoader;
require AutoLoader;

@ISA = qw(Exporter DynaLoader);
@EXPORT = qw(
	
);
$VERSION = '0.1';

bootstrap perlux $VERSION;

1;
__END__

=head1 NAME

perlux - Perl extension interface to Lux

=head1 SYNOPSIS

  use perlux;
  perlux::eval("print(123+456)");

=head1 DESCRIPTION

This is an interface to Lux.

=head1 AUTHOR

Jean-Claude Wippler

=head1 SEE ALSO

perl(1).

=cut
