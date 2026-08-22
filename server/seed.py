import asyncio

from app.database.connection import database

async def seed():
    await database.connect()

    await database.execute("""
        INSERT INTO concepts (code, title_en, title_hi, description_en, description_hi, difficulty)
        VALUES
        ('grammar.greetings', 'Basic Greetings', 'बुनियादी अभिवादन', 'Learn how to greet in English', 'अंग्रेजी में अभिवादन करना सीखें', 1),
        ('grammar.simple_present', 'Simple Present Tense', 'सामान्य वर्तमान काल', 'Learn simple present tense', 'सामान्य वर्तमान काल सीखें', 1),
        ('grammar.present_continuous', 'Present Continuous', 'वर्तमान निरंतर काल', 'Learn present continuous tense', 'वर्तमान निरंतर काल सीखें', 2),
        ('grammar.past_simple', 'Past Simple Tense', 'सामान्य भूत काल', 'Learn past simple tense', 'सामान्य भूत काल सीखें', 2),
        ('grammar.articles', 'Articles: a, an, the', 'आर्टिकल: a, an, the', 'Learn how to use articles', 'आर्टिकल का उपयोग सीखें', 2),
        ('grammar.questions', 'Question Formation', 'प्रश्न बनाना', 'Learn to form questions', 'प्रश्न बनाना सीखें', 3)
        ON CONFLICT (code) DO NOTHING
    """)
    print("✓ Concepts seeded")

    await database.execute("""
        INSERT INTO lessons (code, title_en, title_hi, level, position)
        VALUES
        ('lesson.01.greetings', 'Basic Greetings', 'बुनियादी अभिवादन', 1, 1),
        ('lesson.02.present_tenses', 'Present Tenses', 'वर्तमान काल', 1, 2),
        ('lesson.03.past_tenses', 'Past Tenses', 'भूत काल', 1, 3),
        ('lesson.04.grammar_basics', 'Grammar Basics', 'व्याकरण की मूल बातें', 2, 4)
        ON CONFLICT (code) DO NOTHING
    """)
    print("✓ Lessons seeded")

    await database.execute("""
        INSERT INTO lesson_concepts (lesson_id, concept_id, position)
        SELECT l.id, c.id, 1
        FROM lessons l, concepts c
        WHERE l.code = 'lesson.01.greetings' AND c.code = 'grammar.greetings'
        ON CONFLICT DO NOTHING
    """)

    await database.execute("""
        INSERT INTO lesson_concepts (lesson_id, concept_id, position)
        SELECT l.id, c.id, pos.position
        FROM lessons l
        JOIN (VALUES
            ('grammar.simple_present', 1),
            ('grammar.present_continuous', 2)
        ) AS pos(code, position) ON true
        JOIN concepts c ON c.code = pos.code
        WHERE l.code = 'lesson.02.present_tenses'
        ON CONFLICT DO NOTHING
    """)

    await database.execute("""
        INSERT INTO lesson_concepts (lesson_id, concept_id, position)
        SELECT l.id, c.id, 1
        FROM lessons l, concepts c
        WHERE l.code = 'lesson.03.past_tenses' AND c.code = 'grammar.past_simple'
        ON CONFLICT DO NOTHING
    """)

    await database.execute("""
        INSERT INTO lesson_concepts (lesson_id, concept_id, position)
        SELECT l.id, c.id, pos.position
        FROM lessons l
        JOIN (VALUES
            ('grammar.articles', 1),
            ('grammar.questions', 2)
        ) AS pos(code, position) ON true
        JOIN concepts c ON c.code = pos.code
        WHERE l.code = 'lesson.04.grammar_basics'
        ON CONFLICT DO NOTHING
    """)
    print("✓ Lesson concepts linked")

    await database.disconnect()
    print("✓ Seeding complete")

asyncio.run(seed())
