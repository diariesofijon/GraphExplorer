" ========================================================
"   🧩  Plugin Manager — vim-plug
" ========================================================
" Install if missing:
"   curl -fLo ~/.vim/autoload/plug.vim --create-dirs \
"       https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim

call plug#begin('~/.vim/plugged')

" Linting, Type Checking, Fixing
Plug 'dense-analysis/ale'

" Trailing whitespace highlight and cleanup
Plug 'ntpeters/vim-better-whitespace'

" EditorConfig for consistent formatting (EOF newline, tabs, etc.)
Plug 'editorconfig/editorconfig-vim'

call plug#end()


" ========================================================
"   ⚙️  Core Editor Settings
" ========================================================
set nocompatible
syntax on
filetype plugin indent on
set encoding=utf-8
set number
set ruler
set expandtab
set shiftwidth=4
set softtabstop=4
set fileformats=unix,dos,mac
set autoread
set hidden


" ========================================================
"   🧹  Whitespace and Newline Behavior
" ========================================================
let g:better_whitespace_enabled = 1
let g:strip_whitespace_on_save  = 1

" Ensure exactly one newline at EOF
autocmd BufWritePre * call s:EnsureSingleTrailingNewline()

function! s:EnsureSingleTrailingNewline()
  silent! %s/\($\n\s*\)\+\%$//e
  silent! call append(line('$'), '')
endfunction


" ========================================================
"   🧪  ALE: Python Linting, Type Checking, Formatting
" ========================================================
let g:ale_linters = {
\   'python': ['pylint', 'pyright']
\}

let g:ale_fixers = {
\   'python': ['black', 'isort', 'autopep8']
\}

let g:ale_lint_on_save = 1
let g:ale_fix_on_save  = 1
let g:ale_lint_on_text_changed = 'never'

" Highlight errors inline
let g:ale_set_highlights = 1
let g:ale_echo_cursor = 1


" ========================================================
"   🧭  Pylint & Pyright Executable Paths (Cross-Platform)
" ========================================================
if has('win32') || has('win64')
  let g:ale_python_pylint_executable = 'C:\\Program Files\\Python312\\Scripts\\pylint.exe'
  if !filereadable(g:ale_python_pylint_executable)
    let g:ale_python_pylint_executable = 'C:\\Users\\' . $USERNAME . '\\AppData\\Local\\Programs\\Python\\Python312\\Scripts\\pylint.exe'
  endif
  let g:ale_python_pyright_executable = 'C:\\Users\\' . $USERNAME . '\\AppData\\Roaming\\npm\\pyright.cmd'
elseif has('unix')
  for p in ['/usr/local/bin', '/usr/bin', expand('~/.local/bin')]
    if filereadable(p . '/pylint')
      let g:ale_python_pylint_executable = p . '/pylint'
    endif
    if filereadable(p . '/pyright')
      let g:ale_python_pyright_executable = p . '/pyright'
    endif
  endfor
endif


" ========================================================
"   ⚙️  Optional: Run Tests via ALE + pytest
" ========================================================
" Custom command to run pytest and show results in a split window
command! Pytest call s:RunPytest()

function! s:RunPytest()
  if executable('pytest')
    botright 10split | terminal pytest -q --color=yes
  else
    echo "pytest not found. Install with: pip install pytest"
  endif
endfunction

" Optional: auto-run pytest on save (toggleable)
let g:auto_pytest_on_save = 0

autocmd BufWritePost *.py if g:auto_pytest_on_save | call s:RunPytest() | endif


" ========================================================
"   🎨  Highlight Trailing Spaces
" ========================================================
highlight ExtraWhitespace ctermbg=red guibg=red
autocmd BufWinEnter * match ExtraWhitespace /\s\+$/
autocmd InsertEnter * match ExtraWhitespace /\s\+\%#\@<!$/
autocmd InsertLeave * match ExtraWhitespace /\s\+$/
autocmd BufWinLeave * call clearmatches()


" ========================================================
"   💡  Helper Shortcuts
" ========================================================
" Quickly toggle pytest autorun
nnoremap <leader>tp :let g:auto_pytest_on_save = !g:auto_pytest_on_save \| echo "Auto Pytest:" g:auto_pytest_on_save<CR>

" Manually lint
nnoremap <leader>l :ALELint<CR>

" Manually fix
nnoremap <leader>f :ALEFix<CR>

" Run pytest manually
nnoremap <leader>p :Pytest<CR>


" ========================================================
"   ✅  Ready
" ========================================================
echo "✔ Vim ready: lint + type-check + autoformat + test + clean whitespace"
