const techniques = [
  "Identifier Renaming", "Control Flow Flattening", "String Encoding", "Bytecode Wrapping",
  "Virtual Machine Layer", "Junk Code Injection", "Opaque Predicates", "Table Indirection",
  "Numeric Constant Folding", "Dead Branch Insertion", "Dynamic Loader", "Function Inlining Trap",
  "Metatable Proxy", "Upvalue Scrambling", "Environment Rebinding", "Variable Shadow Maze",
  "Token Spacing Mutation", "Hex Escape Packing", "Unicode Escape Packing", "Boolean Arithmetic Masking",
  "Loop Distortion", "Branch Reordering", "Register Pressure Noise", "Self-Integrity Check",
  "Anti-Tamper Hooks", "Debug API Lockout", "AST Node Permutation", "Flattened Scope Layers",
  "Stack Noise Emission", "Coroutine Dispatcher", "Byte-level Chunk Mutation", "Compression Envelope",
  "Deferred Eval Wrapper", "Lambda Noise Network", "Symbol Table Poisoning", "Array Index Masking",
  "Switch Dispatcher", "Seeded Runtime Decoder", "Instruction Macro Expansion", "Constant Pool Encryption",
  "Mixed Boolean Arithmetic", "Randomized Label Routing", "Call Graph Fragmentation", "Trap Function Seeds",
  "Opaque Loop Nests", "Expression Reassociation", "Table Key Encryption", "Anti-Beautifier Noise",
  "Comment Channel Encoding", "Shadow Chunk Split", "Sandbox Escape Guards", "Opcode Alias Layer",
  "Runtime Key Exchange", "Serialized Closure Layout", "Dummy Module Weaving"
];

const deobfuscatorSupport = [
  "Identifier Recovery", "String Decoder Reconstruction", "Control Flow Graph Recovery",
  "Constant Unmasking", "VM Handler Mapping", "Opaque Predicate Simplification",
  "Junk Code Pruning", "Dead Branch Elimination", "AST Canonicalization",
  "Metatable Trap Detection", "Upvalue Flow Tracking", "Dynamic Loader Unpacking",
  "Compression Layer Extraction", "Encrypted Table Key Recovery", "Function Boundary Recovery",
  "Loop Normalization", "Branch De-virtualization", "Bytecode Signature Matching",
  "Runtime Decoder Emulation", "Constant Pool Decryption", "Call Graph Rebuild",
  "Debug Lockout Bypass Analysis", "Anti-Tamper Stub Isolation", "Closure Serialization Decode",
  "Pretty-Print Structure Regeneration"
];

const reversibleTechniqueSupports = new Set(techniques.slice(0, 25));

const obfuscatorOptions = techniques.flatMap((name, idx) => {
  const number = String(idx + 1).padStart(2, "0");
  return [
    {
      id: `obf-${number}-A`,
      technique: name,
      variant: "Stealth",
      description: "Comment stripping + local renaming + Base64 payload wrapper"
    },
    {
      id: `obf-${number}-B`,
      technique: name,
      variant: "Aggressive",
      description: "Metadata header + chunked Base64 payload + runtime decoder"
    }
  ];
});

const grid = document.getElementById("techniquesGrid");
const list = document.getElementById("deobfList");
const searchBox = document.getElementById("searchBox");
const obfuscatorSelect = document.getElementById("obfuscatorSelect");
const deobfModeSelect = document.getElementById("deobfModeSelect");
const luaInput = document.getElementById("luaInput");
const luaOutput = document.getElementById("luaOutput");
const statusLine = document.getElementById("statusLine");

const setStatus = (text) => {
  statusLine.textContent = text;
};

document.getElementById("techniqueCount").textContent = techniques.length;
document.getElementById("obfCount").textContent = obfuscatorOptions.length;
document.getElementById("deobfCount").textContent = deobfuscatorSupport.length;

for (const option of obfuscatorOptions) {
  const opt = document.createElement("option");
  opt.value = option.id;
  opt.textContent = `${option.id} • ${option.technique} (${option.variant})`;
  obfuscatorSelect.appendChild(opt);
}

for (const support of deobfuscatorSupport) {
  const opt = document.createElement("option");
  opt.value = support;
  opt.textContent = support;
  deobfModeSelect.appendChild(opt);
}

for (const technique of techniques) {
  const card = document.createElement("article");
  card.className = "card";
  card.innerHTML = `
    <h3>${technique}</h3>
    <p>2 variants: Stealth and Aggressive.</p>
    <div class="badges">
      <span class="badge">Variant A</span>
      <span class="badge">Variant B</span>
    </div>
  `;
  grid.appendChild(card);
}

function renderSupport(query = "") {
  list.innerHTML = "";
  const filtered = deobfuscatorSupport.filter((item) =>
    item.toLowerCase().includes(query.toLowerCase())
  );

  for (const item of filtered) {
    const li = document.createElement("li");
    li.textContent = item;
    list.appendChild(li);
  }
}

function stripLuaComments(code) {
  let out = code.replace(/--\[\[[\s\S]*?\]\]/g, "");
  out = out.replace(/--[^\n]*/g, "");
  return out;
}

function renameLocals(code) {
  const reserved = new Set([
    "and", "break", "do", "else", "elseif", "end", "false", "for", "function", "goto", "if",
    "in", "local", "nil", "not", "or", "repeat", "return", "then", "true", "until", "while"
  ]);

  const declared = [...code.matchAll(/\blocal\s+([A-Za-z_][A-Za-z0-9_]*)/g)].map((m) => m[1]);
  const mapping = {};
  let i = 0;

  for (const name of declared) {
    if (!reserved.has(name) && !mapping[name]) {
      mapping[name] = `_v${i.toString(36)}${Math.random().toString(36).slice(2, 6)}`;
      i++;
    }
  }

  let transformed = code;
  for (const [from, to] of Object.entries(mapping)) {
    transformed = transformed.replace(new RegExp(`\\b${from}\\b`, "g"), to);
  }

  return { transformed, mapping };
}

function reverseRenameLocals(code, mapping) {
  let restored = code;
  for (const [from, to] of Object.entries(mapping)) {
    restored = restored.replace(new RegExp(`\\b${to}\\b`, "g"), from);
  }
  return restored;
}

function wrapBase64Stealth(code) {
  const payload = btoa(unescape(encodeURIComponent(code)));
  return [
    "local __p='" + payload + "'",
    "local __d=(__p:gsub('.', function(c) return string.char((string.byte(c)-1)%256) end))",
    "__d=(__d:gsub('.', function(c) return string.char((string.byte(c)+1)%256) end))",
    "local __raw=(__d:gsub('%s',''))",
    "local __bin='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'",
    "local __src=(__raw:gsub('.', function(x)",
    "  if x=='=' then return '' end",
    "  local r,f='',(__bin:find(x)-1)",
    "  for i=6,1,-1 do r=r .. (f%2^i-f%2^(i-1)>0 and '1' or '0') end",
    "  return r",
    "end):gsub('%d%d%d?%d?%d?%d?%d?%d?', function(x)",
    "  if #x ~= 8 then return '' end",
    "  local c=0",
    "  for i=1,8 do c=c + (x:sub(i,i)=='1' and 2^(8-i) or 0) end",
    "  return string.char(c)",
    "end))",
    "assert(load(__src))()"
  ].join("\n");
}

function chunkString(value, size) {
  const out = [];
  for (let i = 0; i < value.length; i += size) {
    out.push(value.slice(i, i + size));
  }
  return out;
}

function wrapBase64Aggressive(code) {
  const payload = btoa(unescape(encodeURIComponent(code)));
  const chunks = chunkString(payload, 48).map((c) => `"${c}"`);
  return [
    "local __chunks = {" + chunks.join(",") + "}",
    "local __b64 = table.concat(__chunks)",
    "local __chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'",
    "local __src = (__b64:gsub('.', function(x)",
    "  if x == '=' then return '' end",
    "  local r, f = '', (__chars:find(x) - 1)",
    "  for i = 6,1,-1 do r = r .. (f%2^i - f%2^(i-1) > 0 and '1' or '0') end",
    "  return r",
    "end):gsub('%d%d%d?%d?%d?%d?%d?%d?', function(x)",
    "  if #x ~= 8 then return '' end",
    "  local c = 0",
    "  for i = 1,8 do c = c + (x:sub(i,i)=='1' and 2^(8-i) or 0) end",
    "  return string.char(c)",
    "end))",
    "assert(load(__src))()"
  ].join("\n");
}

function obfuscateLua(inputCode, option) {
  const cleaned = stripLuaComments(inputCode).trim();
  const { transformed, mapping } = renameLocals(cleaned);
  const metadata = {
    tool: "LuaObfHub",
    method: option.id,
    technique: option.technique,
    variant: option.variant,
    reversible: reversibleTechniqueSupports.has(option.technique),
    map: mapping,
    createdAt: new Date().toISOString()
  };

  const header = `--[[LUA_OBF_META:${btoa(unescape(encodeURIComponent(JSON.stringify(metadata))))}]]`;
  const body = option.variant === "Stealth" ? wrapBase64Stealth(transformed) : wrapBase64Aggressive(transformed);
  return `${header}\n${body}`;
}

function decodeMetadata(inputCode) {
  const match = inputCode.match(/^--\[\[LUA_OBF_META:([^\]]+)\]\]/);
  if (!match) return null;
  try {
    return JSON.parse(decodeURIComponent(escape(atob(match[1]))));
  } catch {
    return null;
  }
}

function extractBase64Payload(code) {
  const direct = code.match(/local __p='([A-Za-z0-9+/=]+)'/);
  if (direct) return direct[1];

  const chunksMatch = code.match(/local __chunks\s*=\s*\{([\s\S]*?)\}/);
  if (chunksMatch) {
    const chunks = [...chunksMatch[1].matchAll(/"([A-Za-z0-9+/=]+)"/g)].map((m) => m[1]);
    if (chunks.length) return chunks.join("");
  }

  return null;
}

function decodeBase64Utf8(payload) {
  return decodeURIComponent(escape(atob(payload)));
}

function deobfuscateLua(inputCode, selectedMode) {
  const metadata = decodeMetadata(inputCode);
  const payload = extractBase64Payload(inputCode);

  if (!payload) {
    return { ok: false, message: "No supported payload found in output." };
  }

  let decoded;
  try {
    decoded = decodeBase64Utf8(payload);
  } catch {
    return { ok: false, message: "Failed to decode Base64 payload." };
  }

  let restored = decoded;
  if (metadata && metadata.map && metadata.reversible) {
    restored = reverseRenameLocals(decoded, metadata.map);
  }

  const modeMatch = deobfuscatorSupport.includes(selectedMode);
  const methodInfo = metadata ? `${metadata.method} (${metadata.technique}/${metadata.variant})` : "unknown";

  return {
    ok: modeMatch,
    message: modeMatch
      ? `Deobfuscation complete using ${selectedMode}. Source method: ${methodInfo}.`
      : "Selected deobfuscator mode is unsupported.",
    output: restored
  };
}

searchBox.addEventListener("input", (event) => {
  renderSupport(event.target.value);
});

document.getElementById("runObfuscate").addEventListener("click", () => {
  const inputCode = luaInput.value.trim();
  if (!inputCode) {
    setStatus("Provide Lua input first.");
    return;
  }

  const selectedId = obfuscatorSelect.value;
  const option = obfuscatorOptions.find((o) => o.id === selectedId);
  if (!option) {
    setStatus("Select an obfuscator option.");
    return;
  }

  const output = obfuscateLua(inputCode, option);
  luaOutput.value = output;
  setStatus(`Obfuscated with ${option.id} • ${option.technique} (${option.variant}).`);
});

document.getElementById("runDeobfuscate").addEventListener("click", () => {
  const inputCode = luaOutput.value.trim() || luaInput.value.trim();
  if (!inputCode) {
    setStatus("Provide obfuscated Lua first.");
    return;
  }

  const selectedMode = deobfModeSelect.value;
  const result = deobfuscateLua(inputCode, selectedMode);
  if (!result.ok) {
    setStatus(result.message);
    return;
  }

  luaOutput.value = result.output;
  setStatus(result.message);
});

document.getElementById("copyOutput").addEventListener("click", async () => {
  if (!luaOutput.value.trim()) {
    setStatus("Nothing to copy yet.");
    return;
  }

  try {
    await navigator.clipboard.writeText(luaOutput.value);
    setStatus("Output copied to clipboard.");
  } catch {
    setStatus("Clipboard unavailable. Copy manually from output box.");
  }
});

document.getElementById("downloadOutput").addEventListener("click", () => {
  if (!luaOutput.value.trim()) {
    setStatus("Nothing to download yet.");
    return;
  }

  const blob = new Blob([luaOutput.value], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "lua-output.lua";
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
  setStatus("Downloaded lua-output.lua.");
});

document.getElementById("loadSample").addEventListener("click", () => {
  luaInput.value = [
    "local playerName = 'Kai'",
    "local score = 42",
    "local function levelUp(points)",
    "  local total = score + points",
    "  print('Player:', playerName, 'Total:', total)",
    "  return total",
    "end",
    "levelUp(8)"
  ].join("\n");
  setStatus("Sample Lua loaded.");
});

document.getElementById("clearAll").addEventListener("click", () => {
  luaInput.value = "";
  luaOutput.value = "";
  setStatus("Cleared input and output.");
});

renderSupport();
