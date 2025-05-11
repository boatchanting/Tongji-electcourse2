// ----------------------------------
// ---------- 与后端交互 -------------
// ----------------------------------
let currentLogTask = null, logTimer = null;

// 显示错误 Modal
function showErrorModal(msg) {
  document.getElementById('modal-error-body').textContent = msg;
  document.getElementById('modal-error').classList.add('active');
}
// 隐藏错误 Modal
function hideErrorModal() {
  document.getElementById('modal-error').classList.remove('active');
}

// 登录函数
async function login() {
  if (!document.getElementById('agree').checked) {
    showErrorModal('请先同意用户守则');
    return;
  }
  const u = document.getElementById('username').value;
  const p = document.getElementById('password').value;
  const success = await window.pywebview.api.login(u, p);
  if (success) {
    document.getElementById('login').style.display = 'none';
    document.getElementById('main').style.display = 'block';
    refreshTasks();
  } else {
    showErrorModal('登录失败，请检查用户名或密码');
  }
}

function viewLogin() {
  clearInterval(logTimer);
  document.getElementById('main').style.display = 'none';
  document.getElementById('login').style.display = 'flex';
}

async function addTask() {
  const c = document.getElementById('course_no').value;
  const r = document.getElementById('max_retry').value;
  if (!c) return showErrorModal('请输入课程编号');
  await window.pywebview.api.add_task(c,r);
  refreshTasks();
}

async function startTask(id) {
  await window.pywebview.api.start_task(id); refreshTasks();
}
async function stopTask(id) {
  await window.pywebview.api.stop_task(id); refreshTasks();
}

async function refreshTasks() {
const tasks = await window.pywebview.api.get_tasks();
const tb = document.getElementById('tasks_body');
tb.innerHTML = '';
tasks.forEach(t => {
  const tr = document.createElement('tr');
  tr.innerHTML = `
    <td>${t.course_number}</td>
    <td>${t.max_retries}</td>
    <td>${t.status}</td>
    <td>
      <button onclick="startTask('${t.id}')">开始</button>
      <button onclick="stopTask('${t.id}')">停止</button>
      <button onclick="showLogs('${t.id}')">日志</button>
    </td>
    <td>
      <button class="delete-btn" onclick="deleteTask('${t.id}')">删除</button>
    </td>
  `;
  tb.appendChild(tr);
});
}

// 服务于 deleteTask 函数，显示确认弹窗
// 弹窗 Promise 化，msg 为提示内容
function showConfirmModal(msg) {
  return new Promise(resolve => {
    document.getElementById('modal-confirm-body').textContent = msg;
    const modal = document.getElementById('modal-confirm');
    modal.classList.add('active');

    // 绑定一次性回调
    window._confirmResolve = result => {
      resolve(result);
      delete window._confirmResolve;
    };
  });
}
// 服务于 deleteTask 函数，隐藏弹窗
function hideConfirmModal(result) {
  document.getElementById('modal-confirm').classList.remove('active');
  // 调用 resolve
  if (window._confirmResolve) window._confirmResolve(result);
}

// deleteTask 函数, 调用 showConfirmModal 确认删除
async function deleteTask(id) { // 删除任务
  if (await showConfirmModal('确定要删除这个任务吗？')) {
    await window.pywebview.api.delete_task(id);
    // 如果当前在看该任务日志，停止轮询
    if (currentLogTask === id) {
      clearInterval(logTimer);
      currentLogTask = null;
      document.getElementById('log_area').value = '';
    }
    refreshTasks();
  }
}

function showLogs(tid) {
  currentLogTask = tid; document.getElementById('log_area').value = '';
  if (logTimer) clearInterval(logTimer);
  logTimer = setInterval(async ()=>{
    const lines = await window.pywebview.api.get_logs(currentLogTask);
    if (lines.length) {
      const area = document.getElementById('log_area');
      lines.forEach(l=> area.value += l + '\n');
      area.scrollTop = area.scrollHeight;
    }
  }, 500);
}
