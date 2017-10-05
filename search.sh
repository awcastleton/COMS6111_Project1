#!/bin/bash

# abstracted entry-point for search.py

if [ $# -eq 2 ]
    then
        /usr/bin/python ./search.py AIzaSyCATX_cG2DgsJjFtCdgcThfR2xaH7MSMl0 010829534362544137563:ndji7c0ivva $1 "$2"
fi

if [$# -eq 3 ]
    then
        /usr/bin/python ./search.py AIzaSyCATX_cG2DgsJjFtCdgcThfR2xaH7MSMl0 010829534362544137563:ndji7c0ivva $1 "$2" "$3"
fi
