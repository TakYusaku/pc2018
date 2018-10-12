#!/bin/sh

if test $1 = "1" ; then
  export http_proxy="http://http-p.srv.cc.suzuka-ct.ac.jp:8080"
  export https_proxy="http://http-p.srv.cc.suzuka-ct.ac.jp:8080"
elif test $1 = "0" ; then
  export http_proxy=""
  export https_proxy=""
fi

echo "http_proxy is ${http_proxy} "
echo "https_proxy is ${https_proxy} "
