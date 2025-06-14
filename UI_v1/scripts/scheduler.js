// scripts/schedule.js
(() => {
  let timerId = null;
  const disp  = document.getElementById('timer_display');
  const setBtn= document.getElementById('setTimerBtn');

  setBtn.addEventListener('click', () => {
    if (timerId) clearInterval(timerId);

    const mode = document.querySelector('input[name="timer_mode"]:checked').value;
    let target;

    if (mode === 'countdown') {
      const sec = +document.getElementById('countdown_seconds').value;
      if (!sec) return alert('请输入倒计时秒数');
      target = Date.now() + sec * 1000;
    } else {
      target = new Date(document.getElementById('fixed_time').value).getTime();
      if (isNaN(target))  return alert('请选择有效的时间');
      if (target <= Date.now()) return alert('指定时间已过，请重新选择');
    }

    timerId = setInterval(() => {
      const diff = target - Date.now();
      if (diff <= 0) {
        clearInterval(timerId);
        disp.textContent = '已触发，正在启动全部任务…';
        autoStartAll();
      } else {
        disp.textContent = '距离触发还有 ' + fmt(diff);
      }
    }, 1000);
  });

  function fmt(ms){
    const s = Math.floor(ms/1000);
    const h = String(Math.floor(s/3600)).padStart(2,'0');
    const m = String(Math.floor(s%3600/60)).padStart(2,'0');
    const sec = String(s%60).padStart(2,'0');
    return `${h}:${m}:${sec}`;
  }

  /** 不改 backend.js：直接找 inline-onclick=“startTask(…)” 的按钮 */
  function autoStartAll(){
    const btns = document.querySelectorAll('button[onclick^="startTask"]');
    if(!btns.length){
      disp.textContent = '未找到“开始”按钮';
      return;
    }
    btns.forEach(b => b.click());
    disp.textContent = `已自动触发 ${btns.length} 个任务`;
  }
})();
