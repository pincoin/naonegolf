# dev on mac

## pyenv
### homebrew 설치
```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

### pyenv, pyenv-virtualenv 패키지 설치
```
$ brew update
$ brew install pyenv
$ brew install pyenv-virtualenv
```

### ~/.zshrc
```
export LC_ALL=en_US.UTF-8

export CFLAGS="$CFLAGS -I$(brew --prefix openssl)/include"
export LDFLAGS="$LDFLAGS -L$(brew --prefix openssl)/lib"

eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

### 파이썬 컴파일 설치
```
pyenv install -l
pyenv install 3.7.5
```

### 가상환경 생성
```
pyenv virtualenv -p python3.7 3.7.5 naonegolf
```

### pip 업그레이드
```
pip install --upgrade pip
```

## Django 및 패키지 설치
```
pip install django
```
