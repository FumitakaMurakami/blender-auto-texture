// 音声合成
function speak(button, text) {
  console.log("speak", button, text);
  const url =
    "https://texttospeech.googleapis.com/v1/text:synthesize?key=" +
    "AIzaSyBR2Q1j0FRzqROrnHz4Tu-P5-8PnYGIdzY";
  const data = {
    input: {
      text: text,
    },
    voice: {
      languageCode: "ja-JP",
      name: "ja-JP-Standard-B",
    },
    audioConfig: {
      audioEncoding: "MP3",
      speaking_rate: "1.00",
      pitch: "0.00",
    },
  };
  const otherparam = {
    headers: {
      "content-type": "application/json; charset=UTF-8",
    },
    body: JSON.stringify(data),
    method: "POST",
  };
  fetch(url, otherparam)
    .then((data) => {
      return data.json();
    })
    .then((res) => {
      console.log("res", res);
      try {
        var blobUrl = base64ToBlobUrl(res.audioContent);
        var audio = new Audio();
        audio.src = blobUrl;
        audio.play();
      } catch (e) {
        console.log(e);
      }
    })
    .catch((error) => alert(error));
}

// Base64 → BlobUrl
function base64ToBlobUrl(base64) {
  console.log("base64:", base64);
  var bin = atob(base64.replace(/^.*,/, ""));
  var buffer = new Uint8Array(bin.length);
  for (var i = 0; i < bin.length; i++) {
    buffer[i] = bin.charCodeAt(i);
  }
  return window.URL.createObjectURL(
    new Blob([buffer.buffer], { type: "audio/wav" })
  );
}
