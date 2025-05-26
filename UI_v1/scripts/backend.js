// ----------------------------------
// ---------- 与后端交互 -------------
// ----------------------------------
let currentLogTask = null, logTimer = null;

function showErrorModal(msg) {
  document.getElementById('modal-error-body').innerHTML = msg;
  document.getElementById('modal-error').classList.add('active');
}
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

// 服务于 enableRemarkEdit 函数，双击备注列时启用编辑，td 为双击的单元格元素
function enableRemarkEdit(td) {
  if (td.querySelector('input')) return;

  const oldText = td.textContent;
  td.innerHTML = `<input type="text" value="${oldText}" style="width:100%">`;
  const input = td.firstElementChild;
  input.focus(); input.select();

  function save() {
    const newText = input.value.trim() || '无';
    td.textContent = newText;
    // 同步到后端：
    const taskId = td.dataset.taskId;
    window.pywebview.api.update_remark(taskId, newText);
  }

  input.addEventListener('blur', save);
  input.addEventListener('keydown', e => {
    if (e.key === 'Enter') input.blur();
    if (e.key === 'Escape') td.textContent = oldText;
  });
}

/** refreshTasks 函数
 * 刷新任务列表，从后端获取最新任务信息并更新到页面上
 */
async function refreshTasks() {
  const tasks = await window.pywebview.api.get_tasks();
  const tb = document.getElementById('tasks_body');
  tb.innerHTML = '';

  tasks.forEach(t => {
    const tr = document.createElement('tr');
    tr.dataset.taskId = t.id;

    tr.innerHTML = `
      <td>${t.course_number}</td>
      <td>${t.max_retries}</td>
      <td>${t.status}</td>
      <td>
        <button onclick="startTask('${t.id}')">开始</button>
        <button onclick="stopTask('${t.id}')">停止</button>
        <button onclick="showLogs('${t.id}')">日志</button>
      </td>
      <td class="remarks-cell"
          ondblclick="enableRemarkEdit(this)"
          data-task-id="${t.id}">${t.remark || '无'}</td>  <!-- 新增备注列 -->
      <td>
        <button class="delete-btn" onclick="deleteTask('${t.id}')">删除</button>
      </td>
    `;
    tb.appendChild(tr);
  });
}


// 显示确认弹窗
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

// showLogs, 显示任务日志
function showLogs(tid) {
  currentLogTask = tid;
  const tbody = document.getElementById('log_body');
  tbody.innerHTML = '';               // 清空之前的日志
  if (logTimer) clearInterval(logTimer);

  logTimer = setInterval(async () => {
    const lines = await window.pywebview.api.get_logs(currentLogTask);
    if (lines.length) {
      lines.forEach(line => {
        // 将 “[HH:MM:SS.xxx] 内容” 拆成两部分
        const match = line.match(/^\[(.*?)\]\s*(.*)$/);
        const time = match ? match[1] : '';
        const msg  = match ? match[2] : line;

        const tr = document.createElement('tr');
        const tdTime = document.createElement('td');
        const tdMsg  = document.createElement('td');

        tdTime.textContent = time;
        tdMsg.textContent  = msg;

        tr.appendChild(tdTime);
        tr.appendChild(tdMsg);
        tbody.appendChild(tr);
      });

      // 滚动到底部
      const container = document.querySelector('.log-table-container');
      container.scrollTop = container.scrollHeight;
    }
  }, 500);
}

