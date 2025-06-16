// ---------------- 推送消息弹窗逻辑 ----------------
function showPushModal(html) {
  const pushLines = [
    '👍 收到！',
    '🐵 我知道啦~',
    '🚀 Let’s go!',
    '🚀 冲鸭!',
    '🙆‍♀️ 明白，继续冲！',
    '📝 去抢课咯！',
    '🌟 嗯呐谢谢提醒～',
    '🫡 遵命，长官！',
    '📚 马上安排！',
    '🐣 你太美',
    '🥺 明白了',
    '🐱 好耶~',
    '🐶 好哒~',
    '⚔️ 冲刺！',
    '🎉 好哒~',
    '🏃 马上去',
  ];
  const randomBtnText = pushLines[Math.floor(Math.random() * pushLines.length)];

  document.getElementById('modal-push-body').innerHTML = html;
  document.getElementById('modal-push-btn').textContent = randomBtnText;
  document.getElementById('modal-push').classList.add('active');
}

function hidePushModal() {
  document.getElementById('modal-push').classList.remove('active');
}

// ---------------- 示例推送 ----------------
window.addEventListener('DOMContentLoaded', () => {
  // 立即推送
  showPushModal(
    '🎉 <strong>Tongji-Electcourse2</strong> 祝您第三轮选课愉快！<br>' +
    '📣 如果你觉得这个程序有用，不妨把它 <strong>分享给更多小伙伴</strong> 吧～<br>' +
    '✨ 祝你选上心仪课程，选课顺利！<br>'+
    '经反馈，本版本未提供改选课功能，可以在程序自动查找课程完毕后，手动点击选课系统页面取消键实现，该问题后续将添加代码自动化完成，完成后将会在第一时间推送更新消息'
  );

  // 延时推送 Star 提醒
  setTimeout(() => {
    showPushModal(
      '您对本应用的使用体验如何？<br>' +
      '觉得还不错的话，欢迎前往 ' +
      '<a href="https://github.com/boatchanting/Tongji-Electcourse2" target="_blank">GitHub&nbsp;项目页 ⭐</a> 点个&nbsp;star！<br>'+
      '🛠️ 有功能建议或遇到问题？<br>欢迎前往 <a href="https://github.com/boatchanting/Tongji-Electcourse2/issues" target="_blank">Issues 区</a> 留言反馈！',
    );
  }, 500_000);  // 8min20s
});
