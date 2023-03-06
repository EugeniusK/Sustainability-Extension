function handleMessage(request, sender, sendResponse) {
  if (request.type == "contentToBackground") {
    console.log("content to bc");
    console.log(request.co2_to_extension);

    chrome.storage.local.get(["co2"]).then((result) => {
      co2_before = parseFloat(result.co2);
      chrome.storage.local.set({
        co2: co2_before + parseFloat(request.co2_to_extension),
      });
      chrome.runtime.sendMessage({
        co2: co2_before + parseFloat(request.co2_to_extension),
      });
      sendResponse({ co2: request.co2 });
    });

    console.log("message sent to popup");
    console.log(request.co2_to_extension);
  } else {
    console.log("popup to bc");
    chrome.storage.local.get(["co2"]).then((result) => {
      sendResponse({ co2: result.co2 });
    });
  }
  return true;
}
chrome.runtime.onMessage.addListener(handleMessage);
