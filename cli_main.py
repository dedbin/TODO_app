import cmd
from task import TaskRepository
from pyfiglet import Figlet


class TodoApp(cmd.Cmd):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prompt = ">>> "
        self.intro = f"Добро пожаловать в приложение для отслеживания задач! \n {custom_fig.renderText('TODO app')}"

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
        try:
            task_id = int(task_id)
            task = self.task_repository.get_task(task_id)
            if task:
                print(task.__dict__)
            else:
                print("Нет такой задачи!")
        except:
            print("Нет такой задачи!")

    def do_get_all_tasks(self, arg):
        """
        Получить все задачи.
        Формат: get_all_tasks
        """
        tasks = self.task_repository.get_all_tasks()
        for task in tasks:
            print(task.__dict__)

    def do_mark_task_as_completed(self, task_id):
        """
        Отметить задачу как выполненную.
        Формат: mark_task_as_completed task_id
        Пример: mark_task_as_completed 1
        """
        try:
            task_id = int(task_id)
            success = self.task_repository.update_task(task_id, completed=True)
            if success:
                print("Задача отмечена как выполненная!")
            else:
                print("Задача не найдена!")
        except:
            print("Нет такой задачи!")

    def do_get_incomplete_tasks(self, arg):
        """
        Вывести список невыполненных задач.
        Формат: get_incomplete_tasks
        """
        incomplete_tasks = self.task_repository.get_incomplete_tasks()
        for task in incomplete_tasks:
            print(task.__dict__)

    def do_get_completed_tasks(self, arg):
        """
        Вывести список выполненных задач.
        Формат: get_completed_tasks
        """
        completed_tasks = self.task_repository.get_completed_tasks()
        for task in completed_tasks:
            print(task.__dict__)

    def do_update_task(self, arg):
        """
        Обновить задачу по идентификатору.
        Формат: update_task task_id key1=value1 key2=value2 ...
        Пример: update_task 1 title=Новый заголовок description=Новое описание
        """
        try:
            args = arg.split(",")
            print(f"{args[0][0] = }")
            task_id = int(args[0][0])
            print(f'{task_id = }')
            updates = {}
            for pair in args[1:]:
                key, value = pair.split("=")
                updates[key.strip()] = value.strip()
            print(f'{updates = }')
            success = self.task_repository.update_task(task_id, **updates)
            if success:
                print("Задача обновлена успешно!")
            else:
                print("Нет такой задачи!")
        except:
            print("При обновлении задачи произошла ошибка!")

    def do_delete_task(self, task_id):
        """
        Удалить задачу по идентификатору.
        Формат: delete_task task_id
        Пример: delete_task 1
        """
        try:
            task_id = int(task_id)
            success = self.task_repository.delete_task(task_id)
            if success:
                print("Задача удалена успешно!")
            else:
                print("Задача не найдена!")
        except:
            print("Нет такой задачи!")

    def do_exit(self, arg):
        """
        Выйти из приложения.
        Формат: exit
        """
        print("До свидания!")
        return True


if __name__ == "__main__":
    custom_fig = Figlet(font='slant')

    app = TodoApp()
    app.cmdloop()
