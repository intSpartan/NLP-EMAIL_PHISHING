function check(content) {
  // fetch('http://localhost:3000/analyze email_content=urgent
  return chrome.runtime.sendMessage({ data: content });
}

function getElementsByXpath(receiver, path) {
  return document.evaluate(path, receiver, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
}

function insertAfter(referenceNode, newNode) {
  referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
}

function isHidden(el) {
  return (el.offsetParent === null)
}

var allTables = getElementsByXpath(document, "//div[@class='Cp']//tbody");

for (var i=0 ; i < allTables.snapshotLength; i++) {
  var table = allTables.snapshotItem(i);
  if (isHidden(table)) continue;
  var emails = Array.from(table.children);
  var email_contents = emails.map(e => e.innerText);

  Promise.all(email_contents.map(async c => (await check(c)).is_phishing))
  .then(classification => {
    console.log(classification);
    emails.forEach((email, i) => {
      // var target = getElementsByXpath(email, "//*[contains(@class, 'yX') and contains(@class, 'xY')]").snapshotItem(0);
      // insertAfter(target, document.createTextNode(classification[i]));
      var node = document.createElement('div');
      node.style = 'position: absolute;';
      node.className = 'nlp-project';
      node.appendChild(document.createTextNode(classification[i] ? "SPAM" : "LEGIT"));
      email.appendChild(node);
    });
    // console.log(classification);
  });
}

//div[@class='Cp']//tbody