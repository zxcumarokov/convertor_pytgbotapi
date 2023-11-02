INSERT INTO "public"."phrases" ("language_id", "phrase_code", "text") VALUES
    (1, 'RUB_TO_USD', 'рубли в доллары'),
    (2, 'RUB_TO_USD', 'rubles to dollars'),
    (1, 'USD_TO_RUB', 'доллары в рубли'),
    (2, 'USD_TO_RUB', 'dollars to rubles'),
    (1, 'SELECT_LANGUAGE', 'язык успешно выбран'),
    (2, 'SELECT_LANGUAGE', 'language successfully selected'),
    (1, 'CHOOSE_DIRECTION', 'выберете направление перевода'), -- Добавьте кавычку здесь
    (2, 'CHOOSE_DIRECTION', 'select the direction of transfer'),
    (1,'ENTER_AMOUNT','Введите сумму для конвертации'),
    (2,'ENTER_AMOUNT','Enter the amount to convert');

ON CONFLICT ("phrase_code", "language_id") DO UPDATE
SET "text" = excluded."text";
