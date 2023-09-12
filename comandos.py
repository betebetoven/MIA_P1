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
                                                                  mkfile -path=/home/documents/papers/archivos.txt -r -size=10\
                                                                      mkfile -path=/home/documents/papers/mentos/kk -r \
                                                                          mkfile -path=/home/documents/papers/mentos/kk1 -r \
                                                                              mkfile -path=/home/documents/papers/mentos/kk2 -r \
                                                                                  mkfile -path=/home/documents/papers/mentos/kk3 -r \
                                                                      mkfile -path=/home/documents/papers/mentos/mentos.txt -r -cont=/contenido.txt\
                                                                          mkfile -path=/home2/documents/papers/mentos/mentos2.txt -r -cont=/contenido.txt\
                            remove -path=/home/documents/papers/mentos/mentos.txt\
                                mkfile -path=/home/documents/papers/mentos/mentos.txt -r -cont=/contenido.txt\
                                    mkfile -path=/casa" -r\
                                         mkdir -path=/carro" -r\
                                             rename -path=/carro -name=carrititito\
                                                 edit -path=/home2/documents/papers/mentos/mentos2.txt -cont=/contenido_editado.txt -r\
                                                     mkfile -path=/home2/documents/llena2" -r\
                                                    mkfile -path=/home2/documents/llena3" -r\
                                                        mkfile -path=/home2/documents/llena4" -r\
                                                     copy -path=/home2/documents/papers/mentos/mentos2.txt -destino=/home2/documents\
                        '                               
#unmount -id=533Disco4 \