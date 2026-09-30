// Article comments live in GitHub Discussions; no credentials belong in this file.
(() => {
  const container = document.querySelector(".giscus");
  if (!container) return;

  const origin = "https://giscus.app";
  const currentTheme = () =>
    document.documentElement.dataset.theme === "dark" ? "dark_dimmed" : "light";
  const syncTheme = () => {
    const frame = container.querySelector("iframe.giscus-frame");
    frame?.contentWindow?.postMessage(
      { giscus: { setConfig: { theme: currentTheme() } } }, origin
    );
  };

  // Keep comments in sync with Mana's manual theme switch.
  new MutationObserver(syncTheme).observe(document.documentElement, {
    attributes: true,
    attributeFilter: ["data-theme"],
  });
  // An iframe can appear after the user switches themes during initial loading.
  const frameObserver = new MutationObserver(() => {
    const frame = container.querySelector("iframe.giscus-frame");
    if (!frame) return;
    frame.addEventListener("load", syncTheme);
    syncTheme();
    frameObserver.disconnect();
  });
  frameObserver.observe(container, { childList: true });

  const script = document.createElement("script");
  script.src = `${origin}/client.js`;
  script.async = true;
  script.crossOrigin = "anonymous";
  Object.assign(script.dataset, container.dataset, {
    mapping: "pathname",
    strict: "1",
    reactionsEnabled: "1",
    emitMetadata: "0",
    inputPosition: "top",
    theme: currentTheme(),
    loading: "lazy",
  });
  script.addEventListener("error", () => {
    container.textContent = "评论暂时无法加载，请稍后重试，或使用下方 GitHub 链接。";
  });
  container.append(script);
})();
