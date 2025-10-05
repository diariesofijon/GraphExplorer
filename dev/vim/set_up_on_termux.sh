#!/bin/bash

# Installation Steps (for Termux or Debian)
# Required Packages (for Termux / Debian / Linux / macOS)
# Python linters and type checkers
pkg install vim git curl python nodejs -y
# On Termux/Debian
pip install pylint pyright black autopep8 isort pytest
curl -fLo ~/.vim/autoload/plug.vim --create-dirs \
  https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
vim +PlugInstall +qall


# SetUp Vim/Neovim

vim +PlugInstall +qall
