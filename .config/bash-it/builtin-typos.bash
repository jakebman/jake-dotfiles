# shellcheck shell=bash

function typo {
	local key=${1?} val=${2?}
	alias -- "${key}=${val}"
}

#######################
## typos to builtins
## These typo aliases are expanded before we go into the command_not_found_handler
## Because that runs in a subshell, and in a subshell... doesn't help us in the outer shell
## It's not a great plan, but it's the best I have right now
#######################

typo alais alias

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
typo wpd pwd

typo tpe type
typo ype type
typo tyep type
typo tyoe type
typo yype type
typo typew type # ... because type already operates on its which (this might bite future me. Sorry, future me)

unset -f typo
