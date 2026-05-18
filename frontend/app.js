const matlabCode = document.getElementById("matlab-code");
const pythonCode = document.getElementById("python-code");
const output = document.getElementById("output");
const translateBtn = document.getElementById("translate-btn");
const runBtn = document.getElementById("run-btn");
const loadBtn = document.getElementById("load-btn");
const fileInput = document.getElementById("file-input");

// =========================
// LOAD FILE
// =========================
loadBtn.addEventListener("click", () => {
    fileInput.click();
});

fileInput.addEventListener("change", (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
        matlabCode.value = e.target.result;
    };
    reader.readAsText(file);
});

// =========================
// TRANSLATE
// =========================
translateBtn.addEventListener("click", async () => {
    const code = matlabCode.value;
    try {
        const response = await fetch("/translate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ code: code })
        });

        const data = await response.json();

        if (data.success) {
            pythonCode.value = data.python;
            output.textContent = "Translation successful.";
        } else {
            output.textContent = data.error;
        }
    } catch (error) {
        output.textContent = "Cannot connect to backend.";
    }
});

// =========================
// RUN PYTHON
// =========================
runBtn.addEventListener("click", async () => {
    const code = pythonCode.value;
    try {
        const response = await fetch("/run", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ code: code })
        });

        const data = await response.json();

        if (data.success) {
            output.textContent = data.stdout || data.stderr;
        } else {
            output.textContent = data.error;
        }
    } catch (error) {
        output.textContent = "Cannot connect to backend.";
    }
});