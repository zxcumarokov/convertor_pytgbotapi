-- -------------------------------------------------------------
-- TablePlus 5.5.2(512)
--
-- https://tableplus.com/
--
-- Database: telegrambotapiconverter
-- Generation Time: 2023-11-04 19:33:52.4980
-- -------------------------------------------------------------


INSERT INTO "public"."directions" ("id", "name", "phrase_code") VALUES
(1, 'usd-rub', 'USD_TO_RUB'),
(2, 'rub-usd', 'RUB_TO_USD');

ON CONFLICT (id) DO UPDATE
    SET phrase_code = excluded.phrase_code,
        name = excluded.name;
SELECT setval('directions_id_seq', (SELECT MAX(id) FROM directions));