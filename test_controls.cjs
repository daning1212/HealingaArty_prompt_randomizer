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
            {name: "누워포즈", value: "none"}, {name: "이미지방향", value: "none"},
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
        return {properties: {...this.properties}, widgets_values: this.widgets.map(w => w.value)};
    }
    configure(info) {
        this.properties = {...info.properties};
        info.widgets_values.forEach((value, index) => { if (this.widgets[index]) this.widgets[index].value = value; });
    }
}
extension.beforeRegisterNodeDef(Node, {name: "HealingArtyPromptRandomizerV11",
    input: {optional: Object.fromEntries(["표정","서서포즈","앉기포즈","촬영_인원","프로필_단체포즈","누워포즈","이미지방향","팬티스타킹"]
        .map(name => [name, [["none", "random", "순차"]]]))}});
const node = new Node();
const before = node.serialize();
assert.equal(before.widgets_values.length, 14);
node.widgets.find(w => w.name === "의상제거").value = true;
node.widgets[0].callback();
for (const name of ["표정","서서포즈","앉기포즈","촬영_인원","프로필_단체포즈","누워포즈","이미지방향","팬티스타킹"]) {
    assert.equal(node.widgets.find(w => w.name === name).value, "none");
}
assert.equal(node.widgets.find(w => w.name === "의상제거").value, false);
assert.equal(node.widgets.find(w => w.name === "시드").value, 42);
assert.equal(node.widgets.find(w => w.name === "표정_가중치").value, 1.2);
assert.equal(node.widgets.find(w => w.name === "추가_태그").value, "high quality");
node.configure(before);
assert.deepEqual(node.serialize(), before);
assert.equal(node.widgets[0].type, "button");
const legacy = new Node();
legacy.widgets.find(w => w.name === "촬영_인원").value = "none";
legacy.widgets.find(w => w.name === "프로필_단체포즈").value = "none";
legacy.configure({widgets_values: [7, "순차", "random", 1, "tags", "random", "none", 1, 0]});
assert.equal(legacy.widgets.find(w => w.name === "시드_모드").value, "고정");
assert.equal(legacy.widgets.find(w => w.name === "표정").value, "순차");
assert.equal(legacy.widgets.find(w => w.name === "촬영_인원").value, "none");
assert.equal(legacy.widgets.find(w => w.name === "프로필_단체포즈").value, "none");
console.log("PASS: clear-all, preserved controls, save/reload, legacy migration");
