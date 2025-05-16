// 显示错误 Modal
function showErrorModal(msg) {
  document.getElementById('modal-error-body').textContent = msg;
  document.getElementById('modal-error').classList.add('active');
}
// 隐藏错误 Modal
function hideErrorModal() {
  document.getElementById('modal-error').classList.remove('active');
}