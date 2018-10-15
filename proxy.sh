#!/bin/sh

if test $1 = "1" ; then
  git config --global http.proxy wpad.ca.suzuka-ct.ac.jp:8080
  git config --global https.proxy wpad.ca.suzuka-ct.ac.jp:8080
elif test $1 = "0" ; then
  git config --global --unset http.proxy
  git config --global --unset https.proxy
fi

git config --list | grep proxy
