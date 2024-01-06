#!/bin/sh 
docPath="content/posts/"
newDocPath=$1
path=${docPath}${newDocPath}

echo ${path}
hugo new ${path}