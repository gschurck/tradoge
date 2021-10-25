    find /c "testnet" tradoge.py >NUL
    if %errorlevel% equ 1 goto notfound
        echo found
    goto done
    :notfound
        echo notfound
    goto done
    :done