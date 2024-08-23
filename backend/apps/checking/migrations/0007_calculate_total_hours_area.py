# Generated by Django 5.0.6 on 2024-08-23 00:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checking', '0006_get_checking_reports_area_range'),
    ]

    operations = [
        migrations.RunSQL(
            """
            CREATE OR REPLACE FUNCTION calculate_total_hours_area(
                area_id_param INTEGER,
                start_date TIMESTAMPTZ,
                end_date TIMESTAMPTZ
            )
            RETURNS INTERVAL AS $$
            DECLARE
                total_hours INTERVAL := '0 hours';
            BEGIN
                SELECT 
                    SUM(chk.check_out - chk.check_in) 
                INTO total_hours
                FROM checking_check chk
                JOIN register_person rp ON chk.person_id = rp.id
                JOIN register_area ra ON rp.area_id = ra.id
                WHERE 
                    ra.id = area_id_param
                    AND chk.check_in >= start_date
                    AND chk.check_out <= end_date
                    AND chk.check_out IS NOT NULL;

                RETURN total_hours;
            END;
            $$ LANGUAGE plpgsql;
            """,
            reverse_sql="""
            DROP FUNCTION IF EXISTS calculate_total_hours_area();
            """
        ),
    ]
