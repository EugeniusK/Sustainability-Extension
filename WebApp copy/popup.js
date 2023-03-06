function handleResponse(message) {
  document.getElementsByClassName("CO2")[1].textContent =
    Math.round(message.co2 * 100) / 100 + " kg";
  return true;
}
window.onload = (event) => {
  const sending = chrome.runtime.sendMessage({
    type: "popupToBackground",
  });
  sending.then(handleResponse);
};

document.getElementsByClassName("CO2")[1].onMessage.addListener(handleMessage);

function handleMessage(request, sender, sendResponse) {
  document.getElementsByClassName("CO2")[1].textContent = request.co2 + " kg";
}
