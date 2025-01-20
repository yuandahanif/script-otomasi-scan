# script-otomasi-scan

## git submodule

```sh
git clone --recurse-submodules --shallow-submodules --depth 1 https://github.com/yuandahanif/script-otomasi-scan
```

```sh
git submodule update --init
```

## [loxs](https://github.com/coffinxp/loxs)

```sh
python3 -m venv .venv

source .venv/bin/activate

pip install -r submodules/loxs/requirements.txt
```

## [katana](https://github.com/projectdiscovery/katana)

```sh
CGO_ENABLED=1 go install github.com/projectdiscovery/katana/cmd/katana@latest
```

```sh
export PATH=$PATH:$(go env GOPATH)/bin
```
