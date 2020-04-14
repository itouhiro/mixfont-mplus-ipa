#!/bin/sh

if [ ! -f release/Makefile ] || [ ! -d ucstable.d ] ; then
    echo "Error: please 'cd mplus_outline_fonts'"
    exit
fi

MPLUS_VER=`head -1 release/Makefile | sed 's,^.*= *,,'`
MPLUS_DIR=mplus-TESTFLIGHT-${MPLUS_VER}
IPA_DIR=`ls mig.d/sfd.d/Read* | sed 's,^[^_]*_\([^\.]*\)\..*$,\1,'`

TODAY=`date +%Y%m%d`

## MigMix and Migu zip
for SORT in migmix migu ; do
    for GROUP in 1p 2p 1m 2m 1c; do
        if [ -f "${SORT}-${GROUP}-regular.ttf" ] ; then
            MIG_DIR=${SORT}-${GROUP}-${TODAY}
            mkdir -pv ${MIG_DIR}/${MPLUS_DIR}
            cp -pv release/README_* ${MIG_DIR}/${MPLUS_DIR}/
            mkdir -pv ${MIG_DIR}/${IPA_DIR}
            cp -pv mig.d/sfd.d/*.txt ${MIG_DIR}/${IPA_DIR}/
            cp -pv mig.d/release/${SORT}-R*.txt ${MIG_DIR}/

            mv -v ${SORT}-${GROUP}*.ttf ${MIG_DIR}/
            zip -9rv ${MIG_DIR}.zip ${MIG_DIR}/
        fi
    done
done

## Circle M+ zip
for SORTGROUP in mplus-1mn mplus-1p mplus-2p mplus-1m mplus-2m mplus-1c ; do
    if [ -f "work.d/circle-${SORTGROUP}-regular.ttf" ] ; then
        MIG_DIR=`echo circle-${SORTGROUP}-${TODAY}`
        mkdir -pv ${MIG_DIR}/${MPLUS_DIR}
        cp -pv release/*_* ${MIG_DIR}/${MPLUS_DIR}/
        cp -pv mig.d/release/circle-mplus-README.txt ${MIG_DIR}/

        for F in work.d/circle-${SORTGROUP}*.ttf ; do
            mv -v $F ${MIG_DIR}/
        done
        zip -9rv ${MIG_DIR}.zip ${MIG_DIR}/
    fi
done

## Clamp zip
for SORTGROUP in 1mn 1p 2p 1m 2m 1c ; do
    if [ -f "work.d/clamp-${SORTGROUP}-w1-regular.ttf" ] ; then
        MIG_DIR=`echo clamp-${SORTGROUP}-${TODAY}`
        mkdir -pv ${MIG_DIR}/${MPLUS_DIR}
        cp -pv release/*_* ${MIG_DIR}/${MPLUS_DIR}/
        cp -pv mig.d/release/clamp-README.txt ${MIG_DIR}/

        for F in work.d/clamp-${SORTGROUP}*.ttf ; do
            mv -v $F ${MIG_DIR}/
        done
        zip -9rv ${MIG_DIR}.zip ${MIG_DIR}/
    fi
done

SORT=migu
for GROUP in 1vs 1bt 2ds; do
    if [ -f "${SORT}-${GROUP}-regular.ttf" ] ; then
        MIG_DIR=${SORT}-${GROUP}-${TODAY}
        mkdir -pv ${MIG_DIR}/${MPLUS_DIR}
        cp -pv release/*_* ${MIG_DIR}/${MPLUS_DIR}/
        mkdir -pv ${MIG_DIR}/${IPA_DIR}
        cp -pv mig.d/sfd.d/*.txt ${MIG_DIR}/${IPA_DIR}/
        if [ "$GROUP" = "1vs" ] ; then
            VER=`grep 'DejaVuSans' mig.d/sfd.d/version|head -1|sed 's,^.*: Ver[^ ]* ,,'|sed 's, ,_,g'`
            DOC_DIR=dejavu-fonts-${VER}
            mkdir -pv ${MIG_DIR}/${DOC_DIR}
            cp -pv mig.d/sfd.d/DejaVuSans-LICENSE ${MIG_DIR}/${DOC_DIR}/LICENSE
        elif [ "$GROUP" = "1bt" ] ; then
            VER=`grep 'Bitr' mig.d/sfd.d/version|head -1|sed 's,^.*: Ver[^ ]* ,,'|sed 's, ,_,g'`
            DOC_DIR=Bitter_${VER}
            mkdir -pv ${MIG_DIR}/${DOC_DIR}
            cp -pv mig.d/sfd.d/Bitter-LICENSE ${MIG_DIR}/${DOC_DIR}/OFL.txt
        elif [ "$GROUP" = "2ds" ] ; then
            VER=`grep 'DroidSans' mig.d/sfd.d/version|head -1|sed 's,^.*: Ver[^ ]* ,,'|sed 's, ,_,g'`
            DOC_DIR=Droid_Sans_${VER}
            mkdir -pv ${MIG_DIR}/${DOC_DIR}
            cp -pv mig.d/sfd.d/DroidSans-LICENSE ${MIG_DIR}/${DOC_DIR}/LICENSE.txt
        fi
        cp -pv mig.d/release/${SORT}-${GROUP}*.txt ${MIG_DIR}/
        mv -v ${SORT}-${GROUP}*.ttf ${MIG_DIR}/
        zip -9rv ${MIG_DIR}.zip ${MIG_DIR}/
    fi
done
