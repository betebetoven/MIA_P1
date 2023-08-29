comandos = '\
mkdisk -size=10 -path="/home/mis discos/Disco4.dsk" -unit=M -fit=WF \n\
    fdisk -size=10 -path="/home/mis discos/Disco4.dsk" -name=laprimera -type=P\
        fdisk -size=100 -type=E -unit=K -path="/home/mis discos/Disco4.dsk" -name=lasegunda -fit=BF \
            fdisk -size=10 -type=P -unit=K -path="/home/mis discos/Disco4.dsk" -name=latercera -fit=WF \
                fdisk -size=300 -type=P -unit=K -path="/home/mis discos/Disco4.dsk" -name=lacuarta -fit=FF \
                    fdisk -size=10 -type=P -unit=K -path="/home/mis discos/Disco4.dsk" -name=laquinta -fit=BF \
                        fdisk -name=lasegunda -delete=full -path="/home/mis discos/Disco4.dsk" \
                            fdisk -name=lacuarta -delete=full -path="/home/mis discos/Disco4.dsk" \
                            fdisk -size=90 -path="/home/mis discos/Disco4.dsk" -name=laacomodada -fit=WF \
                                fdisk -add=100 -unit=K -path="/home/mis discos/Disco4.dsk" -name=laprimera\
                                    fdisk -size=1 -type=P -unit=K -path="/home/mis discos/Disco4.dsk" -name=laquenoentra -fit=FF \
                                        mount -path="/home/mis discos/Disco4.dsk" -name=latercera \
                                            unmount -id=533Disco4 \
'