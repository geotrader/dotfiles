"dein Scripts-----------------------------

if !&compatible
  set nocompatible
endif

" reset augroup
augroup MyAutoCmd
  autocmd!
augroup END

" dein settings {{{ dein自体の自動インストール
let s:cache_home = empty($XDG_CACHE_HOME) ? expand('~/.cache') : $XDG_CACHE_HOME
let s:dein_dir = s:cache_home . '/dein'
let s:dein_repo_dir = s:dein_dir . '/repos/github.com/Shougo/dein.vim'
if !isdirectory(s:dein_repo_dir)
  call system('git clone https://github.com/Shougo/dein.vim ' . shellescape(s:dein_repo_dir))
endif
let &runtimepath = s:dein_repo_dir .",". &runtimepath
" プラグイン読み込み＆キャッシュ作成
let s:toml_file = fnamemodify(expand('<sfile>'), ':h').'/dein.toml'
if dein#load_state(s:dein_dir)
  call dein#begin(s:dein_dir)
  call dein#load_toml(s:toml_file)
  call dein#end()
  call dein#save_state()
endif
" 不足プラグインの自動インストール
if has('vim_starting') && dein#check_install()
  call dein#install()
endif
" }}}

"End dein Scripts-------------------------


" deoplete設定
let g:deoplete#enable_at_startup = 1

" vim
syntax on
set number
set cursorline
set cursorcolumn
set whichwrap=b,s,[,],<,>
set autoindent
set clipboard=unnamedplus
set expandtab
set incsearch
set list
set smartindent
set tabstop=4
set ignorecase

filetype plugin on

" set filetypes
augroup mySytanx
  autocmd!
  autocmd BufRead,BufNewFile .vimperatorrc setf vim
  autocmd BufRead,BufNewFile .vifmrc setf vim
  autocmd BufRead,BufNewFile .py setfiletype python
  autocmd BufRead,BufNewFile .hs setfiletype haskell
augroup END


"map
nnoremap U <C-r>
