function initSpeechToText() {
  const startButton = document.getElementById("startStopButton");
  // WebkitSpeechRecognitionをサポートしているか確認
  if (!("webkitSpeechRecognition" in window)) {
    alert(
      "WebkitSpeechRecognitionはこのブラウザではサポートされていません。Chromeをお試しください。"
    );
    return;
  }

  const recognition = new webkitSpeechRecognition();
  let isRecognizing = false;

  recognition.lang = "ja-JP";
  recognition.interimResults = true;
  recognition.continuous = true;

  recognition.onstart = function () {
    isRecognizing = true;
    startButton.textContent = "音声認識を停止";
  };

  recognition.onend = function () {
    isRecognizing = false;
    startButton.textContent = "音声認識を開始";
  };

  recognition.onresult = function (event) {
    let interimTranscript = "";
    for (let i = event.resultIndex; i < event.results.length; i++) {
      let transcript = event.results[i][0].transcript;
      if (event.results[i].isFinal) {
        document.getElementById("result").value = transcript;
      } else {
        interimTranscript = transcript;
      }
    }
    document.getElementById("result").value += interimTranscript;
  };

  startButton.addEventListener("click", function () {
    if (isRecognizing) {
      recognition.stop();
    } else {
      document.getElementById("result").value = ""; // テキストエリアをクリア
      recognition.start();
    }
  });
}
window.addEventListener("load", () => {
  initSpeechToText();
});
