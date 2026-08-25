let tasks = [];
let currentFilter = 'all';
let searchTerm = '';

function displayTasks() {
    const taskList = document.getElementById('task-list');
    taskList.innerHTML = '';
    const filteredTasks = tasks.filter(task => {
        if (currentFilter === 'all') return true;
        if (currentFilter === 'active') return !task.completed;
        if (currentFilter === 'completed') return task.completed;
        return true;
    }).filter(task => task.name.toLowerCase().includes(searchTerm.toLowerCase()));
    filteredTasks.forEach((task, index) => {
        const taskElement = document.createElement('li');
        taskElement.innerHTML = `
            <input type="checkbox" ${task.completed ? 'checked' : ''} data-index="${index}">
            <span>${task.name}</span>
            <button class="edit-task" data-index="${index}">Edit</button>
            <button class="delete-task" data-index="${index}">Delete</button>
        `;
        taskList.appendChild(taskElement);
    });
    document.getElementById('total-tasks').textContent = `Total tasks: ${tasks.length}`;
}

function addTask() {
    const taskInput = document.getElementById('task-input');
    const taskName = taskInput.value.trim();
    if (taskName) {
        tasks.push({ name: taskName, completed: false });
        taskInput.value = '';
        displayTasks();
    }
}

function editTask(index) {
    const editTaskInput = document.getElementById('edit-task-input');
    editTaskInput.value = tasks[index].name;
    document.getElementById('edit-task-form').style.display = 'block';
    document.getElementById('update-task').addEventListener('click', () => {
        tasks[index].name = editTaskInput.value.trim();
        displayTasks();
        document.getElementById('edit-task-form').style.display = 'none';
    });
    document.getElementById('cancel-edit-task').addEventListener('click', () => {
        document.getElementById('edit-task-form').style.display = 'none';
    });
}

function deleteTask(index) {
    tasks.splice(index, 1);
    displayTasks();
}

function markTaskAsCompleted(index, completed) {
    tasks[index].completed = completed;
    displayTasks();
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('add-task').addEventListener('click', () => {
        document.getElementById('task-form').style.display = 'block';
        document.getElementById('save-task').addEventListener('click', addTask);
        document.getElementById('cancel-task').addEventListener('click', () => {
            document.getElementById('task-form').style.display = 'none';
        });
    });
    document.getElementById('clear-completed').addEventListener('click', () => {
        tasks = tasks.filter(task => !task.completed);
        displayTasks();
    });
    document.getElementById('search-bar').addEventListener('input', (e) => {
        searchTerm = e.target.value.trim();
        displayTasks();
    });
    document.getElementById('all-filter').addEventListener('click', () => {
        currentFilter = 'all';
        document.getElementById('all-filter').classList.add('active');
        document.getElementById('active-filter').classList.remove('active');
        document.getElementById('completed-filter').classList.remove('active');
        displayTasks();
    });
    document.getElementById('active-filter').addEventListener('click', () => {
        currentFilter = 'active';
        document.getElementById('active-filter').classList.add('active');
        document.getElementById('all-filter').classList.remove('active');
        document.getElementById('completed-filter').classList.remove('active');
        displayTasks();
    });
    document.getElementById('completed-filter').addEventListener('click', () => {
        currentFilter = 'completed';
        document.getElementById('completed-filter').classList.add('active');
        document.getElementById('all-filter').classList.remove('active');
        document.getElementById('active-filter').classList.remove('active');
        displayTasks();
    });
    document.getElementById('task-list').addEventListener('click', (e) => {
        if (e.target.classList.contains('edit-task')) {
            editTask(e.target.dataset.index);
        } else if (e.target.classList.contains('delete-task')) {
            deleteTask(e.target.dataset.index);
        } else if (e.target.type === 'checkbox') {
            markTaskAsCompleted(e.target.dataset.index, e.target.checked);
        }
    });
});