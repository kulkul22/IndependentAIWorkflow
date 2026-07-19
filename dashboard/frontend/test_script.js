const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

function makeElement() {
    return {
        children: [],
        className: '',
        innerHTML: '',
        textContent: '',
        appendChild(child) {
            this.children.push(child);
        }
    };
}

function loadDashboardScript() {
    const columns = {
        '#col-todo .column-content': makeElement(),
        '#col-in_progress .column-content': makeElement(),
        '#col-in_test .column-content': makeElement(),
        '#col-stuck .column-content': makeElement(),
        '#col-done .column-content': makeElement()
    };
    const document = {
        addEventListener() {},
        createElement: makeElement,
        querySelector(selector) {
            return columns[selector];
        }
    };
    const context = vm.createContext({ document, EventSource: function EventSource() {} });
    const source = fs.readFileSync(path.join(__dirname, 'script.js'), 'utf8');
    vm.runInContext(`${source}\nthis.renderKanbanForTest = renderKanban;`, context);
    return { columns, renderKanban: context.renderKanbanForTest };
}

test('processing tickets render in the working column', () => {
    const { columns, renderKanban } = loadDashboardScript();

    renderKanban([{ title: 'Implement parser fix', status: 'processing' }]);

    assert.equal(columns['#col-todo .column-content'].children.length, 0);
    assert.equal(columns['#col-in_progress .column-content'].children.length, 1);
});
