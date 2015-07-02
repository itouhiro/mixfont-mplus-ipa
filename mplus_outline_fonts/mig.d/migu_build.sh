#!/bin/sh
# Usage:  sh mig.d/migu_build.sh 2>&1 | tee `date +%Y%m%d-%H%M`.log

if [ ! -f Makefile ] || [ ! -d ucstable.d ] ; then
  echo "Error: please 'cd mplus_outline_fonts'"
  exit
fi

# prepare
cp -pfv mig.d/Makefile .
cp -pfv mig.d/scripts/* scripts/

FULL_ZERO_SVG=svg.d/latin_fullwidth1/uFF10.svg
if [ ! -f ${FULL_ZERO_SVG}.noslash ] ; then
    # backup
    cp -fpv ${FULL_ZERO_SVG} ${FULL_ZERO_SVG}.noslash
fi
# replace glyphs
replace_glyph(){
    for F in `find mig.d/svg.d/ -type f`; do
        if [ "`echo $F|grep /CVS`" ] ; then
            echo > /dev/null
        elif [ "`echo $F|grep '\.ai$'`" ] ; then
            echo > /dev/null
        elif [ "`echo $F|grep /vert/`" ] ; then
            DESTDIR=`echo $F|sed -e 's,mig.d/,,' -e 's,[^/]*$,,'`
            mkdir -pv $DESTDIR
            DEST=`echo $F|sed 's,mig.d/,,'`
            cp -fpv $F $DEST
            touch $DEST
        else
            DEST=`echo $F|sed 's,mig.d/,,'`
            cp -fpv $F $DEST
            touch $DEST
        fi
    done
    find work.d/targets/ -name "*.ttf" -exec rm -fv {} \;
    return 0
}


## build M+ for Migu
replace_glyph
cp -fpv ${FULL_ZERO_SVG}.noslash ${FULL_ZERO_SVG}
touch ${FULL_ZERO_SVG}
MPLUS_FULLSET=yes make SPLIT_CONCURRENCY=2 -j2
for F in `find work.d/targets -name "mplus-*.ttf"| egrep '(1p|2p|2m)'`; do
    mv -v $F work.d/circle-`basename $F`
done


## build M+ for Migu (slashed zero)
replace_glyph
MPLUS_FULLSET=yes make SPLIT_CONCURRENCY=2 -j2
for F in `find work.d/targets -name "mplus-1[cm]*ttf"`; do
    mv -v $F work.d/circle-`basename $F`
done
