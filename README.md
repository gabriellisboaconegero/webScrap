# Intalação
## Apenas pip
```shell
python3 -m pip install -r requirements.txt
```

## Usando virtual env
```shell
python -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
```

## Usando miniconda
```shell
conda create -n webScrap --file requirements.txt
conda activate webScrap
```

# Uso
```shell
usage: get.py [-h] [--dump-html]

Faz um web scrapping

options:
  -h, --help   show this help message and exit
  --dump-html  Se deve jogar o html da página pega
```


# Links úteis
- https://serpapi.com/blog/google-search-parameters/#:~:text=The%20'oq'%20parameter%20of%20Google,into%20the%20Google%20search%20box.
- https://seoheronews.com/url-google
