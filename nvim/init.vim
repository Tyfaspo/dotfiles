call plug#begin()

Plug 'tpope/vim-commentary'
Plug 'raimondi/delimitmate'
Plug 'dense-analysis/ale'
Plug 'morhetz/gruvbox'
Plug 'preservim/nerdtree'
Plug 'norcalli/nvim-colorizer.lua'
Plug 'neoclide/coc.nvim', {'branch': 'release'}

call plug#end()

inoremap <silent><expr> <F1>
      \ pumvisible() ? "\<C-n>" :
      \ <SID>check_back_space() ? "\<F1>" :
      \ coc#refresh()
inoremap <expr><S-F1> pumvisible() ? "\<C-p>" : "\<C-h>"
 
function! s:check_back_space() abort
  let col = col('.') - 1
  return !col || getline('.')[col - 1]  =~# '\s'
endfunction
 
" Make <CR> to accept selected completion item or notify coc.nvim to format
" <C-g>u breaks current undo, please make your own choice.
inoremap <silent><expr> <CR> coc#pum#visible() ? coc#pum#confirm()
                              \: "\<C-g>u\<CR>\<c-r>=coc#on_enter()\<CR>"


set termguicolors
lua require'colorizer'.setup()

autocmd vimenter * ++nested colorscheme gruvbox
autocmd vimenter * set bg=dark
set autoindent
set tabstop=2
set shiftwidth=2
syntax on
set relativenumber
