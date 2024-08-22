# Generated by Django 5.0.6 on 2024-08-22 17:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checking', '0004_calculate_hours'),
    ]

    operations = [
        migrations.RunSQL(
            """
            CREATE OR REPLACE FUNCTION get_checking_reports_range(
                person_id_param INTEGER,
                start_date TIMESTAMPTZ,
                end_date TIMESTAMPTZ
            )
            RETURNS TABLE(
                uuid UUID,
                person_id BIGINT,
                check_in TIMESTAMPTZ,
                check_out TIMESTAMPTZ,
                reason INTEGER,
                created TIMESTAMPTZ,
                modified TIMESTAMPTZ
            ) AS $$
            BEGIN
                RETURN QUERY
                SELECT 
                    chk.uuid,
                    chk.person_id,
                    chk.check_in,
                    chk.check_out,
                    chk.reason,
                    chk.created,
                    chk.modified
                FROM checking_check chk
                WHERE 
                    chk.person_id = person_id_param
                    AND chk.check_in >= start_date
                    AND chk.check_out <= end_date;
            END;
            $$ LANGUAGE plpgsql;
            """,
            reverse_sql="""
            DROP FUNCTION IF EXISTS get_checking_reports_range();
            """
        ),
    ]