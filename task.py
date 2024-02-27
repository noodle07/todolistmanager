import tkinter as tk
from tkinter import PhotoImage, Label, Entry, Button, simpledialog, Text, END
import csv

class TaskBase:
    def __init__(self, task_id, description, task_type):
        # construtor da classe Task
        self.id = task_id #o ID é atribuido posteriormente
        self.type = task_type
        self.description = description
        self.completed = False

    # metodo abstrato
    def mark_as_completed(self):
        # metodo para marcar a tarefa como concluida
        self.completed = True

class Task(TaskBase): #classe task(default) herda da classe TaskBase
    def __init__(self, task_id, description):
        super().__init__(task_id, description, 'D')

    def mark_as_completed(self):
        super().mark_as_completed()
        #print(f"Task ID:{self.id} marked as completed.")
        return 1 #tasktype

class MeetingTask(TaskBase):
    def __init__(self, task_id, description):
        super().__init__(task_id, description, 'M')

    def mark_as_completed(self):
        super().mark_as_completed()
        #print(f"MeetingTask ID:{self.id} marked as completed.")
        return 2 #tasktype

class ProjectTask(TaskBase):
    def __init__(self, task_id, description):
        super().__init__(task_id, description, 'P')

    def mark_as_completed(self):
            super().mark_as_completed()
            #print(f"ProjectTask ID:{self.id} marked as completed.")
            return 3 #tasktype

class AssignmentTask(TaskBase):
    def __init__(self, task_id, description):
        super().__init__(task_id, description, 'A')

    def mark_as_completed(self):
        super().mark_as_completed()
        #print(f"AssignmentTask ID:{self.id} marked as completed.")
        return 4 #tasktype

class TaskList:
    def __init__(self):
        # Construtor da classe TaskList
        self.tasks = []
        # Ler tasks de ficheiro .csv
        self.load_tasks_from_file()
        self.next_task_id = len(self.tasks) + 1 # Inicializa o próximo ID

    def add_task(self, task):
        # Ordenar a lista de tarefas com base nos IDs
        self.reorganize_ids()

        # Obter o próximo ID com base na lista ordenada
        if self.tasks:#verificar se a lista nao esta vazia
            self.next_task_id = self.tasks[-1].id + 1 #self.tasks[-1] refere se à ultima tarefa da lista ordenada(ordenada no metodo reorganize_ids)
        else:
            self.next_task_id = 1
        
        # Atribui o proximo ID à tarefa
        task.id = self.next_task_id  
        
        # Metodo para adicionar uam tarefa à lista de tarefas
        self.tasks.append(task)
        
        # Atualiza o proximo ID
        self.next_task_id += 1 

        # Salvar/Escrever no ficheiro .csv
        self.save_tasks_to_file()

    def add_task_with_type(self, task_type, description):
        task_id = self.next_task_id
        if task_type == 1:
            new_task = Task(task_id, description)
        elif task_type == 2:
            new_task = MeetingTask(task_id, description)
        elif task_type == 3:
            new_task = ProjectTask(task_id, description)
        elif task_type == 4:
            new_task = AssignmentTask(task_id, description)
        else:
            raise ValueError("Invalid task type")
        
        #Atualizar o tipo da tarefa
        new_task.type = 'D' if task_type == 1 else 'M' if task_type == 2 else 'P' if task_type == 3 else 'A'
        self.add_task(new_task)

    #metodo para eliminar tasks
    def delete_task(self, task_id):
        self.tasks = [task for task in self.tasks if task.id != task_id]
        self.reorganize_ids()
        self.save_tasks_to_file()

    #reorganizar a lista, para estar devidamente enumerada
        #os ids das tarefas por vezes mudam de valor, para que a lista esteja ordenada...
    def reorganize_ids(self):
        # Ordenar a lista de tarefas com base nos IDs
        self.tasks.sort(key=lambda task: task.id)

        # Atualizar os IDS de acordo com a ordem na lista
        for index, task in enumerate(self.tasks, start=1):
            task.id = index

    #ler tasks de ficheiro .csv (comma sepparated values)
    def load_tasks_from_file(self):
        try:
            with open('tasks.csv', 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    task_id = int(row['ID'])
                    description = row['Description']
                    completed = bool(int(row['Completed']))
                    task_type = row['Type']

                    if task_type == 'D':
                        task = Task(task_id, description)
                    elif task_type == 'M':
                        task = MeetingTask(task_id, description)
                    elif task_type == 'P':
                        task = ProjectTask(task_id, description)
                    elif task_type == 'A':
                        task = AssignmentTask(task_id, description)
                    else:
                        raise ValueError(f"Invalid task type: {task_type}")
                    
                    task.completed = completed
                    self.tasks.append(task)
        except FileNotFoundError:
            pass #Se o ficheiro nao for encontrado, nao fazer nada
    
    #Salvar no ficheiro .csv
    def save_tasks_to_file(self):
        with open('tasks.csv', 'w', newline='') as csvfile:
            fieldnames = ['ID', 'Type', 'Description', 'Completed']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for task in self.tasks:
                writer.writerow({'ID': task.id, 'Type': task.type, 'Description': task.description, 'Completed': int(task.completed)})

############GUI#############
class GUI:
    def __init__(self, master):
        #Construtor da classe GUI, recebe um objeto Tkinter como argumento
        self.master = master
        self.master.title("To-Do List Manager")
        self.master.geometry("400x550+400+100")
        self.master.resizable(False, False)

        #Janela de output
        self.output = Text(master, height=20, width=40, bg = "PaleGreen1", state="disabled")
        self.output.grid(row=2, columnspan=2) #adicionar o widget de texto a janela principal

        # Icon da aplicacao
        self.image_icon = PhotoImage(file="Image/task.png")
        self.master.iconphoto(False, self.image_icon)

        # Imagem na parte superior
        self.top_image = PhotoImage(file="Image/topbar.png")
        Label(self.master, image=self.top_image).grid(row=0, columnspan=2)

        #Imagem do icon "dock"
        self.dock_image=PhotoImage(file="Image/dock.png")
        Label(root, image=self.dock_image, bg="#8FD786").place(x=30,y=25)

        #Imagem do icone "note"
        self.note_image=PhotoImage(file="Image/task.png")
        Label(self.master, image=self.note_image, bg="#8FD786").place(x=340, y=25)

        #Titulo cabeçalho
        self.heading = Label(root, text="TASK LIST", font="arial 20 bold", fg="white", bg="#8FD786")
        self.heading.place(x=130, y=20)

        # Lista de tarefas
        self.task_list = TaskList()
        self.view_tasks() #imprimir lista de tarefas quando o programa inicia

        # Input/entrada de texto
        self.description_entry = Entry(self.master, width=40)
        self.description_entry.grid(row=1, column=0, padx=10, pady=10)

        # Botao de adicionar tarefas
        self.add_button = Button(self.master, text="Add Task", command=self.add_task)
        self.add_button.grid(row=1, column=1, padx=10, pady=10)

        # Botao para ver lista de tarefas
        self.view_button = Button(self.master, text="View Tasks", command=self.view_tasks)
        #self.view_button.grid(row=3,column=0, pady=10)
        self.view_button.place(x=50, y=460)
        
        # Botão para marcar tarefa como concluída
        self.mark_completed_button = Button(self.master, text="Mark as Completed", command=self.mark_task_as_completed)
        #self.mark_completed_button.grid(row=3,column=1, pady=10)
        self.mark_completed_button.place(x=140, y=460)
        
        # Botão para eliminar tasks
        self.delete_button = Button(self.master, text="Delete Task", command=self.delete_task)
        #self.delete_button.grid(row=3,column=2, pady=10)
        self.delete_button.place(x=280, y=460)

        # Autor label
        self.author_info_label = Label(self.master, text="Feito por aluno José Barroso, nº2104846")
        self.author_info_label.place(x=0, y = 530)
    
    # Metodo para limpar a janela de output
    def clear_output(self):
        # Tornar a caixa de texto editável temporariamente
        self.output.config(state="normal")
        self.output.delete(1.0, "end") #limpar a janela de output
        # Tornar a caixa de texto não editável novamente
        self.output.config(state="disabled")

    # Metodo para permitir output na janela de texto
    def add_output_text(self, text):
        # Tornar a caixa de texto editável temporariamente
        self.output.config(state="normal")
        # Adicionar o texto desejado à caixa de texto
        self.output.insert(END, text + "\n")
        # Tornar a caixa de texto não editável novamente
        self.output.config(state="disabled")
        
    # Metodo para adicionar tarefas à lista    
    def add_task(self):
        #obter a descricao da tarefa da caixa de entrada
        description = self.description_entry.get()

        # Obter o tipo de tarefa escolhido pelo usuário
        task_type = simpledialog.askinteger("Task Type", "Enter the task type(number) (1-Default/2-Meeting/3-Project/4-Assignment):")

        try:
            # Criar e adicionar a nova tarefa à lista de tarefas no objeto TaskList
            self.task_list.add_task_with_type(task_type, description)
            if task_type == 1:
                self.clear_output()
                self.add_output_text(f"Default task added.")#print(f"Default task added.")
            elif task_type == 2:
                self.clear_output()
                self.add_output_text(f"Meeting task added.") #print(f"Meeting task added.")
            elif task_type == 3:
                self.clear_output()
                self.add_output_text(f"Project task added." ) #print(f"Project task added.")
            elif task_type == 4:
                self.clear_output()
                self.add_output_text(f"Assignment task added.")#print(f"Assignment task added.")
        except ValueError as e:
            #print(f"Error: {e}")
            self.clear_output()
            self.add_output_text(f"Error: {e}")
        #limpar a caixa de entrada apos uma tarefa ter sido adicionada,
        #para se poder escrever(input) e adicionar novas tarefas
        self.description_entry.delete(0, END)

    # Metodo para eliminar tasks
    def delete_task(self):
        # Dialog para obter o ID da tarefa a ser marcada como concluída
        task_id_to_delete = simpledialog.askinteger("Delete Task", "Enter the ID of the task to be deleted:")

        if task_id_to_delete is not None:
            for task in self.task_list.tasks:
                if task.id == task_id_to_delete:
                    self.task_list.delete_task(task_id_to_delete)
                    self.clear_output()
                    #print(f"Task ID: {task_id_to_delete} deleted.")
                    self.add_output_text(f"Task ID: {task_id_to_delete} was deleted.")
                    return
            # Task Id nao foi encontrado
            self.clear_output()
            self.add_output_text(f"Task ID:{task_id_to_delete} not found.")#print(f"Task ID:{task_id_to_delete} not found.")

    # Metodo para imprimir a lista de tarefas
    def view_tasks(self):
        # Método para limpar a janela de output
        self.clear_output()
        #display no terminal da lista de tarefas
        # metodo para exibir as tarefas na lista (imprime no terminal)
        for task in self.task_list.tasks:
            #print(f"{task.id}[{task.type}]. {task.description} {'(Completed)' if task.completed else ''}")
            self.add_output_text(f"{task.id}[{task.type}]. {task.description} {'(Completed)' if task.completed else ''}")
    
    # Metodo para marcar uma tarefa como concluída
    def mark_task_as_completed(self): 

        # Dialog para obter o ID da tarefa a ser marcada como concluída
        task_id_to_mark = simpledialog.askinteger("Mark Task as Completed", "Enter the ID of the task to be marked as completed:")

        #marcar Task como completa
        if task_id_to_mark is not None:
            for task in self.task_list.tasks:
                if task.id == task_id_to_mark:
                    task_completed_type = task.mark_as_completed()
                    if task_completed_type == 1:
                        self.clear_output()
                        self.add_output_text(f"Task ID:{task.id} marked as completed.")#print(f"Default task added.")
                    elif task_completed_type == 2:
                        self.clear_output()
                        self.add_output_text(f"MeetingTask ID:{task.id} marked as completed.") #print(f"Meeting task added.")
                    elif task_completed_type == 3:
                        self.clear_output()
                        self.add_output_text(f"ProjectTask ID:{task.id} marked as completed." ) #print(f"Project task added.")
                    elif task_completed_type == 4:
                        self.clear_output()
                        self.add_output_text(f"AssignmentTask ID:{task.id} marked as completed.")#print(f"Assignment task added.")
                    self.task_list.save_tasks_to_file()  # Guardar no ficheiro .csv a alteracao de que a task foi completada.
                    return
            
            # Task Id nao foi encontrado
            self.clear_output()
            self.add_output_text(f"Task ID:{task_id_to_mark} not found.")#print(f"Task ID:{task_id_to_mark} not found.")

#main
if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()