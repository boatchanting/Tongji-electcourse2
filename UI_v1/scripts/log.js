// 日志的导出
async function exportLogs(format) {
  if (!currentLogTask) {
    return showErrorModal('请先选择并显示一个任务的日志');
  }

  const lines = await window.pywebview.api.get_logs(currentLogTask);
  if (!lines.length) {
    return showErrorModal('当前日志为空，无法复制');
  }

  // 生成内容
  let content;
  if (format === 'txt') {
    content = lines.join('\r\n');               // 纯文本
  } else if (format === 'json') {
    const arr = lines.map(line => {
      const m = line.match(/^\[(.*?)\]\s*(.*)$/);
      return { time: m ? m[1] : '', message: m ? m[2] : line };
    });
    content = JSON.stringify(arr, null, 2);     // JSON 字符串
  } else {
    return;
  }

  // 尝试写入剪贴板
  try {
    await navigator.clipboard.writeText(content);
    showErrorModal(`已将 ${format.toUpperCase()} 日志内容复制到剪贴板`);
  } catch (err) {
    console.error(err);
    showErrorModal('复制到剪贴板失败：浏览器/环境可能不支持 Clipboard API');
  }
}


