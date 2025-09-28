// content.js - Gmail email capture, send once per email
(() => {
  const BACKEND_URL = "https://blue-mail.vercel.app/api/check";
  const sentEmails = new Set();

  function safeText(node) {
    try { return node ? node.innerText || node.textContent || "" : ""; } 
    catch { return ""; }
  }

  function getEmailData(root) {
    const senderEl = root.querySelector('span.gD, span[email]');
    const sender = senderEl ? senderEl.getAttribute('email') || safeText(senderEl).trim() : "";

    const subjectEl = document.querySelector('h2.hP, h1.hP');
    const subject = subjectEl ? safeText(subjectEl).trim() : "";

    const bodyNode = root.querySelector('div.a3s, .ii.gt .a3s');
    const body_text = safeText(bodyNode).trim();

    const links = [];
    if (bodyNode) {
      bodyNode.querySelectorAll('a[href]').forEach(a => { links.push(a.href); });
    }

    return { sender, subject, body_text, links };
  }

  function fingerprint(data) {
    if (!data.sender && !data.subject) return null;
    return data.sender + "||" + data.subject;
  }

  async function postPayload(payload) {
    try {
      console.log("Sending payload:", payload);
      const res = await fetch(BACKEND_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      const responseData = await res.json();
      console.log("Received response:", responseData);
      if (responseData.status === "1") alert(responseData.response || "Suspicious email detected!");
    } catch (e) {
      console.error("Error sending payload:", e);
    }
  }

  async function trySend(root) {
    const data = getEmailData(root);
    const id = fingerprint(data);
    if (!id || sentEmails.has(id)) return;
    if (!data.sender && !data.subject && (!data.body_text || data.body_text.length < 20)) return; // ignore empty
    sentEmails.add(id);
    await postPayload({
      url: window.location.href,
      sender: data.sender,
      subject: data.subject,
      body_text: data.body_text,
      links: data.links
    });
  }

  function observeEmails() {
    const observer = new MutationObserver(muts => {
      for (const m of muts) {
        if (!m.addedNodes) continue;
        for (const n of m.addedNodes) {
          if (!(n instanceof HTMLElement)) continue;
          // look for email panels
          if (n.querySelector && (n.querySelector('div.a3s') || n.querySelector('span.gD'))) {
            trySend(n);
          }
        }
      }
    });
    observer.observe(document.body, { childList: true, subtree: true });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", observeEmails);
  } else {
    observeEmails();
  }
})();

