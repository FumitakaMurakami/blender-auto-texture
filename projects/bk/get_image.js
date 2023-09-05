const imageId = "7bf67cb7-93a1-46b4-90b1-d9d374ae617c"; // <<< TODO: change this to image ID (the ID you got from previous request)

async function main() {
  try {
    const response = await fetch(
      `https://demo.imagineapi.dev/items/images/${imageId}`,
      {
        method: "GET",
        headers: {
          Authorization: "Bearer 57dzT_G5ZlH3bMk05jZZ74-E0PMS8Bdz", // <<<< TODO: remember to change this
          "Content-Type": "application/json",
        },
      }
    );

    const responseData = await response.json();
    console.log(responseData);
  } catch (error) {
    console.error("Error", error);
    throw error;
  }
}

main();
