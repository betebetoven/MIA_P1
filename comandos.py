comandos = '\
mkdisk -size=10 -path="/home/mis discos/Disco4.dsk" -unit=M -fit=WF \n\
    fdisk -size=150 -path="/home/mis discos/Disco4.dsk" -name=laprimera -type=P\
        fdisk -size=100 -type=E -unit=K -path="/home/mis discos/Disco4.dsk" -name=lasegunda -fit=BF \
            fdisk -size=10 -type=P -unit=K -path="/home/mis discos/Disco4.dsk" -name=latercera -fit=WF \
                fdisk -size=300 -type=P -unit=K -path="/home/mis discos/Disco4.dsk" -name=lacuarta -fit=FF \
                    fdisk -size=10 -type=P -unit=K -path="/home/mis discos/Disco4.dsk" -name=laquinta -fit=BF \
                        fdisk -name=lasegunda -delete=full -path="/home/mis discos/Disco4.dsk" \
                            fdisk -name=lacuarta -delete=full -path="/home/mis discos/Disco4.dsk" \
                            fdisk -size=90 -path="/home/mis discos/Disco4.dsk" -name=laacomodada -fit=WF \
                                fdisk -add=100 -unit=K -path="/home/mis discos/Disco4.dsk" -name=laprimera\
                                    fdisk -size=1 -type=P -unit=K -path="/home/mis discos/Disco4.dsk" -name=laquenoentra -fit=FF \
                                        fdisk -size=1 -type=L -unit=K -path="/home/mis discos/Disco4.dsk" -name=acaandamos -fit=FF \
                                            fdisk -size=1 -type=L -unit=K -path="/home/mis discos/Disco4.dsk" -name=acanosfuimos -fit=FF \
                                                fdisk -size=1 -type=L -unit=K -path="/home/mis discos/Disco4.dsk" -name=acanosreimos -fit=FF \
                                        mount -path="/home/mis discos/Disco4.dsk" -name=laprimera \
                                              mkfs -type=full -id=531Disco4\
                                                  logout\
                                                  login -user=root -pass=123 -id=531Disco4\
                                                      mkusr -user=user1 -pass=usuario -grp=root\
                                                          mkusr -user=user2 -pass=usuario -grp=root\
                                                              mkusr -user=user3 -pass=usuario -grp=root\
                                                                  mkusr -user=user4 -pass=usuario -grp=root\
                                                                      mkusr -user=user5 -pass=usuario -grp=root\
                                                                          mkgrp -name=usuarios\
                                                                          mkusr -user=user6 -pass=usuario -grp=root\
                                                                              mkusr -user=user7 -pass=usuario -grp=root\
                                                                                  mkusr -user=user6 -pass=usuario -grp=root\
                                                                                      mkusr -user=user8 -pass=usuario -grp=root\
                                                                                          mkusr -user=user9 -pass=usuario -grp=root\
                                                                                              mkusr -user=user10 -pass=usuario -grp=root\
                                                                                                 mkgrp -name=usuarios2 \
                                                                                                     mkgrp -name=usuarios3 \
                                                                                                         mkgrp -name=usuarios4 \
                                                                                                             mkgrp -name=usuarios4 \
                                                                                                                 mkusr -user=mamadas -pass=usuario -grp=usuarios4\
                                                      rmgrp -name=usuarios\
                                                          rmusr -user=user1\
                                                              mkfile -path=/users.txt\
                                                                  mkfile -path=/home.txt/users.txt\
                                                                      mkfile -path=/home2\
                                                                          mkfile -path=/home3\
                                                                              mkfile -path=/home4.txt\
                                                                                  mkfile -path=/home5\
                                                                                      mkfile -path=/home5/ejemplo.txt\
                                                                                          mkfile -path=/home5/ejemplo2\
                                                                                              mkfile -path=/home5/ejemplo3.txt\
                                                                                                  mkfile -path=/home5/ejemplo4.txt\
                                                                                                      mkfile -path=/home5/ejemplo5.txt\
'
#unmount -id=533Disco4 \