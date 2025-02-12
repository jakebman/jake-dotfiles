# shellcheck shell=bash

function typo {
	local key=${1?} val=${2?}
	alias -- "${key}=${val}"
}

#######################
## typos to builtins
## A bad shim until I figure something better
#######################

typo '~cd' cd
typo foo 'cd foo'
typo vd cd
typo vf cd # left hand misaligned
typo dc cd
typo ce cd
typo ced cd
typo dcd cd
typo ccd cd
typo cdc cd
typo xs cd
typo qcd cd    # I quit less *twice*, then wanted to cd
typo lcd cd    # I tried to ls, then decided to change directories instead
typo treecd cd # Ditto, but tree. Wow.

typo cdg cdgit

typo hsitory history
typo pws pwd

typo tpe type
typo ype type
typo tyep type
typo tyoe type
typo yype type
typo typew type # ... because type already operates on its which (this might bite future me. Sorry, future me)
