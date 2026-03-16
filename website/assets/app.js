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

const grid = document.getElementById("techniquesGrid");
const list = document.getElementById("deobfList");
const searchBox = document.getElementById("searchBox");

document.getElementById("techniqueCount").textContent = techniques.length;
document.getElementById("obfCount").textContent = techniques.length * 2;
document.getElementById("deobfCount").textContent = deobfuscatorSupport.length;

for (const technique of techniques) {
  const card = document.createElement("article");
  card.className = "card";
  card.innerHTML = `
    <h3>${technique}</h3>
    <p>Two variants available for deployment.</p>
    <div class="badges">
      <span class="badge">Variant A: Stealth</span>
      <span class="badge">Variant B: Aggressive</span>
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

searchBox.addEventListener("input", (event) => {
  renderSupport(event.target.value);
});

renderSupport();
