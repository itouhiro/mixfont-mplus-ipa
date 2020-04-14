#!/bin/sh
# Usage:  sh mig.d/clamp.sh 2>&1 | tee `date +%Y%m%d-%H%M`.log

if [ ! -f release/Makefile ] || [ ! -d ucstable.d ] ; then
  echo "Error: please 'cd mplus_outline_fonts'"
  exit
fi
if [ ! -f work.d/circle-mplus-1p-regular.ttf ] ; then
  echo "Error: please build circle-mplus*ttf"
  exit
fi

# prepare
cp -pfv mig.d/scripts/* scripts/

## build
for middlefamily in 1p 1c 1m 1mn 2p 2m ; do
  fontforge -script scripts/clamp.py ${middlefamily} thin    w1 regular
  fontforge -script scripts/clamp.py ${middlefamily} regular w1 bold

  fontforge -script scripts/clamp.py ${middlefamily} light   w3 regular
  fontforge -script scripts/clamp.py ${middlefamily} medium  w3 bold

  fontforge -script scripts/clamp.py ${middlefamily} regular w4 regular
  fontforge -script scripts/clamp.py ${middlefamily} bold    w4 bold
done

for middlefamily in 1p 1c 2p ; do
  fontforge -script scripts/clamp.py ${middlefamily} medium  w5 regular
  fontforge -script scripts/clamp.py ${middlefamily} heavy   w5 bold

  fontforge -script scripts/clamp.py ${middlefamily} bold    w7 regular
  fontforge -script scripts/clamp.py ${middlefamily} black   w7 bold
done
