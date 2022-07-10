" from https://vi.stackexchange.com/questions/4141/how-to-indent-as-spaces-instead-of-tab/4175#4175
" tabstop:          Width of tab character
" softtabstop:      Fine tunes the amount of white space to be added
" shiftwidth        Determines the amount of whitespace to add in normal mode
" expandtab:        When this option is enabled, vi will use spaces instead of tabs
set tabstop     =2
set softtabstop =2
set shiftwidth  =2
set expandtab

" preserve edit position, per https://stackoverflow.com/questions/7894330/preserve-last-editing-position-in-vim/7894493#7894493
source $VIMRUNTIME/vimrc_example.vim
