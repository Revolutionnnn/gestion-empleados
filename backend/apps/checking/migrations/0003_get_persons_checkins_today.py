# Generated by Django 5.0.6 on 2024-08-22 16:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checking', '0002_create_count_people_inside_today_function'),
    ]

    operations = [
        migrations.RunSQL(
            """
            CREATE OR REPLACE FUNCTION get_persons_checkins_today()
            RETURNS TABLE(uuid UUID, person_name VARCHAR, person_document VARCHAR,check_in TIMESTAMPTZ) AS $$
            BEGIN
                RETURN QUERY
                SELECT 
                    chk.uuid,
                    rp.name AS person_name,
                    rp.document AS person_document,
                    chk.check_in
                FROM checking_check chk
                JOIN
                    register_person rp ON chk.person_id = rp.id
                WHERE
                    chk.check_in::date = CURRENT_DATE
                    AND chk.check_out IS NULL;
            END;
            $$ LANGUAGE plpgsql;
            """,
            reverse_sql="""
            DROP FUNCTION IF EXISTS get_persons_checkins_today();
            """
        ),
    ]
