FROM ubuntu:22.04

RUN apt-get update && apt-get upgrade -y
RUN dpkg --add-architecture i386 && apt-get update && apt-get install -y wget unzip

# RUN wget https://github.com/PowerShell/PowerShell/releases/download/v7.3.5/PowerShell-7.3.5-win-x86.zip
# RUN wineboot
# RUN unzip PowerShell-7.3.5-win-x86.zip -d /powershell
# RUN wine cmd /c "powershell\pwsh.exe --version" && exit 1
# RUN wine "Z:/powershell/pwsh.exe" --version

RUN mkdir -pm755 /etc/apt/keyrings
RUN wget -O /etc/apt/keyrings/winehq-archive.key https://dl.winehq.org/wine-builds/winehq.key
RUN wget -NP /etc/apt/sources.list.d/ https://dl.winehq.org/wine-builds/ubuntu/dists/jammy/winehq-jammy.sources
RUN apt-get update && apt-get install -y --install-recommends winehq-staging

RUN wget https://github.com/PietJankbal/powershell-wrapper-for-wine/raw/master/install_pwshwrapper.exe
RUN wine install_pwshwrapper.exe
RUN wine powershell -noni -c 'echo "done"'
RUN wine powershell -noni -c 'echo "done"' && exit 1