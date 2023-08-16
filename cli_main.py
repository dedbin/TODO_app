import cmd
from task import TaskRepository

class TodoApp(cmd.Cmd):
    def __init__(self):
        super().__init__()
        self.prompt = ">>> "
        self.intro = "Добро пожаловать в приложение для отслеживания задач!"

        self.task_repository = TaskRepository()

    def do_create_task(self, arg):
        """
        Создать новую задачу.
        Формат: create_task title, description, deadline
        Пример: create_task Покупки, Купить продукты для ужина, 2023-08-19
        """
        args = arg.split(",")
        title = args[0].strip()
        description = args[1].strip()
        deadline = args[2].strip()
        self.task_repository.create_task(title, description, deadline)
        print("Задача создана успешно!")

    def do_get_task(self, task_id):
        """
        Получить задачу по идентификатору.
        Формат: get_task task_id
        Пример: get_task 1
        """
        task_id = int(task_id)
        task = self.task_repository.get_task(task_id)
        if task:
            print(task.__dict__)
        else:
            print("Задача не найдена!")

    def do_get_all_tasks(self, arg):
        """
        Получить все задачи.
        Формат: get_all_tasks
        """
        tasks = self.task_repository.get_all_tasks()
        for task in tasks:
            print(task.__dict__)

    def do_update_task(self, arg):
        """
        Обновить задачу по идентификатору.
        Формат: update_task task_id key1=value1 key2=value2 ...
        Пример: update_task 1 title=Новый заголовок description=Новое описание
        """
        args = arg.split(",")
        task_id = int(args[0].strip())
        updates = {}
        for pair in args[1:]:
            key, value = pair.split("=")
            updates[key.strip()] = value.strip()
        success = self.task_repository.update_task(task_id, **updates)
        if success:
            print("Задача обновлена успешно!")
        else:
            print("Задача не найдена!")

    def do_delete_task(self, task_id):
        """
        Удалить задачу по идентификатору.
        Формат: delete_task task_id
        Пример: delete_task 1
        """
        task_id = int(task_id)
        success = self.task_repository.delete_task(task_id)
        if success:
            print("Задача удалена успешно!")
        else:
            print("Задача не найдена!")

    def do_exit(self, arg):
        """
        Выйти из приложения.
        Формат: exit
        """
        print("До свидания!")
        return True

    def do_help(self, arg):
        """
        Вывести список доступных команд или получить помощь по конкретной команде.
        Формат: help [command]
        Пример: help create_task
        """
        if arg:
            # Вывести помощь по конкретной команде
            try:
                doc = getattr(self, "do_" + arg).__doc__
                if doc:
                    print(doc)
                else:
                    print("Нет помощи для этой команды.")
            except AttributeError:
                print("Нет такой команды.")
        else:
            # Вывести список доступных команд
            print("Список доступных команд:")
            command_names = [cmd[3:] for cmd in self.get_names() if cmd.startswith("do_")]
            for command_name in command_names:
                print(command_name)


if __name__ == "__main__":
    app = TodoApp()
    app.cmdloop()