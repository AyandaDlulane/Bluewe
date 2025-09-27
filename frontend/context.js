// Collect page URL
const url = window.location.href;

// Collect HTML code as plain text
const htmlText = document.documentElement.outerHTML;

// Collect all inline and external JavaScript code as plain text
async function collectJavaScript() {
    let scripts = Array.from(document.scripts);
    let jsText = '';

    for (let script of scripts) {
        if (script.src) {
            // Fetch external JS
            try {
                let res = await fetch(script.src);
                if (res.ok) {
                    jsText += `\n// Source: ${script.src}\n` + await res.text();
                }
            } catch (e) {
                // Ignore fetch errors
            }
        } else {
            // Inline JS
            jsText += `\n// Inline script\n` + (script.textContent || '');
        }
    }
    return jsText;
}

(async () => {
    const jsText = await collectJavaScript();

    // Prepare payload for POST
    const payload = {
        html_content: "test for warning" ,//htmlText,
        javascript_content:   "test for warning",//jsText
        url: url
    }; 

    // Use POST request
    try {
        const res = await fetch("https://bluewe.vercel.app/api/check", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        // Expecting: { response: "...", status: "1" or "0" }
        if (data.status === "1") {
            alert(data.response || "Warning: This site may be malicious!");
        }
        // If 0, do nothing
        console.log(data.status);
        console.log(data.response);
    } catch (e) {
        // Ignore errors silently
    }
})();