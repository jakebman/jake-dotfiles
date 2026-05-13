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

# Don't evaluate this in normal-typo-land, otherwise `alais -p` will also print typo aliases
typo alais alias

# All typos of cd need to live here, otherwise they won't be able to actually change the directory
typo CD cd # doesn't get helped by my allcaps typo fixer, because that's executed in a subshell
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
typo cd- 'cd -'
typo xs cd
typo qcd cd    # I quit less *twice*, then wanted to cd
typo lcd cd    # I tried to ls, then decided to change directories instead
typo treecd cd # Ditto, but tree. Wow.

typo cdg cdgit
typo dg cdgit  # really a typo of cdg, but shortening the loop
typo dgc cdgit # I... really just mashed keys there
typo dfg cdgit

# pj is cd-like
typo puj pj
typo pjh pj
typo '[k' pj # right hand moved one to the right

unset -f typo
