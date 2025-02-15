from openupgradelib import openupgrade
from psycopg2 import sql


@openupgrade.migrate()
def migrate(env, version):
    drop_sql = sql.SQL("ALTER TABLE {} DROP CONSTRAINT {}")
    table = "stock_delivery_note_account_invoice_rel"
    env.cr.execute(
        """
            SELECT constraint_name
            FROM information_schema.table_constraints
            WHERE constraint_type = 'FOREIGN KEY' AND table_name = %s
            AND constraint_name like %s
        """,
        (table, "%%%s%%" % "invoice_id"),
    )
    for constraint in (row[0] for row in env.cr.fetchall()):
        openupgrade.logged_query(
            env.cr,
            drop_sql.format(
                sql.Identifier(table),
                sql.Identifier(constraint),
            ),
        )
    # update invoice_id ref in table
    query = """
        UPDATE {table}
        SET
            invoice_id = am.id
        FROM account_invoice inv
            JOIN account_move am ON am.id = inv.move_id
        WHERE
            invoice_id = inv.id
    """.format(
        table=table
    )
    openupgrade.logged_query(
        env.cr,
        query,
    )
