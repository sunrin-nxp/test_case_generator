const CLIENT = process.env.CLIENT;

document.getElementById('testcase-form').addEventListener('submit', async function(e) {
    e.preventDefault();

    const language = document.getElementById('language').value;
    const problem = document.getElementById('problem').value;

    const response = await fetch(CLIENT + '/generate-testcases', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ language, problem }),
    });

    const data = await response.json();
    const testcaseList = document.getElementById('testcase-list');
    testcaseList.innerHTML = '';

    data.testCases.forEach(testCase => {
        const li = document.createElement('li');
        li.textContent = testCase;
        testcaseList.appendChild(li);
    });
});
