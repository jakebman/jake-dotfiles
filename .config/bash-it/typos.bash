# shellcheck shell=bash

# There's an outer command called typo, so we use a temporary alias within that file to allow
# easy access to typo declaration without overwriting the outer function
function _generate_typo_as_alias {
	local key=${1?} val=${2?}
	alias -- "${key}=${val}"
}
alias typo=_generate_typo_as_alias
shopt -s expand_aliases

# TODO: if there's a makefile, could we pre-load its targets as typo options?
# TODO: if the completion is trying to look up a command (_completion_loader?), can it check here too?

if [ -f pom.xml ]; then
	# We're in maven-land, baby!
	declare -a IMPLICIT_MAVEN
	mapfile -t IMPLICIT_MAVEN < <(grep -v "^#" < "$(dirname "$BASH_SOURCE")/maven-goals-and-phases.list" | grep -v '^\s*$')
	declare _IMPLICIT_MAVEN
	for _IMPLICIT_MAVEN in "${IMPLICIT_MAVEN[@]}"; do
		typo "$_IMPLICIT_MAVEN" "mvn ${_IMPLICIT_MAVEN}"
	done
	unset _IMPLICIT_MAVEN IMPLICIT_MAVEN
else
	typo clean 'make clean'
fi

if [ -f package.json ]; then
	# NPM-land!
	# Not the smartest. I'm just assuming there's a `scripts.dev: nodemon...` entry.
	# I'd prefer this to try and guess the script I've most-recently run, not just use dev
	typo rs 'npm run dev'
fi

# a "complex typo", because it could mean several things
# Specifically, don't make the definition of this dependent on the presence of package.json -
# it should be clear from its definition that it chooses between two options.
function run {
	if [ -f package.json ]; then
		# probably npm run
		npm-run "$@"
	elif [ -f pom.xml ]; then
		# probably maven
		mvn spring-boot:run "$@"
	else
		# probably docker run
		docker-run "$@"
	fi
}

function npm-run {
	: "I don't feel like making a jake-npm bash-it plugin at this exact moment"
	if [ "$#" -eq 0 ]; then
		set -- "${JAKE_TYPO_NPM_RUN_DEFAULT_TARGET:-dev}"
	fi
	npm run "$@"
}

# pre-emptive
typo npmrun npm-run

typo viim vim
typo vbim vim
typo vimi vim
typo vimn vim # actual
typo vinm vim # actual
typo vimm vim # speculative
typo viom vim
typo vom vim
typo ivm vim
typo vmi vim
typo vin vim
typo vun vim # right hand shifted left by one
typo gim vim
typo bim vim
typo cim vim
typo fim vim
typo vm vim
typo im vim

typo wimw vimw

typo it git
typo gi git
typo gie git
typo gir git
typo gti git
typo fir git
typo igt git
typo vit git
typo bit git
typo dit git
typo did git
typo fit git
typo fig git
typo tit git
typo got git
typo gut git
typo agit git
typo ghit git
typo gith git
typo ghti git
typo gitt git
typo gitr git
typo qgit git
typo jgti git # it's like... sometimes I just mash the keyboard while thinking really hard about the command

typo glap glab

typo ggsheild ggshield # Git Guardian - a work tool

# Not technically typos, but a common misstep:
typo :q "echo You are not in vim"
typo :wq :q
typo wq :q

typo ecoh echo
typo ehco echo

typo explorer. 'explorer .'
typo exploer. explorer. # happened while I was writing the alias above

typo htpo htop
typo hotp htop
typo htp htop

# It's faster to just alias these to cht.sh and let the invocation fail later instead of checking for the existence of cht.sh
typo cht cht.sh
typo ch cht.sh

typo ks ls
typo lks ls
typo dls ls
typo lss ls
typo lsa 'ls -a'
typo lsl 'ls -l'
typo los ls
typo lh llh
typo les less
typo hess less
typo lesss less

typo ach ack
typo avk ack
typo acl ack
typo akc ack

typo skeep sleep

typo path path_to_lines

# mt is actually a real command, but I don't plan on doing stuff with magnetic tape
typo mt mr

typo map man # I'm kinda surprised there was no existing map command that this overrides
typo amn man
typo mabn man
typo nan man

typo sork sort
typo sortr sort

typo shfmy shfmt
typo shf shfmt # tentative, sitting at the tab completion fork with shfolder.dll
typo shft shfmt
typo shmft shfmt
typo shfmty shfmt # speculative

typo crontabl crontab

typo cata cat
typo vat cat
typo at cat
typo ca cat
typo cag cat
typo catg cat
typo catr cat
typo qcat cat

# G is closer to B than C on the keyboard
typo gat bat
typo bathhelp bathelp

# lls is define in jake-aliases. Basically ls | less
typo qls ls # I quit less *twice* then wanted to ls
typo lll lls
typo llls lls
typo llss lls
typo lle lls
typo kkt llt
typo lt llt # Bragging on typos - this *will never* override the `lt` command from apt's looptools
typo lld 'll -d'
typo lles lls
typo lless lls

typo tre tree
typo ree tree
typo tgree tree
typo treee tree

# These are times when I expected tree to have neither the depth nor count limits
typo treea ltree
typo treen ltree
typo trene treen

typo deita delta

typo di diff
typo idf diff
typo dif diff
typo iff diff
typo idff diff
typo duff diff
typo dfif diff
typo didd diff
typo difdf diff
typo dfiff diff
typo difff diff
typo diiff diff

typo renite remote
typo remtoe remote
typo rewmote remote
typo reomote remote

typo bash0t bash-it
typo bash0-t bash-it
typo bashs-it bash-it
# my own tool that does apt updates
typo apt0up apt-up
typo aptup apt-up
typo apu-up apt-up
typo apt-files apt-file

typo note notepad

typo grpe grep

typo pgre pgrep

typo hgrpe hgrep
typo hrpe hgrep

typo ptree pstree

typo gilr file # Left hand moved one key to the right
typo vile file
typo fiel file
typo fild file
typo fil file

typo filw filew   # not file - filewhich!
typo vilew filew  # phonics!

typo fiels files

typo mkae make
typo maek make
typo mane make
typo manek make

typo tiem time

typo mcn mvn
typo vmn mvn

typo mf mv

typo lobs jobs

typo suod sudo
typo suto sudo
typo audo sudo
typo simon sudo
typo simon-says sudo

typo ssg ssh
typo shs ssh

# The vars command is defined in .bash-it/custom, so it is defined *after* this, but it's fine to
# pre-declare aliases beforehand
typo vasr vars
typo cars vars

# convenience/easier to access the name over basename, base32, and basecsp.dll
typo base base64
typo base65 base64

typo pyt python # technically, just a lazy name
typo pyhtron python
typo pytrhon python
typo pyhton python

# because that's what I was trying to type at the time, and I figure if I most-common'd
# 'type asdf' into 'typ easdf', it wouldn't work anyway
typo typ typo
typo ypo typo
typo fypo typo
typo tyop typo
typo yypo typo
typo rypo typo
typo tyypo typo
typo ytypo typo
typo typeo typo
typo typow typo

typo trypos typos

typo tpe type
typo ype type
typo tyep type
typo tyoe type
typo yype type
typo typew type # ... because type already operates on its which (this might bite future me. Sorry, future me)
typo typw type
typo tpye type
typo tytpe type

# Technically builtins, but fine as normal typos
typo hsitory history
typo pws pwd
typo wpd pwd

typo brows browse
typo brose browse
typo brwose browse
typo borwse browse
typo browsed browse # I was thinking browse when I made this typo

typo cowthing cowthink

typo whick which # (to be fair, I was drinking at the time :| )
typo whoch which
typo whic which
typo wich which

typo gind find
typo fin find

typo ipconfig ifconfig

typo rakubew rakubrew
typo rakub rakubrew

typo heml helm
typo kube kubectl
typo kubectyl kubectl
typo eks eksctl

typo mktmp mktemp

typo s3 'aws s3'

typo puj pj
typo pjh pj

# from jake-aliases - these are git command which drop the "git " prefix
typo stage staged # NB: `git stage` is an alias for `git add`. This here is a TYPO of staged, not an attempt to use `git stage` conveniently
typo stsaged staged
typo setaged staged
typo staghed staged
typo stagerd staged
typo stg staged
typo sjow show
typo whow show
typo shwo show
typo sho show
typo shw show
# some of these are handled by a "duplicating alias" too (so alias comm0t='git comm0t' would work) but it's better for
# them to be here than in jake-aliases which would imply that these are legitimate git commands.
# To handle these both with and without git requires duplication. I'd rather have that duplication in here than
# in jake-aliases. These are typo words, not git-command words.
# TODO: I wish there were a way to auto-correct `commit --amened` to `commit --amend`
typo githelp 'git help'
typo ammend amend
typo amdnd amend
typo amned amend
typo ament amend
typo amedn amend
typo amdne amend # jeez.
typo comit commit
typo ommit commit
typo comm9t commit
typo comm0t commit
typo comm-t commit
typo commt commit
typo cmmit commit
typo cimmit commit
typo vimmit commit
typo ocmmit commit
typo commmit commit
typo commi9t commit
typo commitm commit
typo commitmp commit # variants named from git's simplified version of these bash commands
typo commitpm commit
typo committ commit
typo commit-a 'commit -a'
typo commita 'commit -a'
typo rebas rebase
typo rease rebase
typo reabse rebase
typo revase rebase
typo rebvase rebase
typo rebased rebase
typo erstore restore
typo restoer restore
typo retore restore
typo rstore restore
typo restorep restore
typo qr r
typo r-branches rainbow-branches
typo r-b rainbow-branches
typo rb rainbow-branches
typo r-here rainbow-here
typo r-h rainbow-here
typo rh rainbow-here
typo r-all rainbow-all
typo ra rainbow
typo rain rainbow
typo rainow rainbow
typo rainbo rainbow
typo rianbow rainbow
typo ranibow rainbow
typo rainboqw rainbow
typo rainboiw rainbow
typo raninbow rainbow
typo dubmodule submodule
typo submoduel submodule
typo submod submodule
typo setatus status
typo stsatus status
typo sstatus status
typo sttatus status
typo statuat status
typo statsus status
typo stauts status
typo statud status
typo statu status
typo stqat status
typo staut status
typo tatus status
typo staus status
typo stast status
typo cstat stat # allow a level of indrection here - this *might* actually want to be `stat`
typo stst stat  # ditto.
# NB: `stat` is an existing command. I needed a function to turn zero-arg `stat` into status, not just a simple alias
# That's why all-but-one typos go to `status`, because they all intended to be a status command, never a `stat`
typo sta status
typo st status # first unique difference from s's status-or-show magic
typo brach branch
typo branche branches # because sometimes I get lazy, apparently
typo bracnhes branches
typo gst gstatus
typo gstat gstatus
typo staqsh stash
typo stasg stash
typo stas stash      # Ah. So that's what I meant the first time I made this typo
typo tsga tags       # Wow.
typo unstasn unstash # Amusingly, a typo of a command I didn't even have before I made the typo. Now I do
typo pu pull
typo up pull  # Technically not a typo, but it's a typo of a typo, so I'm keeping it here
typo uop pull # Actually a typo of up, which I'm using more as an alias of up, apparently
typo uip pull
typo ujp pull
typo pul pull
typo ull pull
typo upll pull
typo pulll pull
typo oush push
typo puas push
typo spuh push
typo puhs push
typo psuh push
typo upsh push
typo pusl push
typo ppush push
typo pushb push
typo pusbh push
typo pusjh push
typo pushj push
typo push4 push
# typo pushd push  # shadowed by the bash builtin `pushd`
typo psh push
typo pus push
typo puh push
typo ush push
typo push--- push--
typo cone clone
typo cloen clone
typo addd add
typo ass add
typo ad add
typo unadd unstage # Not actually a typo, but a brain-o(?)
typo .og log
typo nog log
typo loig log
typo lig log
typo lob log
typo jogp logp
typo logd logp # apparently log[D]iff makes sense if I forget it's actually [P]atch
typo lgop logp
typo lopg logp
typo ls-fiels ls-files
# Nope. Tied. splits the ticket.
# typo ls-files 'git ls-files' # an implicit-git typo, but hopefully, it gets the autocomplete first before ls-fiels
typo mrege merge
typo mereg merge
typo merege merge
typo mergve merge
typo mereges merges
typo mergetoo mergetool
typo m- merge-
typo rebse rebase
typo rebase- 'rebase -'
typo r- rebase-
typo yesteday yesterday
typo yest yesterday
typo wortree worktree
typo jfd jdf
typo jdkf jdf
typo jmf jmg
typo ws jws

# most likely something like "said [y] to a tool that already had --yes'd". Just succeed
typo y true

typo wiget winget
typo wignet winget
typo wingetg winget

# shortened (typo-like) form of these "please definitely use git, and not bash, man, or mr" commands
typo ghelp githelp
typo gman gitman
typo gpull gitpull
typo gstatus gitstatus
typo gup gitpull

typo jjake jake # j!! on a jake
typo jske jake
typo jkae jake
typo jaek jake
typo vack jack
typo j! jack
typo jakeTree jaketree

typo furl curl

# Because I apparently use this tool less frequently, and calling it by its full name... should have worked
typo sdkman sdk
typo adk sdk

typo mrdir rmdir

typo dockar docker
typo docksr docker
typo docker0run docker-run

typo ru run
typo rin run

# super eager with that second s
typo bashs bash
typo bass bash
typo bas bash
# custom config command to manage dotfiles
typo confgi config
typo cofngi config
typo conifg config
typo cofnig config
typo confg config
typo cofig config
typo onfig config
typo nfig config
typo conf config

typo nns-conifg nns-config
typo nns-confg nns-config

typo edit-confg edit-config

typo sha256 sha256sum
typo sha sha256sum

typo ci co
typo coi co
typo c- 'co -'
typo co- 'co -'

typo waths watch

unalias typo
