// =========================
// CodeMirror
// =========================

const matlabEditor = CodeMirror.fromTextArea(
    document.getElementById("matlab-code"),
    {
        lineNumbers: true,
        mode: "text/plain",
        theme: "default",
        autoCloseBrackets: true,
        indentUnit: 4,
        tabSize: 4
    }
);

const pythonEditor = CodeMirror.fromTextArea(
    document.getElementById("python-code"),
    {
        lineNumbers: true,
        mode: "python",
        theme: "default",
        autoCloseBrackets: true,
        indentUnit: 4,
        tabSize: 4
    }
);

// =========================
// Elements
// =========================

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

    if (!file)
        return;

    const reader = new FileReader();

    reader.onload = (e) => {
        matlabEditor.setValue(e.target.result);
    };

    reader.readAsText(file);

});

// =========================
// TRANSLATE
// =========================

translateBtn.addEventListener("click", async () => {

    const code = matlabEditor.getValue();

    try {

        const response = await fetch("/translate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                code: code
            })
        });

        const data = await response.json();

        if (data.success) {

            pythonEditor.setValue(data.python);

            output.textContent =
                "Translation successful.";

        } else {

            output.textContent =
                data.error;
        }

    } catch (error) {

        output.textContent =
            "Cannot connect to backend.";
    }

});

// =========================
// RUN PYTHON
// =========================

runBtn.addEventListener("click", async () => {

    const code = pythonEditor.getValue();

    try {

        const response = await fetch("/run", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                code: code
            })
        });

        const data = await response.json(   );

        if (data.success) {

            output.textContent =
                data.stdout || data.stderr;

        } else {

            output.textContent =
                data.error;
        }

    } catch (error) {

        output.textContent =
            "Cannot connect to backend.";
    }

});