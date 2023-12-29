// static/script.js

document.addEventListener('DOMContentLoaded', function () {
    loadTasks();
});

function loadTasks() {
    fetch('/api/tasks')
        .then(response => response.json())
        .then(tasks => {
            const taskList = document.getElementById('taskList');
            taskList.innerHTML = '';

            tasks.forEach(task => {
                const listItem = document.createElement('li');
                listItem.textContent = task.name;

                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.checked = task.done;
                checkbox.addEventListener('change', function(event) {
                    markTaskAsDone(task.id, event.target.checked);
                });

                listItem.appendChild(checkbox);
                taskList.appendChild(listItem);
            });
        });
}

function addTask() {
    const taskInput = document.getElementById('taskInput');
    const taskName = taskInput.value.trim();

    if (taskName !== '') {
        fetch('/api/tasks', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name: taskName }),
        })
        .then(response => response.json())
        .then(() => {
            taskInput.value = '';
            loadTasks();
        });
    }
}

function markTaskAsDone(taskId, isChecked) {
    if (taskId !== undefined) {
        const taskIdString = taskId.toString();
        
        fetch(`/api/tasks/${taskIdString}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ done: isChecked }),
        })
        .then(response => response.json())
        .then(data => {
            if (data && data.done) {
                console.log('Task marked as done:', taskId);
                const listItem = document.querySelector(`input[type="checkbox"][value="${taskId}"]`).parentElement;
                if (listItem) {
                    listItem.remove();
                } else {
                    console.error('List item not found for task:', taskId);
                }
            } else {
                console.error('Failed to mark task as done:', data);
            }
        })
        .catch(error => console.error('Error:', error));
    }
}
