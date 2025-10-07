
# Project-Jump Disambiguation

This folder exists to be placed on the $BASH_IT_PROJECT_PATHS list. When you're getting an ambiguity in `pj u<TAB>` that you want to be *very* clear is in fact `pj uinode-clientservice`, and not `pj utils`, you put a symlink to wherever `uinode-clientservice` lives into this directory, named `u`.

Because pj jumps to the next tab completion, you generally need only one of these at every disambiguation prefix.
So, for abc, alphabet-tiles, and alphabet-soup, you only need to disambiguate at `a`, and `alphabet-`.
Feel free to use a name earlier up the chain, so `alphabet` is also fine too.
