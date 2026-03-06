#!/bin/bash 

rm -rfv ./*1* ./*2* ./*3* ./*4* ./*5* ./*6* ./*7* ./*8* ./*9* ./*0*
bash file.sh && git stage ./* && git commit -m "_: Sync time testing" && git push
