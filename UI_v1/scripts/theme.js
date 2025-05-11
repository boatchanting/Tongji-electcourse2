// ---------- 主题逻辑 ----------
function setTheme(theme) {
    document.body.className = theme;
    localStorage.setItem('theme', theme);
  }
  function checkTimeTheme() {
    const h = new Date().getHours();
    return (h>=6 && h<18) ? '' : 'dark';
  }
  document.getElementById('lightBtn').onclick = ()=> setTheme('');
  document.getElementById('darkBtn').onclick = ()=> setTheme('dark');
  document.getElementById('blueBtn').onclick = ()=> setTheme('blue-theme');
  document.getElementById('greenBtn').onclick = ()=> setTheme('green-theme');
  document.getElementById('purpleBtn').onclick = ()=> setTheme('purple-theme');
  setTheme(localStorage.getItem('theme') || checkTimeTheme());