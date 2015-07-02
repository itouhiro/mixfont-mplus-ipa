#!/bin/sh
# Usage:  sh mig.d/migu_merge.sh 2>&1 | tee `date +%Y%m%d-%H%M`.log

if [ ! -f release/Makefile ] || [ ! -d ucstable.d ] ; then
  echo "Error: please 'cd mplus_outline_fonts'"
  exit
fi


# prepare
KANJI_REGULAR=mig.d/sfd.d/IPAGothic-regular.sfd
KANJI_BOLD=mig.d/sfd.d/IPAGothic-bold.sfd
if [ -f "$KANJI_REGULAR".xz ] || [ -f "$KANJI_BOLD".xz ] ; then
  xz -dv mig.d/sfd.d/*.xz
fi
cp -pfv mig.d/scripts/* scripts/


## build Migu
fontforge -script scripts/migu.py 1P regular
fontforge -script scripts/migu.py 1P bold

fontforge -script scripts/migu.py 2M regular
fontforge -script scripts/migu.py 2M bold

fontforge -script scripts/migu.py 2DS regular
fontforge -script scripts/migu.py 2DS bold


## build Migu (slashed fullwidth zero)
fontforge -script scripts/migu.py 1M regular
fontforge -script scripts/migu.py 1M bold

fontforge -script scripts/migu.py 1C regular
fontforge -script scripts/migu.py 1C bold

fontforge -script scripts/migu.py 1VS regular
fontforge -script scripts/migu.py 1VS bold

fontforge -script scripts/migu.py 1BT regular
fontforge -script scripts/migu.py 1BT bold
