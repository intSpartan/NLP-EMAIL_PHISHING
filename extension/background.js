chrome.runtime.onInstalled.addListener(() => {
  chrome.action.setBadgeText({
    text: "0",
  });
});

const gmail = 'https://mail.google.com';

chrome.action.onClicked.addListener(async (tab) => {
  if (tab.url.startsWith(gmail)) {
    const prevState = await chrome.action.getBadgeText({ tabId: tab.id });
    const nextState = prevState === '1' ? '0' : '1';
    await chrome.action.setBadgeText({
      tabId: tab.id,
      text: nextState,
    });

    if (nextState === "1") {
      await chrome.scripting.executeScript({
        target : { tabId : tab.id },
        files : [ "gmail-apply.js" ],
      })
    } else if (nextState === "0") {
      await chrome.scripting.executeScript({
        target : { tabId : tab.id },
        files : [ "gmail-remove.js" ],
      })
    }
  }
});

chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
  fetch("http://localhost:3000/analyze", {
    method: 'POST',
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json; charset=utf-8'
    },
    body: JSON.stringify({ email_content: request.data })
  })
    .then(response => response.json())
    .then(response => sendResponse(response))
    .catch(error => console.log('Error:', error));
  return true;
});