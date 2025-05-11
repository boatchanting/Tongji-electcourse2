// ---------- Q&A 逻辑 ---------- 
document.addEventListener('DOMContentLoaded', () => {
  // Q&A 数据
  const qaContentArr = [
    {
      q: "1. 这个程序只是代替鼠标进行点击操作吗？",
      a: "是的，但是其可以自动运行并支持后台运行，并有实时展示以及所有过程的日志信息，想去干什么事情都是可以滴~"
    },
    {
      q: "2. 会不会导致信息泄露？",
      a: "不会，本程序完全本地运行，信息仅用于选课系统的身份验证，并不会上传您的信息。如果您对此不放心的话，也可以查看源代码或自行根据源代码运行本程序。"
    },
    {
      q: "3. 可以同时选择多门课程吗？",
      a: "当然可以！您可以添加多个任务，每个任务对应一门课程。程序对每个任务进行独立的操作，不会相互干扰。"
    },
    {
      q: "4. 如何确保程序的稳定性？",
      a: "程序经过多次测试，确保在大多数情况下能够稳定运行。如果遇到问题，可以通过查看日志信息定位问题，或者提交 Issues 寻求帮助。"
    },
    {
      q: "5. 是否需要安装额外的浏览器驱动？",
      a: "默认情况下，程序使用 Edge 浏览器。如果系统未自带 Edge WebDriver，您需要手动安装并配置环境变量。具体步骤请参考 Edge WebDriver 下载页面。"
    },
    {
      q: "6. 如何更新到最新版本？",
      a: "您可以直接从 Releases 页面下载最新版本的可执行文件，或者通过 Git 拉取最新代码并自行构建：<br><code>git pull origin main</code>"
    },
  ];

  let qaStep = 0;
  const qaModal     = document.getElementById('qa-modal');
  const qaShowLink  = document.getElementById('qa-showLink');
  const qaCloseBtn  = document.getElementById('qa-closeBtn');
  const qaPrevBtn   = document.getElementById('qa-prevBtn');
  const qaNextBtn   = document.getElementById('qa-nextBtn');
  const qaContent   = document.getElementById('qa-content');

  function qaUpdateButtons() {
    // 第一步隐藏“上一个”
    qaPrevBtn.style.display = qaStep === 0 ? 'none' : 'inline-block';
    // 最后一步按钮文字改为“完成”，否则“下一个”
    qaNextBtn.textContent = qaStep === qaContentArr.length - 1 ? '完成' : '下一个';
  }

  function qaRenderStep() {
    const item = qaContentArr[qaStep];
    qaContent.innerHTML = `<h4>${item.q}</h4><p>${item.a}</p>`;
    qaUpdateButtons();
  }

  window.qaOpen = () => {
    qaStep = 0;
    qaRenderStep();
    qaModal.classList.add('active');
  };
  window.qaClose = () => {
    qaModal.classList.remove('active');
  };
  window.qaNext = () => {
    if (qaStep < qaContentArr.length - 1) {
      qaStep++;
      qaRenderStep();
    } else {
      qaClose();
    }
  };
  window.qaPrev = () => {
    if (qaStep > 0) {
      qaStep--;
      qaRenderStep();
    }
  };

  // 绑定事件
  qaShowLink.addEventListener('click', qaOpen);
  qaCloseBtn.addEventListener('click', qaClose);
  qaNextBtn.addEventListener('click', qaNext);
  qaPrevBtn.addEventListener('click', qaPrev);
});