const host = "http://localhost:8000";
window.addEventListener("load", () => {
  /**
   * ファイルアップロードとイメージ読み取り、BASE64変換
   */
  const imageDataEl = document.getElementById("imageData");
  imageDataEl.addEventListener("change", (event) => {
    const [file] = event.target.files;
    const preview = document.getElementById("preview");

    if (file) {
      preview.setAttribute("src", URL.createObjectURL(file));
      preview.style.display = "block";

      const reader = new FileReader();
      reader.onload = (event) => {
        const base64Text = event.currentTarget.result;

        document.querySelector("#base64text").value = base64Text.split(",")[1];
      };
      reader.readAsDataURL(file);
    } else {
      preview.style.display = "none";
    }

    console.log(file);
    const imageFile = new File([], file.name, {
      type: "image/png",
    });
    const dt = new DataTransfer();
    dt.items.add(imageFile);
    document.getElementsByName("imageData")[0].files = dt.files;
  });

  /**
   * 送信ボタン
   */
  const sendButton = document.getElementById("send");
  sendButton.addEventListener("click", async () => {
    const data = {
      file_name: "test",
      image_body_b64: document.getElementById("base64text").value,
      ext_without_dot: "png",
    };
    console.log(data);
    const response = await fetch(host + "/images/to_canvas", {
      method: "post",
      headers: {
        accept: "application/json",
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
      },
      body: JSON.stringify(data),
    });
    const responseJson = await response.json();
    const get_model_url = responseJson.get_model_url;
    window.open(get_model_url, "__blank");
  });

  /**
   * 接続確認ボタン
   */
  const helloBtn = document.getElementById("helloBtn");
  helloBtn.addEventListener("click", async () => {
    const response = await fetch(host);
    const resJson = await response.json();
    console.log(resJson);
    alert(resJson.message);
  });

  /**
   * 音声認識ボタン操作
   */
  const speechToTextButton = document.getElementById("speechToTextButton");
  speechToTextButton.addEventListener("click", async () => {
    alert(await speechToText("promptText"));
  });

  // 翻訳
  async function translationExec(text) {
    const API_KEY = "0f6d969e-4476-b856-d215-e2a6aeb7d88f:fx";
    const API_URL = "https://api-free.deepl.com/v2/translate";

    let content = encodeURI(
      "auth_key=" + API_KEY + "&text=" + text + "&source_lang=JA&target_lang=EN"
    );
    let url = API_URL + "?" + content;

    let response = await fetch(url);
    let json = await response.json();
    console.log(json);
    return json["translations"][0]["text"];
  }

  /**
   * 翻訳ボタン
   */
  const translationButton = document.getElementById("translationButton");
  translationButton.addEventListener("click", async (e) => {
    const promptExchanged = document.getElementById("promptExchanged");
    const speechText = document.getElementById("result");
    const translated = await translationExec(speechText.value);
    console.log(translated);
    promptExchanged.value = translated;
  });
});
