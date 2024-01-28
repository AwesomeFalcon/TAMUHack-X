document.getElementById("scrapeEmails").addEventListener("click", async () => {
    let [tab] = await chrome.tabs.query({active: true, currentWindow: true})

    chrome.scripting.executeScript({
        target: {tabId: tab.id}, func: scrapeEmailsFromPage()
    });
})

async function scrapeEmailsFromPage() {
    const html = document.documentElement.outerHTML;
    const doc = new DOMParser().parseFromString(html, 'text/html');

    const paragraphs = doc.querySelectorAll('p'); 
    const extractedText = Array.from(paragraphs).map(p => p.textContent.trim()).join('\n');
    alert("hi");

    return extractedText; 
}