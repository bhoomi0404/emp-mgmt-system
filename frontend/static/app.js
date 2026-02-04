// Employee Management App
const apiRoot = '/api/employees';
let allEmployees = [];

// Toast Notification System
function showToast(message, type = 'info', duration = 5000) {
  const toastContainer = document.getElementById('toastContainer');
  if (!toastContainer) return;
  
  const icons = {
    success: '✓',
    error: '✕',
    warning: '⚠',
    info: 'ℹ'
  };
  
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `
    <span class="toast-icon">${icons[type]}</span>
    <span>${escapeHtml(message)}</span>
    <button class="toast-close">&times;</button>
  `;
  
  toastContainer.appendChild(toast);
  
  const closeBtn = toast.querySelector('.toast-close');
  closeBtn.addEventListener('click', () => toast.remove());
  
  if (duration > 0) {
    setTimeout(() => {
      toast.style.animation = 'slideInRight 0.3s ease-out reverse';
      setTimeout(() => toast.remove(), 300);
    }, duration);
  }
}

function showError(msg) {
  console.error(msg);
  showToast(msg, 'error');
}

function showSuccess(msg) {
  console.log(msg);
  showToast(msg, 'success');
}

function showWarning(msg) {
  console.warn(msg);
  showToast(msg, 'warning');
}

async function fetchEmployees() {
  try {
    const res = await fetch(`${apiRoot}?limit=100`);
    if (!res.ok) throw new Error('Failed to load employees');
    const payload = await res.json();
    console.log('API Response:', payload);
    allEmployees = payload.data || [];
    console.log('Employees loaded:', allEmployees);
    renderEmployees(allEmployees);
  } catch (err) {
    console.error('Fetch error:', err);
    showError('Failed to load employees');
  }
}

function renderEmployees(list) {
  console.log('Rendering employees:', list);
  const tbody = document.querySelector('#employeesTable tbody');
  const noDataMsg = document.getElementById('noEmployees');
  
  console.log('Found tbody:', tbody);
  console.log('Found noDataMsg:', noDataMsg);
  
  tbody.innerHTML = '';
  
  if (!list || list.length === 0) {
    noDataMsg.style.display = 'block';
    return;
  }
  
  noDataMsg.style.display = 'none';
  
  list.forEach((emp, index) => {
    const tr = document.createElement('tr');
    tr.style.animationDelay = `${index * 0.05}s`;
    tr.innerHTML = `
      <td>${emp.id}</td>
      <td><strong>${escapeHtml(emp.first_name)} ${escapeHtml(emp.last_name)}</strong></td>
      <td>${escapeHtml(emp.email)}</td>
      <td>${escapeHtml(emp.department || '-')}</td>
      <td>${escapeHtml(emp.title || '-')}</td>
      <td class="emp-actions">
        <button class="btn-edit" data-id="${emp.id}">✎ Edit</button>
        <button class="btn-delete" data-id="${emp.id}">🗑 Delete</button>
      </td>
    `;
    tbody.appendChild(tr);
  });

  // Attach event handlers
  document.querySelectorAll('.btn-edit').forEach(btn => {
    btn.addEventListener('click', handleEditClick);
  });
  
  document.querySelectorAll('.btn-delete').forEach(btn => {
    btn.addEventListener('click', handleDelete);
  });
  
  // Update employee count
  const countEl = document.querySelector('.section-subtitle');
  if (countEl) {
    countEl.textContent = `${list.length} employee${list.length !== 1 ? 's' : ''} in system`;
  }
}

async function handleDelete(event) {
  event.preventDefault();
  const empId = this.getAttribute('data-id');
  const btn = this;
  
  // Get employee name for better message
  const row = btn.closest('tr');
  const nameCell = row.querySelector('td:nth-child(2)');
  const empName = nameCell ? nameCell.textContent : `#${empId}`;
  
  if (!confirm(`Delete ${empName}? This cannot be undone.`)) {
    return;
  }
  
  btn.disabled = true;
  btn.style.opacity = '0.6';
  
  try {
    const res = await fetch(`${apiRoot}/${empId}`, { method: 'DELETE' });
    if (!res.ok) {
      throw new Error(`Delete failed with status ${res.status}`);
    }
    showSuccess(`${empName} deleted successfully`);
    fetchEmployees();
  } catch (err) {
    console.error('Delete error:', err);
    showError('Failed to delete employee');
    btn.disabled = false;
    btn.style.opacity = '1';
  }
}

function escapeHtml(str) {
  if (!str) return '';
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

document.addEventListener('DOMContentLoaded', () => {
  console.log('Page loaded, fetching employees...');
  fetchEmployees();

  const form = document.getElementById('createForm');
  if (form) {
    form.addEventListener('submit', handleCreateEmployee);
  }
  
  // Modal handlers
  const editModal = document.getElementById('editModal');
  const closeBtn = document.querySelector('.modal-close');
  const cancelBtn = document.getElementById('cancelEditBtn');
  const editForm = document.getElementById('editForm');
  
  if (closeBtn) {
    closeBtn.addEventListener('click', () => {
      editModal.style.display = 'none';
    });
  }
  
  if (cancelBtn) {
    cancelBtn.addEventListener('click', () => {
      editModal.style.display = 'none';
    });
  }
  
  if (editForm) {
    editForm.addEventListener('submit', handleEditSubmit);
  }
  
  // Close modal when clicking outside
  window.addEventListener('click', (e) => {
    if (e.target === editModal) {
      editModal.style.display = 'none';
    }
  });
  
  // Search functionality
  const searchInput = document.getElementById('employeeSearch');
  if (searchInput) {
    searchInput.addEventListener('input', handleSearch);
  }
});

function handleSearch(event) {
  const searchTerm = event.target.value.toLowerCase().trim();
  
  if (!searchTerm) {
    renderEmployees(allEmployees);
    return;
  }
  
  const filtered = allEmployees.filter(emp => 
    emp.first_name.toLowerCase().includes(searchTerm) ||
    emp.last_name.toLowerCase().includes(searchTerm) ||
    emp.email.toLowerCase().includes(searchTerm)
  );
  
  renderEmployees(filtered);
}

async function handleEditClick(event) {
  event.preventDefault();
  const empId = this.getAttribute('data-id');
  
  try {
    const res = await fetch(`${apiRoot}/${empId}`);
    if (!res.ok) throw new Error('Failed to load employee');
    const emp = await res.json();
    
    // Populate edit form
    document.getElementById('editEmpId').value = emp.id;
    document.getElementById('edit_first_name').value = emp.first_name || '';
    document.getElementById('edit_last_name').value = emp.last_name || '';
    document.getElementById('edit_email').value = emp.email || '';
    document.getElementById('edit_department').value = emp.department || '';
    document.getElementById('edit_title').value = emp.title || '';
    document.getElementById('edit_salary').value = emp.salary || '';
    
    // Show modal
    document.getElementById('editModal').style.display = 'flex';
  } catch (err) {
    console.error('Failed to load employee:', err);
    showError('Failed to load employee details');
  }
}

async function handleEditSubmit(event) {
  event.preventDefault();
  
  const empId = document.getElementById('editEmpId').value;
  const formData = new FormData(this);
  const data = Object.fromEntries(formData);
  delete data.id; // Remove hidden id field
  
  // Remove empty fields
  Object.keys(data).forEach(k => {
    if (!data[k]) delete data[k];
  });
  
  const btn = this.querySelector('button[type="submit"]');
  btn.disabled = true;
  btn.style.opacity = '0.6';
  
  try {
    const res = await fetch(`${apiRoot}/${empId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    
    if (!res.ok) {
      const errorData = await res.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(errorData.detail || `Update failed with status ${res.status}`);
    }
    
    const updatedEmp = await res.json();
    console.log('Employee updated:', updatedEmp);
    showSuccess(`${updatedEmp.first_name} ${updatedEmp.last_name} updated successfully`);
    document.getElementById('editModal').style.display = 'none';
    fetchEmployees();
  } catch (err) {
    console.error('Update error:', err);
    showError(`Failed to update employee: ${err.message}`);
  } finally {
    btn.disabled = false;
    btn.style.opacity = '1';
  }
}

async function handleCreateEmployee(event) {
  event.preventDefault();
  console.log('Form submitted, creating employee...');
  
  const formData = new FormData(this);
  const data = Object.fromEntries(formData);
  console.log('Form data:', data);
  
  // Remove empty fields
  Object.keys(data).forEach(k => {
    if (!data[k]) delete data[k];
  });
  
  console.log('Data after removing empty fields:', data);
  
  const btn = this.querySelector('button[type="submit"]');
  const originalText = btn.textContent;
  btn.disabled = true;
  btn.style.opacity = '0.6';
  btn.textContent = '⏳ Creating...';
  
  try {
    console.log('Sending POST request to', apiRoot, 'with data:', data);
    const res = await fetch(apiRoot, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    
    console.log('Response status:', res.status);
    
    if (!res.ok) {
      const errorData = await res.json().catch(() => ({ detail: 'Unknown error' }));
      console.error('API error response:', errorData);
      throw new Error(errorData.detail || `Create failed with status ${res.status}`);
    }
    
    const newEmp = await res.json();
    console.log('Employee created:', newEmp);
    showSuccess(`${newEmp.first_name} ${newEmp.last_name} created successfully`);
    this.reset();
    fetchEmployees();
  } catch (err) {
    console.error('Create error:', err);
    showError(`Failed to create employee: ${err.message}`);
  } finally {
    btn.disabled = false;
    btn.style.opacity = '1';
    btn.textContent = originalText;
  }
}
