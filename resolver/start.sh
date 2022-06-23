sudo apt install -y wget

test -f ipfs-cli || wget -N https://github.com/ZachisGit/p2p/releases/download/latest/ipfs-cli

sudo chmod +x ipfs-cli

./ipfs-cli & python3 main.py


