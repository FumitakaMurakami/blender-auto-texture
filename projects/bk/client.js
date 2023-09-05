const startButton = document.getElementById("start");
const stopButton = document.getElementById("stop");
const outputArea = document.getElementById("output");

let mediaRecorder;

startButton.onclick = function () {
  const constraints = { audio: true, video: false };
  navigator.mediaDevices.getUserMedia(constraints).then((stream) => {
    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.start();

    const audioChunks = [];
    mediaRecorder.ondataavailable = (event) => {
      audioChunks.push(event.data);
    };

    mediaRecorder.onstop = () => {
      const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
      sendDataToServer(audioBlob);
    };

    stopButton.disabled = false;
    startButton.disabled = true;
  });
};

stopButton.onclick = function () {
  mediaRecorder.stop();
  stopButton.disabled = true;
  startButton.disabled = false;
};

function sendDataToServer(blob) {
  console.log("sendDataToServer", blob);
  const formData = new FormData();
  formData.append("audio", blob);

  fetch("/transcribe", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("data", data);
      outputArea.value = data.transcript;
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}
