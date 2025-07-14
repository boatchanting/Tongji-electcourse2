let versionConflictModalShown = false;

/**
 * 提取形如 "Tongji-electcourse2v1.2.0" 中的 "v1.2.0"
 */
function parseVersion(str) {
  const match = str?.match(/v\d+\.\d+\.\d+/);
  return match ? match[0] : '';
}

/**
 * 版本检查函数
 */
function UpdateCheck() {
  if (versionConflictModalShown) return;
  if (!window.pywebview || !window.pywebview.api) return;

  let attempts = 0;
  const maxAttempts = 300; // 15秒，每50ms尝试一次，共300次
  const interval = 50; // 每50ms轮询一次

  const checkVersionInterval = setInterval(() => {
    window.pywebview.api.get_version().then(data => {
      const remoteVer = parseVersion(data?.version);
      const targetVer = 'v1.2.1';

      if (!remoteVer || remoteVer !== targetVer) {
        clearInterval(checkVersionInterval); // 获取到版本信息，停止轮询
        versionConflictModalShown = true;
        showUpdateModal(remoteVer || '未知版本', targetVer);
      } else {
        clearInterval(checkVersionInterval); // 获取到目标版本，停止轮询
        showWelcomePush();
      }
    }).catch(() => {
      // 获取版本失败，继续尝试
    });

    attempts++;
    if (attempts >= maxAttempts) {
      clearInterval(checkVersionInterval); // 超过15秒，停止轮询
      versionConflictModalShown = true;
      showUpdateModal('获取失败', 'v1.2.1');
    }
  }, interval);
}

// ---------------- 推送消息弹窗逻辑 ----------------
function showPushModal(html) {
  const pushLines = [
    '👍 收到！', '🐵 我知道啦~', '🚀 Let’s go!', '🚀 冲鸭!',
    '🙆‍♀️ 明白，继续冲！', '📝 去抢课咯！', '🌟 嗯呐谢谢提醒～',
    '🫡 遵命，长官！', '📚 马上安排！', '🐣 你太美',
    '🥺 明白了', '🐱 好耶~', '🐶 好哒~', '⚔️ 冲刺！',
    '🎉 好哒~', '🏃 马上去',
  ];
  const randomBtnText = pushLines[Math.floor(Math.random() * pushLines.length)];

  document.getElementById('modal-push-body').innerHTML = html;
  document.getElementById('modal-push-btn').textContent = randomBtnText;
  document.getElementById('modal-push').classList.add('active');
}

function hidePushModal() {
  document.getElementById('modal-push').classList.remove('active');
}

// 针对版本不匹配的更新提示
function showUpdateModal(current, target) {
  showPushModal(
    '🎉 <strong>Tongji-Electcourse2</strong> 祝您第三轮选课愉快！<br>' +
    '📣 如果你觉得这个程序有用，不妨把它 <strong>分享给更多小伙伴</strong> 吧～<br>' +
    '✨ 祝你选上心仪课程，选课顺利！<br>'+ 
    '经反馈，本版本未提供改选课功能，可在程序自动查找课程后手动点击选课系统页面取消键实现，该问题在新版本已经实现。'+
    `当前版本：<code>${current}</code><br>` +
    `目标版本：<code>${target}</code><br><br>` +
    '请前往 <a href="https://boatchanting.github.io/Tongji-electcourse2/UI_v1/introduction.html" target="_blank">Tongji-electcourse2 项目页</a> 下载最新版本，' +
    '以体验改选课功能及其他最新改进。'
  );
}

// 普通欢迎推送（仅在版本符合时显示）
function showWelcomePush() {
  showPushModal(
    '🎉 <strong>Tongji-Electcourse2</strong> 祝您第三轮选课愉快！<br>' +
    '📣 如果你觉得这个程序有用，不妨把它 <strong>分享给更多小伙伴</strong> 吧～<br>' +
    '✨ 祝你选上心仪课程，选课顺利！<br>'
  );

  // 延时推送 Star 提醒
  setTimeout(() => {
    showPushModal(
      '您对本应用的使用体验如何？<br>' +
      '觉得还不错的话，欢迎前往 ' +
      '<a href="https://github.com/boatchanting/Tongji-Electcourse2" target="_blank">GitHub&nbsp;项目页 ⭐</a> 点个&nbsp;star！<br>' +
      '🛠️ 有功能建议或遇到问题？<br>欢迎前往 ' +
      '<a href="https://github.com/boatchanting/Tongji-Electcourse2/issues" target="_blank">Issues 区</a> 留言反馈！'
    );
  }, 500_000);  // 8 min 20 s
}

// ---------------- 初始化 ----------------
window.addEventListener('DOMContentLoaded', () => {
  UpdateCheck();               // 先执行版本检查
});
