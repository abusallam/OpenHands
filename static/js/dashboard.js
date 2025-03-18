// Token management
let token = localStorage.getItem('token');

// Navigation
document.querySelectorAll('nav a').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const section = e.target.getAttribute('href').substring(1);
        showSection(section);
    });
});

function showSection(sectionName) {
    document.querySelectorAll('main > div').forEach(div => {
        div.classList.add('hidden');
    });
    document.getElementById(`${sectionName}-section`).classList.remove('hidden');
}

// User management
async function loadUsers() {
    try {
        const response = await fetch('/users/', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        const users = await response.json();
        displayUsers(users);
        updateTotalUsers(users.length);
    } catch (error) {
        console.error('Error loading users:', error);
    }
}

function displayUsers(users) {
    const tbody = document.getElementById('users-table-body');
    tbody.innerHTML = users.map(user => `
        <tr>
            <td class="px-6 py-4 whitespace-nowrap">${user.username}</td>
            <td class="px-6 py-4 whitespace-nowrap">${user.email}</td>
            <td class="px-6 py-4 whitespace-nowrap">${user.is_admin ? 'Admin' : 'User'}</td>
            <td class="px-6 py-4 whitespace-nowrap">
                <button onclick="editUser('${user.id}')" class="text-blue-600 hover:text-blue-900 mr-2">Edit</button>
                <button onclick="deleteUser('${user.id}')" class="text-red-600 hover:text-red-900">Delete</button>
            </td>
        </tr>
    `).join('');
}

function updateTotalUsers(count) {
    document.getElementById('total-users').textContent = count;
}

// Modal management
function showAddUserModal() {
    document.getElementById('add-user-modal').classList.remove('hidden');
}

function hideAddUserModal() {
    document.getElementById('add-user-modal').classList.add('hidden');
}

// Form handling
document.getElementById('add-user-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const userData = {
        username: document.getElementById('username').value,
        email: document.getElementById('email').value,
        is_admin: document.getElementById('is-admin').checked
    };

    try {
        const response = await fetch('/users/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(userData)
        });

        if (response.ok) {
            hideAddUserModal();
            loadUsers();
        } else {
            const error = await response.json();
            alert(error.detail);
        }
    } catch (error) {
        console.error('Error adding user:', error);
        alert('Error adding user');
    }
});

// Initialize dashboard
async function initializeDashboard() {
    await loadUsers();
    showSection('dashboard');
}

// Start the application
initializeDashboard(); 