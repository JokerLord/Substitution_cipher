# Substitution_cipher
___
## Программа реализует шифр подстановки (в качестве ключа используется подстановка из символов) c несколькими режимами:
### Генерация ключа. Запуск:
    main.py genkey -o sec.key
### Шифрование. Запуск:
    main.py enc -k sec.key input.txt -o input.txt.enc
### Расшифрование (с ключом). Запуск:
    main.py dec -k sec.key input.txt.enc -o output1.txt
### Создание модели (возвращает массив из частот встречаемости каждого байта на основании большого кол-ва текствов). Запуск:
    main.py makemodel [file1.txt, file2.txt, ...] -o model.txt
### Дешифрование (без ключа) (возвращает ключ). Запуск:
    main.py broke model.txt input.txt -o sec1.key
