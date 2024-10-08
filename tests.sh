#! /usr/bin/bash
if [[ -x ./get.py ]]; then
    chmod +x ./get.py
fi

echo "BEGIN ----------------- Teste 1 -----------------"
./get.py rtx 5000
echo "ESPERADO ----------------- Teste 1 -----------------"
echo "É esperado que sejam retornado no máximo 10 noticias"
echo -e "END ----------------- Teste 1 -----------------\n"

echo "BEGIN ----------------- Teste 2 -----------------"
./get.py rtx 5000 -pc 20
echo "ESPERADO ----------------- Teste 2 -----------------"
echo "É esperado que sejam retornado no máximo 20 noticias"
echo -e "END ----------------- Teste 2 -----------------\n"

echo "BEGIN ----------------- Teste 3 -----------------"
./get.py rtx 5000 -pc 20 -ps 5
echo "ESPERADO ----------------- Teste 3 -----------------"
echo "É esperado que sejam retornado no máximo 15 noticias, começando da noticia 5"
echo -e "END ----------------- Teste 3 -----------------\n"

echo "BEGIN ----------------- Teste 4 -----------------"
./get.py -t d2 -pc 5 rtx 5000
echo "ESPERADO ----------------- Teste 4 -----------------"
echo "É esperado que sejam retornado no máximo 5 noticias, que não sejam mais antigas que 2 dias"
echo -e "END ----------------- Teste 4 -----------------\n"

echo "BEGIN ----------------- Teste 5 -----------------"
./get.py -t y2 -pc 5 rtx 5000
echo "ESPERADO ----------------- Teste 5 -----------------"
echo "É esperado que sejam retornado no máximo 5 noticias, que não sejam mais antigas que 2 anos"
echo -e "END ----------------- Teste 5 -----------------\n"

echo "BEGIN ----------------- Teste 6 -----------------"
./get.py --from 2010 --to 2010 -pc 5 rtx nvidia
echo "ESPERADO ----------------- Teste 6 -----------------"
echo "É esperado que sejam retornado no máximo 5 noticias, que sejam do ano 2010"
echo -e "END ----------------- Teste 6 -----------------\n"
