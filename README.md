

I'm working on managing my own dotfiles.

Exploring from https://news.ycombinator.com/item?id=11070797, we find:

# vcsh + myrepos
https://srijanshetty.in/technical/vcsh-mr-dotfiles-nirvana/, which is referencing old commits:
https://github.com/srijanshetty/cli-goodies/commit/2dbe7fc2f7e0b4c0ca3e574a8960d535fefaaefb
and old articles: https://web.archive.org/web/20141225183659/http://www.martin-burger.net/blog/unix-shell/manage-dotfiles-quickly-and-effortlessly/.

There are several repositories of independent dotfiles. Lets you pick and choose.
Uses git working dir for each of vcsh's managed repos. myrepos is just for multi pull/push actions
https://github.com/RichiH/vcsh
https://github.com/RichiH/myrepos

NB: vcsh is persnickety. I'd like to look into alternatives. https://github.com/capr/multigit seems similar enough?

# rcm
rc manager - uses symlinks
https://thoughtbot.com/blog/rcm-for-rc-files-in-dotfiles-repos

# manual vcsh
The atlassian blog post in my bash-it repo at https://github.com/jakebman/bash-it/blob/custom-jake/plugins/available/dotfiles-via-bare-git-repo-with-config-alias.plugin.bash
https://www.atlassian.com/git/tutorials/dotfiles

# multigit
An alternative to vcsh is to have layered git repos in ~, with https://github.com/capr/multigit

# GNU Stow
A tool for symlinking. Potentially could allow dotfiles repos to be fully independently VCS'd, per https://brandon.invergo.net/news/2012-05-26-using-gnu-stow-to-manage-your-dotfiles.html
https://www.gnu.org/software/stow/
