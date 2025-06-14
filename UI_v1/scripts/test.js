
  // 定义测试码（可自定义）
  const correctTestCode = "xuanke";

  // 页面加载时显示测试码模态框
  window.addEventListener('DOMContentLoaded', function () {
    document.getElementById('testcode-modal').style.display = 'flex';
    document.getElementById('main').style.display = 'none'; // 默认隐藏主界面
  });

  // 验证测试码
  function checkTestCode() {
    const input = document.getElementById('testcode-input').value.trim();
    const error = document.getElementById('testcode-error');

    if (input === correctTestCode) {
      // 测试码正确，隐藏模态框，显示主界面
      document.getElementById('testcode-modal').style.display = 'none';
      document.getElementById('main').style.display = 'block';
      return;
    }

    // 测试码错误，提示错误信息
    error.style.display = 'block';
    document.getElementById('testcode-input').value = '';
  }

  // 可选：按下回车键触发验证
  document.getElementById('testcode-input').addEventListener('keydown', function (e) {
    if (e.key === 'Enter') {
      checkTestCode();
    }
  });