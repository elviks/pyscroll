TIPS = [
    {
        "id": 1,
        "title": "Create tensors",
        "definition": "Constructing tensors is the first act of any PyTorch script. torch.tensor wraps Python lists or numpy arrays directly, while torch.zeros, torch.ones, torch.rand and torch.randn materialize filled tensors of a given shape in one call. Every input — images, text, signals — must first be converted into this uniform numeric container before any layer can touch it.",
        "example": "import torch\nx = torch.tensor([[1, 2], [3, 4]])   # from a nested list\nz = torch.zeros(2, 3)                # all zeros\nr = torch.randn(2, 3)                # standard-normal values",
        "usecase": "Converting imported data into tensors is the mandatory first line of every training pipeline — nothing else in PyTorch accepts raw Python data.",
        "category": "pytorch"
    },
    {
        "id": 2,
        "title": "dtype, shape, device",
        "definition": "Every tensor carries three facts that define how it lives in memory: dtype for numeric precision (float32, int64), shape for the size of each dimension and device for whether it sits on CPU or GPU. Inspecting all three at once is the fastest way to understand a tensor you did not create, and it clears up the majority of tensor errors.",
        "example": "x = torch.ones(4, 6, dtype=torch.float32)\nprint(x.dtype)    # torch.float32\nprint(x.shape)    # torch.Size([4, 6])\nprint(x.device)   # cpu",
        "usecase": "Debugging mismatches — most tensor errors are shape, dtype or device disagreements, and one print() of the three facts settles them.",
        "category": "pytorch"
    },
    {
        "id": 3,
        "title": "Move to GPU with .to()",
        "definition": "The .to() method migrates a tensor or an entire model to another device: passing the string 'cuda' moves work onto the GPU for fast kernels and 'cpu' brings it back. Because device is a property of the object, a whole network can be relocated with a single call — parameters, buffers and all — instead of piece by piece.",
        "example": "device = \"cuda\" if torch.cuda.is_available() else \"cpu\"\nmodel = model.to(device)   # move every parameter\nx = x.to(device)           # and the input too\nout = model(x)             # all on the same device",
        "usecase": "Training on GPU for speed where available, falling back to CPU on machines without CUDA — one guard line makes the whole script portable.",
        "category": "pytorch"
    },
    {
        "id": 4,
        "title": "Autograd: gradients for free",
        "definition": "Autograd is PyTorch's automatic differentiation engine. A tensor flagged with requires_grad=True records every operation applied to it in a graph; calling backward() then walks that graph and deposits the derivative of the output into each tensor's .grad attribute. Exact gradients arrive without a single hand-written derivative formula.",
        "example": "x = torch.tensor(3.0, requires_grad=True)\ny = x ** 2        # operations are recorded\ny.backward()      # computes d(y)/d(x)\nprint(x.grad)     # tensor(6.)",
        "usecase": "Every nn.Module trains through autograd — you write the forward pass and the engine produces the gradients that optimizers consume.",
        "category": "pytorch"
    },
    {
        "id": 5,
        "title": "Optimizer loop in 4 steps",
        "definition": "One training step is four calls in a fixed order: zero_grad() clears stale gradients from the previous batch, the forward pass runs the model and computes a loss, backward() populates fresh gradients and step() applies one weight update. Repeating these four lines for every batch is the universal training loop.",
        "example": "optimizer.zero_grad()          # clear old gradients\nloss = criterion(model(x), y)  # forward + loss\nloss.backward()                # populate gradients\noptimizer.step()               # one weight update",
        "usecase": "The reusable skeleton of every supervised training script — swap the model or loss in and the four-line core stays identical.",
        "category": "pytorch"
    },
    {
        "id": 6,
        "title": "nn.Module is the model class",
        "definition": "nn.Module is the base class of every network component. You subclass it, register layers as attributes inside __init__, and override forward() to define how input flows through them. The framework then tracks the parameters, moves them with .to(), saves them via state_dict() and switches train/eval modes automatically.",
        "example": "import torch.nn as nn\n\nclass Net(nn.Module):\n    def __init__(self):\n        super().__init__()\n        self.fc = nn.Linear(10, 1)\n\n    def forward(self, x):\n        return self.fc(x)\n\nnet = Net()",
        "usecase": "Encapsulating weights, layer structure and forward logic in one saveable, live-trainable object — the standard way to define any architecture.",
        "category": "pytorch"
    },
    {
        "id": 7,
        "title": "nn.Linear, the workhorse",
        "definition": "nn.Linear(in_features, out_features) implements a fully connected layer computing y = x·Wᵀ + b. It owns a weight matrix and a bias vector that optimizers update, and it accepts any input whose last dimension matches in_features while leaving the batch dimension untouched.",
        "example": "layer = nn.Linear(128, 64)\nout = layer(torch.randn(32, 128))   # (32, 64)\nprint(out.shape)                     # batch preserved, 64 features",
        "usecase": "The workhorse behind MLPs, classification heads and the final layer of countless architectures — wherever input features must mix into output features.",
        "category": "pytorch"
    },
    {
        "id": 8,
        "title": "Activations are functions",
        "definition": "Non-linearities such as ReLU, sigmoid and tanh live in torch.nn.functional (F.relu, F.sigmoid) or as layer objects (nn.ReLU). Applied pointwise to activations, they inject the non-linearity that lets stacked layers represent far more than one linear transform, so activation choice shapes training dynamics significantly.",
        "example": "import torch.nn.functional as F\nx = F.relu(hidden)          # clamp negatives to 0\np = torch.sigmoid(logits)   # squash to a 0-1 range",
        "usecase": "Without activations, deep networks collapse into a single linear transform — these functions are what make the depth actually useful.",
        "category": "pytorch"
    },
    {
        "id": 9,
        "title": "Loss functions",
        "definition": "torch.nn ships ready-made loss modules: MSELoss for regression, CrossEntropyLoss for multi-class classification (accepting raw logits, not probabilities), L1Loss and more. Each takes a prediction and a ground truth and returns a scalar that gradients flow through, so choosing the right one is a core modeling decision.",
        "example": "criterion = nn.CrossEntropyLoss()\nlogits = model(xb)               # (B, num_classes)\nloss = criterion(logits, yb)     # scalar tensor",
        "usecase": "The scalar that drives every parameter update — the loss encodes what being wrong costs, so it must match the task you optimize for.",
        "category": "pytorch"
    },
    {
        "id": 10,
        "title": "Optimizers: SGD and Adam",
        "definition": "Optimizers in torch.optim turn gradients into weight updates. SGD subtracts the gradient scaled by a learning rate, with optional momentum to smooth the path; Adam maintains per-parameter adaptive moments for faster, more robust convergence. You hand an optimizer model.parameters() and it updates exactly those tensors each step.",
        "example": "import torch.optim as optim\noptimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.9)\n# or\noptimizer = optim.Adam(model.parameters(), lr=1e-3)",
        "usecase": "Adam is the pragmatic default for most problems; SGD proves more controllable and generalizes well when you tune it deliberately.",
        "category": "pytorch"
    },
    {
        "id": 11,
        "title": "Dataset class",
        "definition": "torch.utils.data.Dataset is the interface for any training data: subclass it, implement __len__ to report the number of samples and __getitem__ to return sample i, and PyTorch's loading machinery handles the rest. A thin wrapper is enough to expose any source — files, DBs, APIs — to the DataLoader.",
        "example": "from torch.utils.data import Dataset\n\nclass MyData(Dataset):\n    def __len__(self):\n        return len(self.rows)\n\n    def __getitem__(self, i):\n        return torch.tensor(self.rows[i])",
        "usecase": "Images from folders, JSONL lines, CSV rows or database queries — any source with an index protocol becomes trainable through one small class.",
        "category": "pytorch"
    },
    {
        "id": 12,
        "title": "DataLoader batches it",
        "definition": "DataLoader(dataset, batch_size, shuffle, num_workers) wraps a Dataset and yields ready-made batches. It shuffles and samples indices, collects individual samples into stacked tensors and can prefetch in parallel worker processes so the GPU never idles waiting on disk or decoding.",
        "example": "from torch.utils.data import DataLoader\nloader = DataLoader(ds, batch_size=32, shuffle=True, num_workers=4)\nfor xb, yb in loader:\n    train_step(xb, yb)",
        "usecase": "Turning a Dataset into a stream of GPU-ready batches, with shuffle and parallel loading handled for you instead of hand-rolled slice logic.",
        "category": "pytorch"
    },
    {
        "id": 13,
        "title": "train() vs eval() mode",
        "definition": "model.train() enables data-dependent layers such as dropout and batch normalization, which behave differently for each sample; model.eval() disables them so inference becomes deterministic. Call the right one before each phase — forgetting eval() before validation is a classic source of mysteriously bad predictions.",
        "example": "model.train()   # before the training loop\n# ... train ...\nmodel.eval()    # before validation or inference",
        "usecase": "Getting repeatable, correct results from dropout and batchnorm at evaluation time — a one-line toggle that changes the layer numerics.",
        "category": "pytorch"
    },
    {
        "id": 14,
        "title": "torch.no_grad() for inference",
        "definition": "Wrapping inference in torch.no_grad() disables autograd graph-building for the whole block. Forward passes still allocate memory and do bookkeeping for gradients without it; with it, memory use drops sharply and predictions run faster — with identical results, because inference needs no gradients.",
        "example": "with torch.no_grad():\n    preds = model(xb)   # no graph built, low memory",
        "usecase": "Scoring validation sets or serving predictions without wasting memory on a graph nobody will backprop — a free speed-and-memory win.",
        "category": "pytorch"
    },
    {
        "id": 15,
        "title": "Save and load models",
        "definition": "torch.save(model.state_dict(), 'net.pt') stores a plain dict mapping each parameter name to its values, and load_state_dict(torch.load('net.pt')) restores them into an identically-defined model. Saving the whole model works too but is fragile across code changes — the state dict is the portable, robust choice.",
        "example": "torch.save(model.state_dict(), \"net.pt\")\nnew_model = Net()\nnew_model.load_state_dict(torch.load(\"net.pt\"))\nnew_model.eval()",
        "usecase": "Persisting trained weights to disk for later inference, deployment or fine-tuning — reload into a fresh copy of the same architecture.",
        "category": "pytorch"
    },
    {
        "id": 16,
        "title": "Conv2d for images",
        "definition": "nn.Conv2d(in_channels, out_channels, kernel_size) slides learned filter kernels over a spatial grid, producing feature maps. Because each filter is shared across the whole image, the layer learns local patterns — edges, textures — that generalize to any position, and padding lets it preserve spatial dimensions.",
        "example": "conv = nn.Conv2d(3, 16, kernel_size=3, padding=1)\nout = conv(torch.randn(8, 3, 32, 32))   # (8, 16, 32, 32)",
        "usecase": "Detecting local visual features anywhere in the image — the foundational layer of every CNN, from small classifiers to modern vision backbones.",
        "category": "pytorch"
    },
    {
        "id": 17,
        "title": "Pooling downsamples",
        "definition": "nn.MaxPool2d downsamples a feature map by sliding a window and keeping only its largest value. That shrinks spatial dimensions, cutting compute and memory in deeper layers, while the max operation preserves the strongest activations and gives the network a degree of tolerance to small shifts in the input.",
        "example": "pool = nn.MaxPool2d(2)                   # 2x2 window, stride 2\nout = pool(torch.randn(8, 16, 32, 32))  # (8, 16, 16, 16)",
        "usecase": "Progressively reducing image resolution so later layers see a wider context — for a fraction of the memory and compute.",
        "category": "pytorch"
    },
    {
        "id": 18,
        "title": "Flatten before the head",
        "definition": "nn.Flatten collapses every dimension after the batch into a single vector, turning feature maps of shape (B, C, H, W) into (B, C*H*W). It sits between convolutional feature extraction and a Linear classifier head, which expects a 2D input of samples and features.",
        "example": "x = torch.randn(8, 16, 8, 8)\nflat = nn.Flatten()(x)     # (8, 1024)\nout = classifier(flat)     # Linear head gets 2D input",
        "usecase": "Bridging the spatial feature maps of a CNN to the fully-connected head that produces the final class scores.",
        "category": "pytorch"
    },
    {
        "id": 19,
        "title": "Embeddings for discrete tokens",
        "definition": "nn.Embedding(vocab_size, embedding_dim) holds a lookup table that maps integer token ids to dense learnable vectors. Given a batch of indices it returns the corresponding rows — conceptually indexing a big matrix, but with gradient updates that slowly rearrange vectors so semantically similar tokens land nearby.",
        "example": "emb = nn.Embedding(1000, 64)\nvecs = emb(torch.tensor([3, 42, 500]))   # (3, 64)\nprint(vecs.shape)",
        "usecase": "Turning words, categories or user ids into real-valued vectors a model can compute with — the standard entry into NLP and recommender systems.",
        "category": "pytorch"
    },
    {
        "id": 20,
        "title": "stack vs cat",
        "definition": "torch.cat joins tensors along an existing dimension, like gluing image rows together; torch.stack places whole tensors side by side along a brand-new outer dimension. cat needs compatible shapes on the joined axis, while stack only requires equal shapes, so which one you want depends on the intended batch layout.",
        "example": "a = torch.zeros(2, 3)\nb = torch.ones(2, 3)\ntorch.cat([a, b], dim=0)    # (4, 3) — same dim, more rows\ntorch.stack([a, b])         # (2, 2, 3) — new dim in front",
        "usecase": "Concatenating padded sequences or feature rows (cat) versus assembling a batch from individual samples stored separately (stack).",
        "category": "pytorch"
    },
    {
        "id": 21,
        "title": "argmax for predictions",
        "definition": "torch.argmax(input, dim) returns the index of the largest value along that dimension. Reduced over the class axis of model output, it converts scores into a concrete predicted class. Because CrossEntropyLoss reads logits along the same axis, the reduction you use for loss matches the one you use for prediction.",
        "example": "logits = torch.tensor([[0.1, 0.7, 0.2],\n                       [0.9, 0.05, 0.05]])\nlabels = logits.argmax(dim=1)   # [1, 0]",
        "usecase": "Turning probability or logit output into a concrete class label for accuracy reports, top-k metrics or hard predictions at serving time.",
        "category": "pytorch"
    },
    {
        "id": 22,
        "title": "Broadcasting shapes",
        "definition": "PyTorch broadcasts operations when dimensions align: a (3,1) tensor combined with a (1,4) tensor produces (3,4) without copying data because size-1 dimensions stretch implicitly. Every elementwise operation follows these rules, so differently-shaped tensors combine concisely and at full memory efficiency.",
        "example": "a = torch.arange(3).reshape(3, 1)\nb = torch.arange(4).reshape(1, 4)\nprint((a + b).shape)   # (3, 4) — broadcast, no copy",
        "usecase": "Adding a per-row and a per-column bias to a whole matrix in one expression, or normalizing features against per-channel statistics.",
        "category": "pytorch"
    },
    {
        "id": 23,
        "title": "Reshape without copies",
        "definition": "view() reinterprets a contiguous tensor's data block as new dimensions without copying; reshape() does the same and copies only when needed to make data contiguous. permute() reorders the axes themselves and may require a following contiguous() call. Choosing correctly keeps memory cheap and layouts predictable.",
        "example": "x = torch.randn(2, 3, 4)\ny = x.view(2, 12)       # flatten, no copy\nz = x.permute(2, 0, 1)  # axes rearranged",
        "usecase": "Flattening feature maps for MLP heads or reordering channels into HWC for plotting and image libraries — all without duplicating memory.",
        "category": "pytorch"
    },
    {
        "id": 24,
        "title": "Seeds for reproducibility",
        "definition": "torch.manual_seed(n) fixes PyTorch's random draws, and setting the same seed in numpy and random pins the other streams. Initialization, data shuffling and split sampling all draw from these generators, so one seed value reproduces a full run on any machine — prerequisites for trustworthy experiments.",
        "example": "import random\nimport numpy as np\nimport torch\ntorch.manual_seed(42)\nnp.random.seed(42)\nrandom.seed(42)",
        "usecase": "Reproducing experiments — the same seed replays init, data order and results across team laptops and cluster nodes.",
        "category": "pytorch"
    },
    {
        "id": 25,
        "title": "Gradient clipping",
        "definition": "nn.utils.clip_grad_norm_(params, max_norm) rescales the total gradient norm so it stays under a cap before the optimizer applies it. Where gradients explode — common in recurrent networks — updates remain bounded and training stays stable instead of degenerating into NaN weights.",
        "example": "loss.backward()\nnn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)\noptimizer.step()",
        "usecase": "Stabilizing RNN/LSTM training where long-sequence gradients balloon — clipping tames the updates that would otherwise wreck the weights.",
        "category": "pytorch"
    },
    {
        "id": 26,
        "title": "Train/validation split",
        "definition": "random_split(dataset, lengths) carves one dataset into several slices deterministically when given a seeded generator. Each slice remains a Dataset, so DataLoaders wrap them independently. Holding out validation data that never enters the training loop is the only honest way to measure generalization.",
        "example": "from torch.utils.data import random_split\ntr, va = random_split(ds, [0.8, 0.2],\n                      generator=torch.Generator().manual_seed(1))",
        "usecase": "Separating a fixed holdout set once and only ever training on the rest — the guardrail against optimistic, memorized metrics.",
        "category": "pytorch"
    },
    {
        "id": 27,
        "title": "Learning rate scheduling",
        "definition": "Schedulers in optim.lr_scheduler reduce the learning rate over time. StepLR decays it by a factor every fixed number of epochs, CosineAnnealingLR follows a smooth cosine curve and ReduceLROnPlateau shrinks it when a monitored metric stalls. Each guides the optimizer from broad exploration into fine settling.",
        "example": "sched = optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.5)\nfor epoch in range(30):\n    train(...)\n    sched.step()",
        "usecase": "Large steps explore early, systematically smaller steps refine late — the schedule is what lets a model actually land in a minimum.",
        "category": "pytorch"
    },
    {
        "id": 28,
        "title": "Dropout, an easy regularizer",
        "definition": "nn.Dropout(p) randomly zeroes a fraction p of activations on each training pass, forcing the network never to rely on any single neuron. At eval mode the layer becomes an identity, so deployed models use their full capacity. It is one of the cheapest effective defenses against overfitting.",
        "example": "self.drop = nn.Dropout(0.2)\n\n# in forward:\nx = self.fc1(x)\nx = self.drop(x)   # active in train, identity in eval",
        "usecase": "Reducing overfit on small datasets — regularizing by making the network robust to missing neurons instead of memorizing their presence.",
        "category": "pytorch"
    },
    {
        "id": 29,
        "title": "Model summary shape check",
        "definition": "Running a dummy input through the model before real training — build a tensor of the expected input shape and print the output shape. Any wiring mistake, such as a wrong dimension or a missing flatten, fails in seconds here rather than three hours into a run, saving expensive GPU cycles.",
        "example": "x = torch.randn(1, 3, 32, 32)\nwith torch.no_grad():\n    print(model(x).shape)   # unexpected? fix layers now",
        "usecase": "Validating the architecture against your exact input format before committing hours of GPU time to a training run.",
        "category": "pytorch"
    },
    {
        "id": 30,
        "title": "Mixed precision for speed",
        "definition": "torch.autocast('cuda') runs eligible operations in float16 while keeping critical ones in float32, and GradScaler multiplies the loss first so tiny float16 gradients never underflow to zero. Together they exploit tensor cores for roughly double throughput on modern GPUs, with accuracy usually within noise of fp32.",
        "example": "with torch.autocast(\"cuda\"):\n    loss = criterion(model(x), y)\nscaler.scale(loss).backward()\nscaler.step(optimizer)\nscaler.update()",
        "usecase": "Faster epochs and bigger batches on tensor-core GPUs — the standard speedup for any modern, large training script.",
        "category": "pytorch"
    },
    {
        "id": 31,
        "title": "LSTM for sequences",
        "definition": "nn.LSTM processes sequences through recurrent cells with gated hidden memory. Given input of shape (batch, seq_len, features) — with batch_first=True — it emits the full output sequence plus the final hidden and cell states. Those gates let the cell retain relevant context across long spans: the classic sequence-learning unit.",
        "example": "lstm = nn.LSTM(input_size=8, hidden_size=16,\n               num_layers=2, batch_first=True)\nout, (h, c) = lstm(torch.randn(32, 20, 8))\nprint(out.shape)   # (32, 20, 16)",
        "usecase": "Time series forecasting, text modeling and audio where order and long-range dependencies decide the answer.",
        "category": "pytorch"
    },
    {
        "id": 32,
        "title": "cuda guard everywhere",
        "definition": "Repeatedly checking torch.cuda.is_available() everywhere is noise; instead compute the device string once, then route the model and every batch through .to(device). All tensors land on the same device and one script runs unchanged on a GPU server or a laptop without CUDA.",
        "example": "device = \"cuda\" if torch.cuda.is_available() else \"cpu\"\nmodel.to(device)\nfor xb, yb in loader:\n    loss = criterion(model(xb.to(device)), yb.to(device))",
        "usecase": "Portable training code that stays identical across machines — the device decision is centralized instead of scattered through the script.",
        "category": "pytorch"
    },
    {
        "id": 33,
        "title": "Gradient tape for custom training",
        "definition": "torch.autograd.grad(outputs, inputs) computes gradients of a function directly and returns them as values, without a model or optimizer loop. That fits research-style training where the derivative itself is what you need — adversarial perturbations, GAN losses or meta-learning — rather than a stored .grad.",
        "example": "from torch.autograd import grad\nx = torch.tensor(2.0, requires_grad=True)\ny = x ** 3\ng = grad(y, x)[0]    # 12.0 — the derivative, as a value",
        "usecase": "Research and custom training schemes that harvest raw gradients in the middle of a computation instead of waiting for a loss.",
        "category": "pytorch"
    },
    {
        "id": 34,
        "title": "Batch size tradeoffs",
        "definition": "Batch size is a genuine hyperparameter. Larger batches average more samples per update, giving smoother gradients and better hardware utilization but using more memory; smaller batches update far more often with noisier estimates, typically needing a re-tuned learning rate. It trades throughput against stability and generalization.",
        "example": "loader = DataLoader(ds, batch_size=64)    # modest\nloader = DataLoader(ds, batch_size=256)   # if VRAM allows",
        "usecase": "Tuning throughput and gradient stability — raising batch size is the first lever when a GPU sits underutilized.",
        "category": "pytorch"
    },
    {
        "id": 35,
        "title": "Whose .grad? A debug check",
        "definition": "A parameter whose .grad stayed None means the backward pass never produced a gradient for it — the signature of wiring bugs such as layers excluded from the graph or a loss that never touches them. Iterating named_parameters() and reporting the Nones pinpoints exactly where the chain breaks.",
        "example": "for name, p in model.named_parameters():\n    if p.grad is None:\n        print(\"no gradient for\", name)",
        "usecase": "Debugging frozen-by-accident layers or loss paths that never reach part of the model after a stalled loss or NaN blow-up.",
        "category": "pytorch"
    },
    {
        "id": 36,
        "title": "Tensors are numpy-aware",
        "definition": ".numpy() exports a CPU tensor's data to a NumPy array that shares its memory, and torch.from_numpy() imports a NumPy array with zero copies. The two libraries exchange data in O(1) — so pipelines can do preprocessing in pandas or NumPy and hand arrays straight to CUDA-capable tensors.",
        "example": "np_x = x.cpu().numpy()                # torch -> numpy, shared memory\ntorch_x = torch.from_numpy(np_x)      # numpy -> torch, no copy",
        "usecase": "Blending NumPy or pandas preprocessing with torch training — data crosses the boundary without a single duplication.",
        "category": "pytorch"
    },
    {
        "id": 37,
        "title": "nn.Sequential for flat nets",
        "definition": "nn.Sequential chains layers in order and calls them sequentially on whatever input it receives. Straight-line models — MLPs and simple CNNs — need no custom forward(), so they're declared in one compact block. Branching architectures outgrow it, at which point a hand-written nn.Module takes over.",
        "example": "model = nn.Sequential(\n    nn.Linear(10, 64),\n    nn.ReLU(),\n    nn.Linear(64, 2),\n)\nprint(model(torch.randn(4, 10)).shape)   # (4, 2)",
        "usecase": "Compact declaration of flat, strictly-stacked networks — the model reads top to bottom, exactly as data flows through it.",
        "category": "pytorch"
    },
    {
        "id": 38,
        "title": "Weight init matters",
        "definition": "nn.init ships standard initializers — kaiming_uniform_, xavier_uniform_ and friends — that set weights to values scale-aware for the activation that follows. Applied via model.apply() right after construction, they give a network a healthy starting geometry instead of random-large or random-degenerate weights.",
        "example": "def init_weights(m):\n    if isinstance(m, nn.Linear):\n        nn.init.kaiming_uniform_(m.weight)\n\nmodel.apply(init_weights)",
        "usecase": "Avoiding vanishing or exploding gradients from the very first batch — good initialization is cheap insurance for every new architecture.",
        "category": "pytorch"
    },
    {
        "id": 39,
        "title": "Top-k accuracy",
        "definition": "torch.topk(logits, k, dim=1) returns the k largest values and their indices per row. Comparing those index sets against the true label measures top-k accuracy — a metric common in large labeled tasks where the correct answer sitting near the top still counts as a reasonable prediction.",
        "example": "top5 = torch.topk(logits, k=5, dim=1).indices          # (B, 5)\ncorrect = (top5 == labels.unsqueeze(1)).any(dim=1).float().mean()\nprint(\"top-5 acc:\", correct.item())",
        "usecase": "ImageNet-style evaluation and retrieval ranking, where near-miss candidates carry signal even when they are not the argmax.",
        "category": "pytorch"
    },
    {
        "id": 40,
        "title": "Freeze layers for fine-tuning",
        "definition": "Transfer learning in three lines: set requires_grad=False on a pretrained backbone's parameters, hand the optimizer only the fresh head's parameters, and train. Frozen weights keep their learned features while the head adapts to your data — and backprop never spends compute on the frozen base.",
        "example": "for p in model.features.parameters():\n    p.requires_grad = False\noptimizer = optim.Adam(model.head.parameters(), lr=1e-3)",
        "usecase": "Reusing a strong pretrained vision or language backbone on a small custom dataset without washing out its features.",
        "category": "pytorch"
    },
    {
        "id": 41,
        "title": "Checkpoint resume training",
        "definition": "A checkpoint bundles the model's state_dict, the optimizer's state_dict, the epoch counter and best metrics into one dict saved to disk. Reloading restores training to the exact moment — learning curves, momentum moments and scheduler state included — so a crash costs at most one save interval.",
        "example": "ckpt = {\n    \"model\": model.state_dict(),\n    \"opt\": optimizer.state_dict(),\n    \"epoch\": epoch,\n}\ntorch.save(ckpt, \"ckpt.pt\")",
        "usecase": "Resuming from epoch 47 after a spotty job rather than restarting from zero — the survival plan for long training schedules.",
        "category": "pytorch"
    },
    {
        "id": 42,
        "title": "torch.max vs argmax",
        "definition": "torch.max(input, dim) returns both the largest values and their indices along that dimension as a named tuple; argmax returns only the indices. When predictions need the winning class and its confidence together, one call yields both — and argmax stays the leaner read when only the class matters.",
        "example": "vals, idx = torch.max(scores, dim=1)\n# vals: best confidence per row, idx: its class\npred, conf = idx, vals",
        "usecase": "Returning the predicted class and model confidence together — exactly what API responses and human-readable results want.",
        "category": "pytorch"
    },
    {
        "id": 43,
        "title": "Device mismatch errors",
        "definition": "Combining a CUDA tensor with a CPU tensor raises a RuntimeError stating that devices differ. The fix is a habit: route every tensor and model through a single device variable via .to(device) at each boundary, so nothing from another device ever reaches the operation.",
        "example": "device = \"cuda\" if torch.cuda.is_available() else \"cpu\"\na = a.to(device)\nb = b.to(device)\nc = a + b   # RuntimeError if devices differ",
        "usecase": "The most frequent beginner error in PyTorch — a three-line routing habit eliminates the whole class of failures.",
        "category": "pytorch"
    },
    {
        "id": 44,
        "title": "gain a feel for in-place vs copy",
        "definition": "Functions ending in an underscore, like relu_() or add_(), mutate the tensor instead of returning a new one. They save memory on huge activations, but applied to a leaf that requires gradients they can disturb autograd's graph — so they belong on intermediate results you will discard.",
        "example": "x = torch.randn(3)\nx.relu_()    # modifies x in place, no copy\nx.add_(1.0)\nprint(x)",
        "usecase": "Saving memory on large intermediate tensors where the original value is no longer needed after the operation.",
        "category": "pytorch"
    },
    {
        "id": 45,
        "title": "Mean reduction across dims",
        "definition": "tensor.mean(dim=k) averages along dimension k, removing it from the result's shape; keepdim=True keeps that axis as size 1. Collapsing dimensions this way is how you produce per-channel statistics or normalize batch features before they flow into the next layer.",
        "example": "x = torch.randn(2, 3)\nrow = x.mean(dim=1, keepdim=True)   # (2, 1)\ncol = x.mean(dim=0)                 # (3,)",
        "usecase": "Computing channel means, batch statistics and per-sample normalizations — the reductions that standardize features before a model sees them.",
        "category": "pytorch"
    },
    {
        "id": 46,
        "title": "Squeeze and unsqueeze",
        "definition": "squeeze(dim) removes a dimension of size 1 and unsqueeze(dim) inserts a new dimension of size 1. They adjust a tensor's rank — adding a batch axis for single-sample inference, stripping an axis after a model — without touching values or the ordering of the data. Tiny shape surgery for matching interfaces.",
        "example": "x = torch.randn(3, 1, 4)\nx = x.squeeze(1)     # (3, 4) — drop size-1 dim\nx = x.unsqueeze(0)   # (1, 3, 4) — add batch axis",
        "usecase": "Making one sample look like a batch to a model, or reshaping to match a loss that expects an extra axis.",
        "category": "pytorch"
    },
    {
        "id": 47,
        "title": "Cosine similarity for comparisons",
        "definition": "F.cosine_similarity(a, b, dim) measures the angle between vectors: 1 for identical direction, 0 for orthogonal, -1 for opposite — regardless of magnitude. Compared this way, embeddings merge semantic ranking with scale robustness, so bigger vectors do not automatically win.",
        "example": "from torch.nn.functional import cosine_similarity\nsim = cosine_similarity(vec_query, candidates, dim=-1)\nbest = sim.argmax()   # most similar candidate",
        "usecase": "Semantic search over embedding stores — retrieval, deduplication and matching where direction encodes meaning better than distance.",
        "category": "pytorch"
    },
    {
        "id": 48,
        "title": "Early stopping wins runs",
        "definition": "Track the best validation loss; when it keeps failing to improve for N epochs, stop training and restore the best weights. Long runs drift from optimizing training fit into memorizing noise, and validation is the ground truth that catches — and then reverses — exactly that drift.",
        "example": "if val_loss < best_loss:\n    best_loss = val_loss\n    torch.save(model.state_dict(), \"best.pt\")\n    patience = 0\nelse:\n    patience += 1\n    if patience > 5:\n        break   # load best.pt and finish",
        "usecase": "Automatic termination the moment generalization stops improving — saves GPU hours and keeps the strongest weights on disk.",
        "category": "pytorch"
    },
    {
        "id": 49,
        "title": "Grad accumulation",
        "definition": "Accumulating gradients fakes a bigger batch: keep calling backward() over several mini-batches, dividing the loss by the accumulation count, and only call step() and zero_grad() every N steps. The optimizer then effectively sees the average of N gradients — an effective batch N times the physical one.",
        "example": "loss = loss / accum_steps\nloss.backward()\nif (i + 1) % accum_steps == 0:\n    optimizer.step()\n    optimizer.zero_grad()",
        "usecase": "Training with batch 1024 on a GPU that only fits 128 — big-batch dynamics from small physical batches.",
        "category": "pytorch"
    },
    {
        "id": 50,
        "title": "Distribution sanity check",
        "definition": "Watch tensor statistics while training: NaN or inf values in outputs mean something exploded numerically. A cheap detector — torch.isnan(activations).any() — raised every few steps catches the failure within minutes, instead of after hours of a silently dead loss curve.",
        "example": "with torch.no_grad():\n    out = model(x.float())\n    if torch.isnan(out).any() or torch.isinf(out).any():\n        raise RuntimeError(\"Numerical blow-up detected\")",
        "usecase": "Catching exploding or vanishing gradients the moment they happen — before a long overnight run quietly returns garbage.",
        "category": "pytorch"
    }
]
