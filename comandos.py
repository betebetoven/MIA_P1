comandos = 'mkdisk -size=10 -path="/home/mis discos/Disco4.dsk" -unit=M -fit=BF \n\
    fdisk -size=300 -path="/home/mis discos/Disco4.dsk" -name=laprimera \
        fdisk -size=10 -type=E -unit=K -path="/home/mis discos/Disco4.dsk" -name=lasegunda -fit=BF \
            fdisk -size=10 -type=E -unit=K -path="/home/mis discos/Disco4.dsk" -name=latercera -fit=BF \
                fdisk -size=10 -type=E -unit=K -path="/home/mis discos/Disco4.dsk" -name=lacuarta -fit=BF \
                    fdisk -size=10 -type=E -unit=K -path="/home/mis discos/Disco4.dsk" -name=laquinta -fit=BF \
'