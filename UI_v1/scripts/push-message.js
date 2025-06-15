// ---------------- 推送消息弹窗逻辑 ----------------
function showPushModal(html){
  document.getElementById('modal-push-body').innerHTML = html;   // 支持富文本
  document.getElementById('modal-push').classList.add('active');
}
function hidePushModal(){
  document.getElementById('modal-push').classList.remove('active');
}

// 页面加载立即推送第一条；500s 后再推第二条
window.addEventListener('DOMContentLoaded', () => {
  // 立即推送
//   showPushModal(
//     '经反馈，有同学对<strong>改选课</strong>有需求，<br>' +
//     '本程序暂未支持，可在进入选课页面后手动取消 / 添加课程实现。'
//   );
  showPushModal(
  '🎉 <strong>Tongji-Electcourse2</strong> 祝您第三轮选课愉快！<br>' +
  '📣 如果你觉得这个程序有用，不妨把它 <strong>分享给更多小伙伴</strong> 吧～<br>' +
  '✨ 祝你选上心仪课程，选课顺利！'
);



  //  500 s 之后推送「Star」提醒
  setTimeout(() => {
    showPushModal(
      '您对本应用的使用体验如何？<br>' +
      '觉得还不错的话，欢迎前往 ' +
      '<a href="https://github.com/boatchanting/Tongji-Electcourse2" target="_blank">GitHub&nbsp;项目页 ⭐</a> 点个&nbsp;star！'
    );
  }, 20_000);   // 500 s = 8 分 20 秒
});
