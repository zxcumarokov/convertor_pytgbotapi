INSERT INTO directions (id, phrase_code, name)
VALUES
    (1, 'ru_en_direction', 'ru-en'),
    (2, 'en_ru_direction', 'en-ru')
ON CONFLICT (id) DO UPDATE
    SET phrase_code = excluded.phrase_code,
        name = excluded.name;
SELECT setval('directions_id_seq', (SELECT MAX(id) FROM directions));