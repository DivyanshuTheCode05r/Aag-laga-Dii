const rollNoInput = document.getElementById('rollNo');
const firstNameInput = document.getElementById('firstName');
const lastNameInput = document.getElementById('lastName');
const addBtn = document.getElementById('addBtn');
const clearBtn = document.getElementById('clearBtn');
const studentList = document.getElementById('studentList');
const countSpan = document.getElementById('count');

let students = JSON.parse(localStorage.getItem('itThirdYear')) || [];

function displayStudents() {
  studentList.innerHTML = '';
  students.forEach((student, index) => {
    const fullName = student.firstName + ' ' + student.lastName;
    const li = document.createElement('li');
    li.innerHTML = `
      <div><strong>Student ${index + 1}</strong></div>
      <div>Name - ${fullName}</div>
      <div>Roll No - ${student.rollNo}</div>
      <button class="delete-btn" onclick="deleteStudent(${index})">Delete</button>
    `;
    li.style.marginBottom = '15px';
    li.style.lineHeight = '1.4';
    studentList.appendChild(li);
  });
  countSpan.textContent = students.length;
}

function addStudent() {
  const rollNo = rollNoInput.value.trim();
  const firstName = firstNameInput.value.trim();
  const lastName = lastNameInput.value.trim();

  if (!rollNo || !firstName || !lastName) {
    alert('Please enter Roll No, First Name, and Last Name');
    return;
  }
  if (students.find(s => s.rollNo === rollNo)) {
    alert('Roll No already exists!');
    return;
  }

  students.push({ rollNo, firstName, lastName });
  localStorage.setItem('itThirdYear', JSON.stringify(students));
  rollNoInput.value = '';
  firstNameInput.value = '';
  lastNameInput.value = '';
  displayStudents();
}

function deleteStudent(index) {
  students.splice(index, 1);
  localStorage.setItem('itThirdYear', JSON.stringify(students));
  displayStudents();
}

function clearAll() {
  if (confirm('Clear all 3rd year data?')) {
    students = [];
    localStorage.removeItem('itThirdYear');
    displayStudents();
  }
}

addBtn.addEventListener('click', addStudent);
clearBtn.addEventListener('click', clearAll);

window.onload = displayStudents;
