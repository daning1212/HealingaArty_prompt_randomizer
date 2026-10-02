import { app } from "../../scripts/app.js";

const VERSION = 2;
const directionValue = value => value === true || value === "세로" ||
    value === "portrait orientation, vertical composition";

app.registerExtension({
    name: "HealingArty.CategoryControls",
    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData.name !== "HealingArtyPromptRandomizerV11") return;
        const categoryNames = new Set(Object.entries(nodeData.input.optional ?? {})
            .filter(([, spec]) => Array.isArray(spec[0]) && spec[0].includes("none"))
            .map(([name]) => name));
        const created = nodeType.prototype.onNodeCreated;
        nodeType.prototype.onNodeCreated = function () {
            const result = created?.apply(this, arguments);
            // Keep UI-only controls after all persisted widgets. Never replace or
            // reorder the widget array: frontend serializers retain references.
            const button = this.addWidget("button", "전체 해제 · 모두 none", null, () => {
                for (const widget of this.widgets ?? []) {
                    if (!categoryNames.has(widget.name) && widget.name !== "의상제거") continue;
                    if (this.inputs?.some(input => input.name === widget.name && input.link != null)) continue;
                    widget.value = widget.name === "의상제거" ? false : "none";
                    widget.callback?.(widget.value, app.canvas, this, undefined, undefined);
                }
                this.setDirtyCanvas(true, true);
                app.graph?.change?.();
            }, { serialize: false });
            button.serialize = false;
            this._healingClearButton = button;
            return result;
        };
        const serialize = nodeType.prototype.serialize;
        nodeType.prototype.serialize = function (...args) {
            this.properties ??= {};
            this.properties.healingCategoryControls = VERSION;
            const info = serialize.apply(this, args);
            const widgets = (this.widgets ?? []).filter(w => w.serialize !== false);
            info.widgets_values = widgets.map(w => w.value);
            info.widgets_values_named = Object.fromEntries(widgets.map(w => [w.name, w.value]));
            return info;
        };
        const configure = nodeType.prototype.configure;
        nodeType.prototype.configure = function (info, ...args) {
            const widgets = (this.widgets ?? []).filter(w => w.serialize !== false);
            let values = info.widgets_values?.slice();
            const version = info.properties?.healingCategoryControls;
            let named = info.widgets_values_named;
            if (version !== VERSION && values) {
                // Broken v1 files can contain leading button/seed nulls while
                // the original seed and mode survive immediately after them.
                const offset = values.findIndex((v, i) => i <= 2 &&
                    typeof v === "number" && ["고정", "자동", "순차", "완전랜덤"].includes(values[i + 1]));
                if (offset > 0 && values.slice(0, offset).every(v => v == null)) values = values.slice(offset);
                const directionIndex = widgets.findIndex(w => w.name === "이미지방향");
                const clothingIndex = widgets.findIndex(w => w.name === "의상제거");
                // Some v1 snapshots lost the direction slot altogether, leaving
                // the intact clothing toggle and stocking values one slot early.
                if (version === 1 && values.length === widgets.length - 1 &&
                    directionIndex >= 0 && clothingIndex === directionIndex + 1 &&
                    typeof values[directionIndex] === "boolean" &&
                    typeof values[clothingIndex] === "string") {
                    values.splice(directionIndex, 0, directionValue(named?.["이미지방향"]));
                }
                if (!version) {
                    const countIndex = widgets.findIndex(w => w.name === "촬영_인원");
                    if (countIndex >= 0) values = values.slice(0, countIndex);
                }
                // v1 named values were generated against a reordered array.
                named = Object.fromEntries(widgets.slice(0, values.length).map((w, i) => [w.name, values[i]]));
            }
            if (named) {
                named = { ...named };
                if (Object.hasOwn(named, "이미지방향")) named["이미지방향"] = directionValue(named["이미지방향"]);
                values = widgets.map((w, i) => Object.hasOwn(named, w.name) ? named[w.name] : (values?.[i] ?? w.value));
            } else if (values) {
                const i = widgets.findIndex(w => w.name === "이미지방향");
                if (i >= 0 && i < values.length) values[i] = directionValue(values[i]);
            }
            const result = configure.call(this, { ...info, widgets_values: values,
                widgets_values_named: named }, ...args);
            const mode = this.widgets?.find(w => w.name === "시드_모드");
            if (mode?.value === "순차") {
                for (const w of this.widgets) if (categoryNames.has(w.name) && w.value === "random") w.value = "순차";
                mode.value = "고정";
            } else if (mode?.value === "완전랜덤") mode.value = "자동";
            this.properties ??= {};
            this.properties.healingCategoryControls = VERSION;
            return result;
        };
    },
});
