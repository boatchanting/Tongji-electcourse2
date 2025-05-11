// ---------- 操作引导 ----------
document.addEventListener('DOMContentLoaded', () => {
    const guideContentArr = [
      "步骤1: 请授权1系统学号和密码以登录系统，便于后续软件<strong>自动</strong>进行1系统的登录和选课操作。",
    "步骤2: 登录后，输入课程编号和最大重试次数，点击添加任务。",
    "步骤3: 点击“开始”按钮来启动任务，点击“停止”来关闭任务。",
    "步骤4: 查看选课日志，了解每次选课尝试的结果。",
    "步骤5: 完成选课后，您可以查看任务的状态，删除不需要的任务。",
    "tip1:点击界面上方的五个小按钮以切换主题。",
    "tip2:双击备注列以编辑备注信息。",
    "您已了解所有操作，Tongji-electcourse2 祝您选课愉快！"
    ];
    let guideStep = 0;
    
    const guideModal    = document.getElementById('guide-modal');
    const guideShowLink = document.getElementById('guide-showLink');
    const guideCloseBtn = document.getElementById('guide-closeBtn');
    const guidePrevBtn  = document.getElementById('guide-prevBtn');
    const guideNextBtn  = document.getElementById('guide-nextBtn');
    const guideContent  = document.getElementById('guide-content');
    
    function guideUpdateButtons() {
      guidePrevBtn.style.display = guideStep === 0 ? 'none' : 'inline-block';
      guideNextBtn.textContent = guideStep === guideContentArr.length - 1 
        ? '完成' 
        : '下一步';
    }
    
    function guideRenderStep() {
      guideContent.innerHTML = `<p>${guideContentArr[guideStep]}</p>`;
      guideUpdateButtons();
    }
    
    window.guideOpen = () => {
      guideStep = 0;
      guideRenderStep();
      guideModal.classList.add('active');
    };
    
    window.guideClose = () => {
      guideModal.classList.remove('active');
    };
    
    window.guideNext = () => {
      if (guideStep < guideContentArr.length - 1) {
        guideStep++;
        guideRenderStep();
      } else {
        guideClose();
      }
    };
    
    window.guidePrev = () => {
      if (guideStep > 0) {
        guideStep--;
        guideRenderStep();
      }
    };
    
    guideShowLink.addEventListener('click', guideOpen);
    guideCloseBtn.addEventListener('click', guideClose);
    guideNextBtn.addEventListener('click', guideNext);
    guidePrevBtn.addEventListener('click', guidePrev);
    });   