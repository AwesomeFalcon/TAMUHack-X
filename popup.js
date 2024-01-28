document.getElementById("scrapeEmails").addEventListener("click", async () => {
  let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: scrapeEmailsFromPage,
  });
});

function scrapeEmailsFromPage() {
  let el = document.getElementsByClassName("gs")[0].children[2];
  let content = el.innerText;
  console.log(content);

  var inputData = {
    text: content,
  };

  // Convert the inputData to a query string
  var queryString = Object.keys(inputData)
    .map((key) => key + "=" + inputData[key])
    .join("&");

  // Make a GET request to the /predict endpoint
  fetch("http://localhost:5000/predict?" + queryString)
    .then((response) => response.json())
    .then((data) => {
      // Handle the result
      console.log("Prediction result:", data);

      if (!document.getElementById("safePercentage")) {
        let safeP = document.createElement("p");
        safeP.id = "safePercentage";
        safeP.innerHTML = `${(data * 100).toFixed(4)}% safe`;
        el.appendChild(safeP);

        let style = document.createElement("style");
        style.innerHTML = `
          #safePercentage {
            color: green;
          }
        `;
        document.head.appendChild(style);
      } else {
        document.getElementById("safePercentage").innerHTML = `${(
          data * 100
        ).toFixed(4)}% safe`;
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}
