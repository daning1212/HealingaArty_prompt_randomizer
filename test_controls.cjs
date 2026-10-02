const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");
let extension;
const app = { registerExtension: value => extension = value, graph: { change() {} } };
vm.runInNewContext(fs.readFileSync(__dirname + "/js/controls.js", "utf8")
    .replace(/^import .*;\n/, ""), { app });
class Node {
    constructor() {
        this.properties = {};
        this.widgets = [
            {name: "시드", value: 42}, {name: "시드_모드", value: "고정"},
            {name: "표정", value: "random"}, {name: "표정_가중치", value: 1.2},
            {name: "추가_태그", value: "high quality"},
            {name: "서서포즈", value: "순차"}, {name: "앉기포즈", value: "none"},
            {name: "촬영_인원", value: "6"}, {name: "프로필_단체포즈", value: "순차"},
            {name: "누워포즈", value: "none"}, {name: "이미지방향", value: false},
            {name: "의상제거", value: false}, {name: "팬티스타킹", value: "none"},
            {name: "팬티스타킹_가중치", value: 1}
        ];
        this.onNodeCreated();
    }
    addWidget(type, name, value, callback, options) {
        const widget = {type, name, value, callback, options};
        this.widgets.push(widget);
        return widget;
    }
    setDirtyCanvas() {}
    serialize() {
        const widgets = this.widgets.filter(w => w.serialize !== false);
        return {properties: {...this.properties}, widgets_values: widgets.map(w => w.value),
            widgets_values_named: Object.fromEntries(widgets.map(w => [w.name, w.value]))};
    }
    configure(info) {
        this.properties = {...info.properties};
        const widgets = this.widgets.filter(w => w.serialize !== false);
        if (info.widgets_values_named) {
            for (const w of widgets) if (Object.hasOwn(info.widgets_values_named, w.name)) w.value = info.widgets_values_named[w.name];
        } else info.widgets_values?.forEach((value, index) => { if (widgets[index]) widgets[index].value = value; });
    }
}
extension.beforeRegisterNodeDef(Node, {name: "HealingArtyPromptRandomizerV11",
    input: {optional: Object.fromEntries(["표정","서서포즈","앉기포즈","촬영_인원","프로필_단체포즈","누워포즈","팬티스타킹"]
        .map(name => [name, [["none", "random", "순차"]]]))}});
const node = new Node();
const before = node.serialize();
assert.equal(before.widgets_values.length, 14);
node.widgets.find(w => w.name === "의상제거").value = true;
node._healingClearButton.callback();
for (const name of ["표정","서서포즈","앉기포즈","촬영_인원","프로필_단체포즈","누워포즈","팬티스타킹"]) {
    assert.equal(node.widgets.find(w => w.name === name).value, "none");
}
assert.equal(node.widgets.find(w => w.name === "의상제거").value, false);
assert.equal(node.widgets.find(w => w.name === "시드").value, 42);
assert.equal(node.widgets.find(w => w.name === "표정_가중치").value, 1.2);
assert.equal(node.widgets.find(w => w.name === "추가_태그").value, "high quality");
node.configure(before);
assert.deepEqual(node.serialize(), before);
assert.equal(node.widgets.at(-1).type, "button");
const legacy = new Node();
legacy.widgets.find(w => w.name === "촬영_인원").value = "none";
legacy.widgets.find(w => w.name === "프로필_단체포즈").value = "none";
legacy.configure({widgets_values: [7, "순차", "random", 1, "tags", "random", "none", 1, 0]});
assert.equal(legacy.widgets.find(w => w.name === "시드_모드").value, "고정");
assert.equal(legacy.widgets.find(w => w.name === "표정").value, "순차");
assert.equal(legacy.widgets.find(w => w.name === "촬영_인원").value, "none");
assert.equal(legacy.widgets.find(w => w.name === "프로필_단체포즈").value, "none");
const broken = new Node();
const good = before.widgets_values;
broken.configure({properties: {healingCategoryControls: 1}, widgets_values: [null, null, ...good],
    widgets_values_named: {시드: null, 시드_모드: 42, 표정_가중치: "none"}});
assert.equal(broken.widgets.find(w => w.name === "시드").value, 42);
assert.equal(broken.widgets.find(w => w.name === "시드_모드").value, "고정");
assert.equal(broken.widgets.find(w => w.name === "표정_가중치").value, 1.2);
for (let i = 0; i < 10; i++) {
    const saved = JSON.parse(JSON.stringify(broken.serialize()));
    broken.configure(saved);
    assert.deepEqual(JSON.parse(JSON.stringify(broken.serialize())), saved);
}
assert.equal(broken.widgets.filter(w => w === broken._healingClearButton).length, 1);
console.log("PASS: clear-all, preserved controls, save/reload, legacy migration");

// Exercise migration with the complete backend schema and an actual v1-shaped
// snapshot, including the two leading nulls and corrupted named values.
const schema = JSON.parse(require("node:child_process").execFileSync("python", ["-c",
    "import json; from updated_prompt_randomizer import HealingArtyPromptRandomizerV11 as N; print(json.dumps(N.INPUT_TYPES()))"], {cwd: __dirname}));
const full = Object.create(Node.prototype);
full.properties = {};
full.widgets = Object.entries({...schema.required, ...schema.optional})
    .filter(([, spec]) => !spec[1]?.forceInput)
    .map(([name, spec]) => ({name, value: Array.isArray(spec[0]) ? spec[0][0] : (spec[1]?.default ?? "")}));
full.onNodeCreated();
const values = full.widgets.filter(w => w.serialize !== false).map(w => w.value);
const names = full.widgets.filter(w => w.serialize !== false).map(w => w.name);
values[names.indexOf("이미지방향")] = "portrait orientation, vertical composition";
full.configure({properties: {healingCategoryControls: 1}, widgets_values: [null, null, ...values],
    widgets_values_named: Object.fromEntries(names.map((name, i) => [name, [null, ...values][i]]))});
assert.equal(full.widgets.find(w => w.name === "이미지방향").value, true);
assert.equal(full.widgets.find(w => w.name === "헤어스타일_가중치").value, 1);
assert.equal(full.widgets.find(w => w.name === "헤어스타일").value, "none");
for (let i = 0; i < 10; i++) {
    const saved = JSON.parse(JSON.stringify(full.serialize()));
    full.configure(saved);
    assert.deepEqual(JSON.parse(JSON.stringify(full.serialize())), saved);
}
console.log("PASS: full schema migration, named restore, repeated tab snapshots");

const missingDirection = values.slice();
missingDirection.splice(names.indexOf("이미지방향"), 1);
full.configure({properties: {healingCategoryControls: 1}, widgets_values: [null, null, ...missingDirection],
    widgets_values_named: {이미지방향: "none"}});
assert.equal(full.widgets.find(w => w.name === "의상제거").value, false);
assert.equal(full.widgets.find(w => w.name === "팬티스타킹").value, "none");
assert.equal(full.widgets.find(w => w.name === "팬티스타킹_가중치").value, 1);
console.log("PASS: missing direction slot recovery");
