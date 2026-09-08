import { app } from "../../scripts/app.js";

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
            const button = this.addWidget("button", "전체 해제 · 모두 none", null, () => {
                for (const widget of this.widgets ?? []) {
                    if (!categoryNames.has(widget.name)) continue;
                    // Linked inputs are controlled upstream, not by their hidden widget.
                    if (this.inputs?.some(input => input.name === widget.name && input.link != null)) continue;
                    widget.value = "none";
                    widget.callback?.(widget.value, app.canvas, this, undefined, undefined);
                }
                this.setDirtyCanvas(true, true);
                app.graph?.change?.();
            }, { serialize: false });
            this.widgets.splice(this.widgets.indexOf(button), 1);
            this.widgets.unshift(button);
            this._healingClearButton = button;
            return result;
        };
        // Keep the UI-only top button out of positional workflow values.
        for (const method of ["serialize", "configure"]) {
            const original = nodeType.prototype[method];
            nodeType.prototype[method] = function (...args) {
                const button = this._healingClearButton;
                if (button) this.widgets = this.widgets.filter(widget => widget !== button);
                try {
                    if (method === "serialize") {
                        this.properties ??= {};
                        this.properties.healingCategoryControls = 1;
                    }
                    if (method === "configure" && !args[0]?.properties?.healingCategoryControls) {
                        // Old workflows ended with start/reset integers. They must
                        // not become the new count/pose menu values.
                        const info = args[0];
                        if (Array.isArray(info?.widgets_values)) {
                            const countIndex = this.widgets.findIndex(widget => widget.name === "촬영_인원");
                            const values = info.widgets_values.slice();
                            if (countIndex >= 0) values.splice(countIndex);
                            args[0] = { ...info, widgets_values: values };
                        }
                    }
                    const result = original?.apply(this, args);
                    if (method === "configure") {
                        const mode = this.widgets?.find(widget => widget.name === "시드_모드");
                        if (mode?.value === "순차") {
                            for (const widget of this.widgets) {
                                if (categoryNames.has(widget.name) && widget.value === "random") {
                                    widget.value = "순차";
                                }
                            }
                            mode.value = "고정";
                        } else if (mode?.value === "완전랜덤") {
                            mode.value = "자동";
                        }
                        this.properties ??= {};
                        this.properties.healingCategoryControls = 1;
                    }
                    return result;
                } finally {
                    if (button) this.widgets.unshift(button);
                }
            };
        }
    },
});
