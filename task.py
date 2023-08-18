import sqlite3


class Task:
    def __init__(self, task_id, title, description, deadline, completed=False):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.deadline = deadline
        self.completed = completed

    def mark_as_completed(self):
        self.completed = True


class TaskRepository:
    def __init__(self):
        self.conn = sqlite3.connect("tasks.db")
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                task_id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                deadline TEXT,
                completed INTEGER
            )
        """)

        self.conn.commit()

    def get_incomplete_tasks(self):
        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT * FROM tasks WHERE completed = 0
        """)

        rows = cursor.fetchall()
        tasks: list = []
        for row in rows:
            task_id, title, description, deadline, completed = row
            tasks.append(Task(task_id, title, description, deadline, bool(completed)))

        return tasks

    def get_completed_tasks(self):
        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT * FROM tasks WHERE completed = 1
        """)

        rows = cursor.fetchall()
        tasks = []
        for row in rows:
            task_id, title, description, deadline, completed = row
            tasks.append(Task(task_id, title, description, deadline, bool(completed)))

        return tasks

    def create_task(self, title, description, deadline):
        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT INTO tasks (title, description, deadline, completed)
            VALUES (?, ?, ?, 0)
        """, (title, description, deadline))

        self.conn.commit()

    def get_task(self, task_id):
        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT * FROM tasks WHERE task_id = ?
        """, (task_id,))

        row = cursor.fetchone()
        if row:
            task_id, title, description, deadline, completed = row
            return Task(task_id, title, description, deadline, bool(completed))
        return None

    def get_all_tasks(self):
        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT * FROM tasks
        """)

        rows = cursor.fetchall()
        tasks = []
        for row in rows:
            task_id, title, description, deadline, completed = row
            tasks.append(Task(task_id, title, description, deadline, bool(completed)))

        return tasks

    def update_task(self, task_id, **kwargs):
        cursor = self.conn.cursor()

        values: list = []
        for key, value in kwargs.items():
            values.append(f"{key} = :{key}")

        query = f"""
            UPDATE tasks
            SET {', '.join(values)}
            WHERE task_id = :task_id
        """

        try:
            cursor.execute(query, {"task_id": task_id, **kwargs})
            self.conn.commit()
            return True
        except:
            return False

    def delete_task(self, task_id):
        cursor = self.conn.cursor()

        cursor.execute("""
            DELETE FROM tasks WHERE task_id = ?
        """, (task_id,))

        self.conn.commit()
        return cursor.rowcount > 0
