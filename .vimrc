" from https://vi.stackexchange.com/questions/4141/how-to-indent-as-spaces-instead-of-tab/4175#4175
" tabstop:          Width of tab character
" softtabstop:      Fine tunes the amount of white space to be added
" shiftwidth        Determines the amount of whitespace to add in normal mode
" expandtab:        When this option is enabled, vi will use spaces instead of tabs
" I choose tabs to be 4 characters long to distinguish them from my two-space
" indent style
set tabstop     =4
set softtabstop =2
set shiftwidth  =2
set expandtab

" visible characters:
" https://vi.stackexchange.com/questions/422/displaying-tabs-as-characters
set list
set listchars=eol:⏎,tab:␉·,trail:␠
"set listchars=eol:¬,tab:▸],trail:␠
"set listchars=eol:·,tab:>],trail:%


" preserve edit position,
" see https://stackoverflow.com/questions/7894330/preserve-last-editing-position-in-vim/7894493#7894493
source $VIMRUNTIME/vimrc_example.vim


" stash temporary files in ~
" https://stackoverflow.com/questions/743150/how-to-prevent-vim-from-creating-and-leaving-temporary-files/61585014#61585014
set undofile
set undolevels=1000         " How many undos
set undoreload=10000        " number of lines to save for undo

set backup                        " enable backups
set swapfile                      " enable swaps
set undodir=$HOME/.vim/tmp/undo     " undo files
set backupdir=$HOME/.vim/tmp/backup " backups
set directory=$HOME/.vim/tmp/swap   " swap files

" Make those folders automatically if they don't already exist.
if !isdirectory(expand(&undodir))
    call mkdir(expand(&undodir), "p")
endif
if !isdirectory(expand(&backupdir))
    call mkdir(expand(&backupdir), "p")
endif
if !isdirectory(expand(&directory))
    call mkdir(expand(&directory), "p")
endif
