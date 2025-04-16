call plug#begin()


Plug 'tpope/vim-commentary'
Plug 'raimondi/delimitmate'
Plug 'dense-analysis/ale'
Plug 'preservim/nerdtree'
Plug 'norcalli/nvim-colorizer.lua'
Plug 'neoclide/coc.nvim', {'branch': 'release'}
Plug 'heavenshell/vim-jsdoc', {
  \ 'for': ['javascript', 'javascript.jsx','typescript'],
  \ 'do': 'make install'
\}
Plug 'nvim-treesitter/nvim-treesitter', {'do': ':TSUpdate'}
Plug 'ellisonleao/gruvbox.nvim'
Plug 'godlygeek/tabular'
Plug 'sindrets/diffview.nvim'
Plug 'nvim-tree/nvim-tree.lua'
Plug 'nvim-tree/nvim-web-devicons'
Plug 'godlygeek/tabular'

call plug#end()

lua << EOF
require'nvim-treesitter.configs'.setup {
  highlight = {
    enable = true,
    -- Setting this to true will run `:h syntax` and tree-sitter at the same time.
    -- Set this to `true` if you depend on 'syntax' being enabled (like for indentation).
    -- Using this option may slow down your editor, and you may see some duplicate highlights.
    -- Instead of true it can also be a list of languages
    additional_vim_regex_highlighting = false,
  },
}
EOF


" " Configure nvim-tree using an embedded Lua block in init.vim
lua << EOF
require("nvim-tree").setup({
  actions = {
    open_file = {
      quit_on_open = false,  -- keep nvim-tree open after opening a file
    },
  },
  update_focused_file = {
    enable = true,
    update_root = true,
  },
	view = {
    width = 50,           -- Set tree width
    side = "right",        -- Show on left (default)
    number = false,       -- Hide line numbers
    relativenumber = true,
  },
	renderer = {
    highlight_git = true, -- Highlight git changes
    icons = {
      show = {
        git = true,
        folder = true,
        file = true,
        folder_arrow = true,
      },
      glyphs = {
        folder = {
          default = "",
          open = "",
          empty = "",
          empty_open = "",
          symlink = "",
        },
      },
    },
  },
  filters = {
    dotfiles = false, -- Show dotfiles (set true to hide)
    custom = { "__pycache__", ".DS_Store", "node_modules" }, -- Hide specific files/folders
  },
  git = {
    enable = true,
    ignore = false, -- Show .gitignore'd files
  },
  -- Remove open_on_setup since it's no longer supported.
})
EOF

let g:loaded_netrw = 1
let g:loaded_netrwPlugin = 1

lua << EOF
local function open_nvim_tree(data)
  -- buffer is a real file on the disk
  local real_file = vim.fn.filereadable(data.file) == 1
  -- buffer is a [No Name]
  local no_name = data.file == "" and vim.bo[data.buf].buftype == ""
  if not real_file and not no_name then
    return
  end
  -- Open the tree, find the file but don't focus it.
  require("nvim-tree.api").tree.toggle({ focus = false, find_file = true })
end

-- Auto-open nvim-tree on VimEnter for valid files.
vim.api.nvim_create_autocmd("VimEnter", {
  callback = open_nvim_tree
})

-- Close nvim-tree if it's the last window remaining.
vim.api.nvim_create_autocmd("BufEnter", {
  nested = true,
  callback = function()
    if #vim.api.nvim_list_wins() == 1 and vim.bo.filetype == "NvimTree" then
      vim.cmd("quit")
    end
  end,
})
EOF

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


nnoremap \do :DiffviewOpen<CR>
nnoremap \dc :DiffviewClose<CR>
" code that changes surrounding quotes single or double into backticks
lua << EOF
local function replace_surrounding(old, new)
  local line = vim.api.nvim_get_current_line()
  -- Escape special characters properly, especially for backticks
  local escaped_old = vim.pesc(old)
  local escaped_new = new
  local new_line = line:gsub("^" .. escaped_old .. "(.-)" .. escaped_old .. "$", escaped_new .. "%1" .. escaped_new)
  vim.api.nvim_set_current_line(new_line)
end
vim.keymap.set("n", "<leader>'\"", function() replace_surrounding("'", "\"") end, { noremap = true, silent = true })
vim.keymap.set("n", "<leader>'`", function() replace_surrounding("'", "`") end, { noremap = true, silent = true })
vim.keymap.set("n", "<leader>\"'", function() replace_surrounding("\"", "'") end, { noremap = true, silent = true })
vim.keymap.set("n", "<leader>\"`", function() replace_surrounding("\"", "`") end, { noremap = true, silent = true })
EOF

" restart coc
nnoremap <leader>cr :CocRestart<CR>

" right alt to clear highlight
nnoremap <silent> <A-/> :noh<CR>

set termguicolors
lua require'colorizer'.setup()

autocmd vimenter * ++nested colorscheme retrobox
autocmd vimenter * set bg=dark
set autoindent
set tabstop=2
set shiftwidth=2
syntax on
set relativenumber


