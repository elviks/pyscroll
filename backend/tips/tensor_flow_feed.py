TIPS = [
    {
        "id": 1,
        "title": "Constants and Variables",
        "definition": "tf.constant creates an immutable value — fixed configuration or literals that never change — while tf.Variable creates a mutable, trainable value whose assign and assign_add methods update it in place. In any TensorFlow program the split is crisp: constants describe the problem, variables hold the things that learning changes.",
        "example": "import tensorflow as tf\nc = tf.constant(3.0)      # immutable\nv = tf.Variable(0.0)      # mutable, trainable\nv.assign_add(1.0)\nprint(v.numpy())          # 1.0",
        "usecase": "Fixed config sits in constants while model weights live in Variables — the objects optimizers update on every training step.",
        "category": "tensorflow"
    },
    {
        "id": 2,
        "title": "The Sequential model",
        "definition": "tf.keras.Sequential stacks layers in a straight line — each layer feeds the next, in the order declared. It is the fastest route to a working network for feed-forward architectures, since the model object itself handles fitting, prediction and evaluation without any custom wiring.",
        "example": "model = tf.keras.Sequential([\n    tf.keras.layers.Dense(64, activation=\"relu\"),\n    tf.keras.layers.Dense(10, activation=\"softmax\"),\n])",
        "usecase": "Feed-forward nets for tabular data, small image classifiers and quick experiments — declare, compile, fit and you are done.",
        "category": "tensorflow"
    },
    {
        "id": 3,
        "title": "Dense layers",
        "definition": "Dense(units, activation) is a fully connected layer: every input neuron connects to every output neuron, with an optional activation applied right after. Stacking these layers is how models build non-linear capacity, and the layer's weights are precisely what training adjusts to reduce loss.",
        "example": "layer = tf.keras.layers.Dense(32, activation=\"relu\")\nout = layer(tf.zeros((16, 8)))   # (16, 32)",
        "usecase": "The basic building block of most Keras models — stacking Dense layers adds capacity, and the pattern scales from tabular to deep.",
        "category": "tensorflow"
    },
    {
        "id": 4,
        "title": "Compile: optimizer + loss",
        "definition": "model.compile wires the optimizer, the loss function and the metrics a model reports — the configuration that defines how learning happens. Nothing trains until compile() runs, and most accuracy questions are really asked of the loss: it is the scalar the optimizer minimizes.",
        "example": "model.compile(\n    optimizer=\"adam\",\n    loss=\"sparse_categorical_crossentropy\",\n    metrics=[\"accuracy\"],\n)",
        "usecase": "Choosing how the model learns — the optimizer drives updates, the loss scores failure and metrics translate it into human numbers.",
        "category": "tensorflow"
    },
    {
        "id": 5,
        "title": "fit() trains it",
        "definition": "model.fit(x_train, y_train, epochs, batch_size, validation_split) runs the whole training loop internally: batching, shuffling, backprop and per-epoch validation, all for you. The loop is deterministic once seeds are fixed, and fit() returns a History object carrying every metric per epoch.",
        "example": "history = model.fit(\n    x_train, y_train,\n    epochs=10, batch_size=32,\n    validation_split=0.2,\n)",
        "usecase": "Training without writing a single gradient or loop line — fit() hides the machinery and returns curves to inspect afterward.",
        "category": "tensorflow"
    },
    {
        "id": 6,
        "title": "The Functional API",
        "definition": "Functional models wire layers by calling them on inputs — layer(input) returns a tensor, and tensors chain into a graph. Unlike Sequential's straight line, this supports branching, skip connections and multiple inputs or outputs, so any architecture expressible as a graph becomes a Model.",
        "example": "inp = tf.keras.Input(shape=(8,))\nx = tf.keras.layers.Dense(32, activation=\"relu\")(inp)\nout = tf.keras.layers.Dense(1)(x)\nmodel = tf.keras.Model(inp, out)",
        "usecase": "Non-linear graphs like ResNets, encoder-decoders and multi-task models — Functional is the escape hatch Sequential can't offer.",
        "category": "tensorflow"
    },
    {
        "id": 7,
        "title": "Input shapes matter",
        "definition": "Input(shape=...) or input_shape in the first layer declares the per-sample tensor shape a model expects, leaving the batch dimension implicit. The declaration both documents the contract and lets shape errors surface at construction time rather than as a cryptic failure deep inside the first fit().",
        "example": "model = tf.keras.Sequential([\n    tf.keras.layers.Input(shape=(28, 28)),\n    tf.keras.layers.Flatten(),\n])",
        "usecase": "Shape mismatches fail on the first fit(); declaring input shapes early surfaces those mismatches the moment the model is built.",
        "category": "tensorflow"
    },
    {
        "id": 8,
        "title": "Normalize before training",
        "definition": "Normalization layers (or manual scaling) pull every feature into a comparable range before it reaches the network. Models optimize much more reliably when input distributions are well-behaved, so a single adapt() on training data is often the difference between an exploding loss and steady convergence.",
        "example": "from tensorflow.keras import layers\nnorm = layers.Normalization(axis=-1)\nnorm.adapt(x_train)          # learn stats from data\nmodel = tf.keras.Sequential([norm, layers.Dense(64, activation=\"relu\")])",
        "usecase": "Tabular data where income is in thousands and age in decades — normalize before the Dense layers or the scale dominates learning.",
        "category": "tensorflow"
    },
    {
        "id": 9,
        "title": "Dropout in Keras",
        "definition": "Dropout(rate) randomly deactivates a fraction of neurons on every training pass, forcing the network never to depend on any single unit. During evaluation the layer becomes inert, so full capacity returns at inference. It is one of the cheapest regularizers Keras ships.",
        "example": "model = tf.keras.Sequential([\n    layers.Dense(128, activation=\"relu\"),\n    layers.Dropout(0.2),\n    layers.Dense(10, activation=\"softmax\"),\n])",
        "usecase": "Regularizing small-data models against memorizing noise — the standard mid-network defense against overfitting.",
        "category": "tensorflow"
    },
    {
        "id": 10,
        "title": "Convnets in Keras",
        "definition": "Conv2D learns filter kernels that slide over the spatial grid, producing feature maps of local patterns; MaxPooling2D downsamples them, shrinking compute while preserving the strongest responses. Followed by Flatten and Dense, this trio is the heart of every convolutional classifier.",
        "example": "tf.keras.Sequential([\n    layers.Conv2D(32, (3, 3), activation=\"relu\", input_shape=(28, 28, 1)),\n    layers.MaxPooling2D(2),\n    layers.Flatten(),\n    layers.Dense(10, activation=\"softmax\"),\n])",
        "usecase": "Image classification at any scale — the same pattern powers everything from small photo datasets to ImageNet-grade models.",
        "category": "tensorflow"
    },
    {
        "id": 11,
        "title": "Callbacks hook the loop",
        "definition": "Callbacks are objects Keras invokes at epoch and batch boundaries, letting you intervene without editing the loop. EarlyStopping ends runs that stop improving, ModelCheckpoint saves weights at the best epoch, and TensorBoard logs curves — the three cover most practical training automation.",
        "example": "from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint\ncb = [\n    EarlyStopping(patience=3),\n    ModelCheckpoint(\"best.keras\", save_best_only=True),\n]",
        "usecase": "Automating patience-based stopping and persisting the best weights mid-run — training that polices itself.",
        "category": "tensorflow"
    },
    {
        "id": 12,
        "title": "Save a Keras model",
        "definition": "model.save('model.keras') writes architecture, weights, optimizer state and configuration into one self-contained file. load_model restores the exact model — trained state included — so a saved file is a complete artifact that can resume training or serve predictions on another machine.",
        "example": "model.save(\"model.keras\")\nrestored = tf.keras.models.load_model(\"model.keras\")\nrestored.evaluate(x_test, y_test)",
        "usecase": "Deploying to servers, resuming after a machine restart or sharing a finished model — one file carries the entire artifact.",
        "category": "tensorflow"
    },
    {
        "id": 13,
        "title": "Transfer learning with pretrained nets",
        "definition": "Loading a pretrained backbone such as ResNet50 — with include_top=False to drop its classifier — and capping it with fresh layers reuses features learned on ImageNet. Frozen during the first phase, the base extracts general visual features while only the new head trains on your data.",
        "example": "base = tf.keras.applications.ResNet50(include_top=False, input_shape=(224, 224, 3))\nbase.trainable = False\nmodel = tf.keras.Sequential([\n    base,\n    layers.GlobalAveragePooling2D(),\n    layers.Dense(10),\n])",
        "usecase": "Strong classifiers from tiny datasets by reusing ImageNet features — transfer learning is the shortcut to production vision models.",
        "category": "tensorflow"
    },
    {
        "id": 14,
        "title": "tf.data pipelines",
        "definition": "tf.data.Dataset pipelines chain declarative transformations — from_tensor_slices from arrays, then shuffle, batch and prefetch — evaluated lazily as training consumes them. prefetch(AUTOTUNE) starts fetching the next batch while the current one computes, hiding I/O behind the GPU and keeping it fed.",
        "example": "ds = tf.data.Dataset.from_tensor_slices((x, y))\nds = ds.shuffle(1000).batch(32).prefetch(tf.data.AUTOTUNE)",
        "usecase": "Feeding huge datasets efficiently — prefetch hides data-loading behind compute, so training never waits on disk.",
        "category": "tensorflow"
    },
    {
        "id": 15,
        "title": "Tokenization for text",
        "definition": "TextVectorization maps raw strings to integer token ids: it builds a vocabulary with adapt(), then encodes new text with the same mapping, padding or truncating to a fixed length. Text becomes a numeric sequence a model can embed — the canonical passage from words to tensors.",
        "example": "vec = tf.keras.layers.TextVectorization(max_tokens=10000)\nvec.adapt(texts)                    # learns vocab from data\nids = vec([\"hello world\"]).numpy()  # integer ids",
        "usecase": "Text classification, chat intent and sentiment models starting from raw strings — vocabulary building and encoding in one layer.",
        "category": "tensorflow"
    },
    {
        "id": 16,
        "title": "Embeddings in Keras",
        "definition": "Embedding(vocab_size, dim) is a lookup table: each integer token id indexes a dense learnable vector. Training nudges those vectors so similar tokens land close together in the embedding space, turning discrete ids into distributions a network can actually compute with.",
        "example": "emb = tf.keras.layers.Embedding(10000, 32)\nout = emb(tf.constant([3, 42, 999]))   # (3, 32) vectors",
        "usecase": "Words, products or users become vectors before recurrent or attention layers run — the universal input stage of NLP and recommender models.",
        "category": "tensorflow"
    },
    {
        "id": 17,
        "title": "Custom training loop with GradientTape",
        "definition": "GradientTape records every operation inside its block, then tape.gradient(loss, trainable_variables) computes the derivatives and apply_gradients pushes them into the weights. When fit() cannot express your training scheme — adversarial losses, nested updates, custom schedules — this is the escape hatch that exposes the full loop.",
        "example": "with tf.GradientTape() as tape:\n    loss = loss_fn(model(x, training=True), y)\ngrads = tape.gradient(loss, model.trainable_variables)\noptimizer.apply_gradients(zip(grads, model.trainable_variables))",
        "usecase": "GANs, reinforcement learning and novel training schemes fit() can't express — full control over each gradient step.",
        "category": "tensorflow"
    },
    {
        "id": 18,
        "title": "tf.function speeds loops",
        "definition": "@tf.function compiles a Python function into a TensorFlow graph, tracing it once and executing optimized kernels — often orders of magnitude faster for per-op Python overhead. Just decorate and call; the first call traces, later calls run the graph.",
        "example": "@tf.function\ndef predict(x):\n    return model(x, training=False)",
        "usecase": "Inference hot loops and research code where per-op Python overhead dominates — one decorator turns eager Python into graph execution.",
        "category": "tensorflow"
    },
    {
        "id": 19,
        "title": "TensorBoard callbacks",
        "definition": "The TensorBoard callback logs losses, metrics, histograms and even model graphs to a directory as training runs. Point the tensorboard CLI at that logdir and the browser shows live curves — the standard way to watch a model train without hand-plotting.",
        "example": "tb = tf.keras.callbacks.TensorBoard(log_dir=\"logs\")\nmodel.fit(x, y, epochs=20, callbacks=[tb])\n# then at the terminal: tensorboard --logdir logs",
        "usecase": "Watching loss curves, metric trends and histograms live — and sharing them with teammates — without a single manual plot.",
        "category": "tensorflow"
    },
    {
        "id": 20,
        "title": "LR scheduling built in",
        "definition": "tf.keras.optimizers.schedules returns a callable that replaces a fixed learning rate: ExponentialDecay shrinks it by a factor every N steps, and ReduceLROnPlateau watches a metric and halves the rate when it stalls. The schedule object plugs straight into any optimizer.",
        "example": "lr = tf.keras.optimizers.schedules.ExponentialDecay(1e-2, 1000, 0.9)\noptimizer = tf.keras.optimizers.Adam(lr)",
        "usecase": "Fast exploration at a high rate, then systematic decay — the schedule is built in so convergence comes for free.",
        "category": "tensorflow"
    },
    {
        "id": 21,
        "title": "model.summary() keeps you honest",
        "definition": "summary() prints every layer with its output shape and parameter count, plus the total trainable budget. A single glance confirms that the flatten is where you think it is, the head has the right units, and no layer doubled in parameters by accident.",
        "example": "model.summary()\n# Layer (type)    Output Shape     Param #\n# dense (Dense)   (None, 64)       576",
        "usecase": "Debugging architectures before a long training run commits you to them — the 2-second wiring sanity check.",
        "category": "tensorflow"
    },
    {
        "id": 22,
        "title": "Weights are configurable",
        "definition": "get_weights() returns a layer's weight and bias matrices as plain numpy arrays; set_weights() pushes arrays back in. That direct access makes weight surgery trivial — rescaling, initialization experiments, or moving numbers between identically-shaped architectures.",
        "example": "w = layer.get_weights()\nlayer.set_weights([arr * 0.5 for arr in w])   # halve the weights",
        "usecase": "Custom init, weight surgery or porting weights between identical architectures — direct, numpy-level control of parameters.",
        "category": "tensorflow"
    },
    {
        "id": 23,
        "title": "RNN layers for sequences",
        "definition": "LSTM and GRU layers process ordered data step by step, carrying internal state so earlier elements inform later ones. Fed embedded token ids or raw time steps, they compress the whole sequence into a context vector — the classic choice for text and time series.",
        "example": "tf.keras.Sequential([\n    layers.Embedding(10000, 32),\n    layers.LSTM(64),\n    layers.Dense(1, activation=\"sigmoid\"),\n])",
        "usecase": "Sentiment, forecasting and sequence classification where position and long-range context matter more than any single value.",
        "category": "tensorflow"
    },
    {
        "id": 24,
        "title": "BatchNormalization stabilizes",
        "definition": "BatchNormalization re-centers and rescales layer inputs using the statistics of the current batch, then lets the network learn its own scale and shift. That normalization during training keeps activations in a healthy range, which typically allows higher learning rates and faster, more stable convergence.",
        "example": "tf.keras.Sequential([\n    layers.Dense(64),\n    layers.BatchNormalization(),\n    layers.Activation(\"relu\"),\n])",
        "usecase": "Deep networks with exploding or vanishing gradients — batch norm calms the training dynamics and unlocks bigger learning rates.",
        "category": "tensorflow"
    },
    {
        "id": 25,
        "title": "predict vs predict_on_batch",
        "definition": "model.predict handles batching for you — given any dataset it chunks internally and returns all predictions; predict_on_batch runs a single batch directly with no splitting. Serving code that already manages its own chunk sizes often wants the latter; everything else should just call predict.",
        "example": "preds = model.predict(big_ds, verbose=0)   # auto-batched over the whole set\npreds = model.predict_on_batch(x_batch)     # exactly this one batch",
        "usecase": "Tailoring inference to batch sizes in serving code, versus hands-free prediction on any dataset in analysis scripts.",
        "category": "tensorflow"
    },
    {
        "id": 26,
        "title": "Binary vs multi-class losses",
        "definition": "BinaryCrossentropy suits two-class targets, typically with a sigmoid output; SparseCategoricalCrossentropy handles multi-class integer labels, typically with softmax. Picking the loss that matches your label format is the difference between a model that learns and one that quietly reports nonsense accuracy.",
        "example": "model.compile(\n    optimizer=\"adam\",\n    loss=\"binary_crossentropy\",          # 0/1 labels\n    metrics=[\"accuracy\"],\n)",
        "usecase": "Two-class spam filtering vs N-class digit recognition — the loss must match how you encoded the labels.",
        "category": "tensorflow"
    },
    {
        "id": 27,
        "title": "GPU visibility config",
        "definition": "tf.config.list_physical_devices('GPU') lists visible accelerators, and set_memory_growth or set_visible_devices controls how they are used. When several processes share one card — or a single process should stay on one device — these calls prevent the classic out-of-memory collisions.",
        "example": "gpus = tf.config.list_physical_devices(\"GPU\")\nif gpus:\n    tf.config.experimental.set_memory_growth(gpus[0], True)",
        "usecase": "Running several models on one GPU or debugging out-of-memory errors — explicit device and memory policy, no surprises.",
        "category": "tensorflow"
    },
    {
        "id": 28,
        "title": "Save only weights",
        "definition": "save_weights() persists just the numbers — each weight and bias as a flat file — while load_weights() restores them into a model with matching architecture. Unlike a full save, the file knows nothing about layers or optimizer, so the same weights map onto any identically-shaped model.",
        "example": "model.save_weights(\"weights.h5\")\nmodel2 = make_model_with_same_shape()\nmodel2.load_weights(\"weights.h5\")",
        "usecase": "Moving weights between model variants — research, distillation or a leaner serving build — without rebuilding the artifact.",
        "category": "tensorflow"
    },
    {
        "id": 29,
        "title": "Data augmentation in the pipeline",
        "definition": "Augmentation layers — RandomFlip, RandomRotation, RandomZoom — transform each training image on the fly, yielding a fresh, slightly different example every epoch. The dataset effectively grows, and the model learns invariance to the transformations instead of memorizing exact pixels.",
        "example": "aug = tf.keras.Sequential([\n    layers.RandomFlip(\"horizontal\"),\n    layers.RandomRotation(0.1),\n])\n# feed model input through aug during training only",
        "usecase": "Making a small image dataset effectively bigger and teaching the model to ignore flips, rotations and zooms.",
        "category": "tensorflow"
    },
    {
        "id": 30,
        "title": "Custom metrics are functions",
        "definition": "Subclass tf.keras.metrics.Metric, implement update_state(y_true, y_pred) and maybe result(), and your metric joins the compile list with full per-epoch tracking. Custom metrics surface the numbers that matter to your business — not just the ones Keras guessed you wanted.",
        "example": "class TopK(tf.keras.metrics.Metric):\n    def update_state(self, y_true, y_pred):\n        # accumulate hits where the true class is in top k\n        ...\n    def result(self):\n        return self.acc / self.count",
        "usecase": "Reporting top-5 accuracy, F1 or other business metrics alongside the built-ins — monitored by callbacks too.",
        "category": "tensorflow"
    },
    {
        "id": 31,
        "title": "Keras optimizers amped up",
        "definition": "Keras optimizers expose more than learning rate: clipnorm trims the gradient norm per step, clipvalue clips individual values, and momentum, rho and epsilon tune the optimizer's internals. Adjusting these beats shipping defaults when gradients misbehave or convergence stalls.",
        "example": "optimizer = tf.keras.optimizers.Adam(learning_rate=1e-3, clipnorm=1.0)",
        "usecase": "Taming exploding gradients and tuning convergence speed per model — optimizer configuration is a first-class hyperparameter.",
        "category": "tensorflow"
    },
    {
        "id": 32,
        "title": "Mixed precision for free speed",
        "definition": "set_global_policy('mixed_float16') runs the model in half precision under the hood — float16 buffers, float32 accumulation — cutting memory use roughly in half. On GPUs with tensor cores this translates directly to faster training, with accuracy usually within noise of full precision.",
        "example": "tf.keras.mixed_precision.set_global_policy(\"mixed_float16\")",
        "usecase": "Bigger batches and higher throughput on tensor-core GPUs — one line of configuration before the model is even built.",
        "category": "tensorflow"
    },
    {
        "id": 33,
        "title": "Functional multi-input models",
        "definition": "Functional models accept any number of inputs: build one Input() per source, fold the branches together with a merge layer like Concatenate, and declare tf.keras.Model([inp_a, inp_b], out). Multi-modal data reaches a shared representation before the head decides.",
        "example": "img = tf.keras.Input((28, 28))\nmeta = tf.keras.Input((5,))\nmerged = tf.keras.layers.Concatenate()([layers.Flatten()(img), meta])\nout = layers.Dense(1)(merged)\nmodel = tf.keras.Model([img, meta], out)",
        "usecase": "Models that combine pixel data with tabular features — image-and-metadata fraud detection being the canonical example.",
        "category": "tensorflow"
    },
    {
        "id": 34,
        "title": "ReduceLROnPlateau, set and forget",
        "definition": "ReduceLROnPlateau watches a metric you name and, when it stops improving for patience epochs, multiplies the learning rate by its factor. Plateaus dissolve automatically — training resumes progress without anyone intervening — which makes it close to a free accuracy booster at the tail of runs.",
        "example": "cb = tf.keras.callbacks.ReduceLROnPlateau(\n    monitor=\"val_loss\", factor=0.5, patience=2)\nmodel.fit(x, y, validation_split=0.2, callbacks=[cb])",
        "usecase": "Escaping loss plateaus automatically instead of babysitting the learning rate through long training runs.",
        "category": "tensorflow"
    },
    {
        "id": 35,
        "title": "Padding and masking sequences",
        "definition": "Variable-length sequences become one rectangular batch by padding shorter ones to a fixed max length; masks mark real positions so layers like embedding and RNN ignore the filler. Preprocessing normalizes lengths, while masking keeps the semantics honest — padded cells never leak into the computation.",
        "example": "from tensorflow.keras.preprocessing.sequence import pad_sequences\nseqs = pad_sequences(ids, maxlen=100, padding=\"post\")",
        "usecase": "Batching sentences of varying length — pad to 100 tokens and mask so attention and RNNs skip the filler.",
        "category": "tensorflow"
    },
    {
        "id": 36,
        "title": "The KerasTuner for hyperparams",
        "definition": "keras_tuner searches the hyperparameter space for you: you define build_model(hp) with hp.Choice and hp.Int ranges, and the tuner runs trial architectures against your objective. What would be days of hand-tuned experiments becomes an automated sweep over layer counts, units and learning rates.",
        "example": "import keras_tuner as kt\ntuner = kt.Hyperband(build_model, objective=\"val_accuracy\", max_epochs=10)\ntuner.search(x_train, y_train)\nbest = tuner.get_best_models(1)[0]",
        "usecase": "Letting automated search spend the GPU hours finding a strong architecture instead of guessing by hand.",
        "category": "tensorflow"
    },
    {
        "id": 37,
        "title": "Monitors say what you optimize",
        "definition": "The metrics you list in compile are what you will judge the model by — and what callbacks like ModelCheckpoint monitor. Accuracy alone lies on imbalanced data, so pick metrics that match the cost of each error type. The monitor defines what good looks like, so choose deliberately.",
        "example": "model.compile(optimizer=\"adam\", loss=\"binary_crossentropy\",\n              metrics=[tf.keras.metrics.Recall(), tf.keras.metrics.Precision()])",
        "usecase": "Fraud or defect data where accuracy hides problems — precision and recall tell the real story of rare-class performance.",
        "category": "tensorflow"
    },
    {
        "id": 38,
        "title": "The tf.data cache() trick",
        "definition": "dataset.cache() stores the (already decoded, already normalized) dataset in memory or on disk after the first pass, so subsequent epochs skip reprocessing entirely. Expensive per-sample work — image decoding, text preprocessing — runs once instead of for every epoch.",
        "example": "ds = ds.cache().shuffle(10000).batch(32).prefetch(tf.data.AUTOTUNE)",
        "usecase": "Trimming repeated image decoding and normalization work on every epoch — cache makes later epochs nearly free.",
        "category": "tensorflow"
    },
    {
        "id": 39,
        "title": "Random seeds for reproducibility",
        "definition": "Reproducible runs require pinning every randomness source: Python's random, NumPy's generator and TensorFlow's own tf.random.set_seed(). With all three fixed, weight init and data shuffling repeat identically across machines — the foundation of fair experiment comparison.",
        "example": "import random\nimport numpy as np\nrandom.seed(42)\nnp.random.seed(42)\ntf.random.set_seed(42)",
        "usecase": "Comparing architectures fairly — identical runs across machines and restarts, once every seed is pinned.",
        "category": "tensorflow"
    },
    {
        "id": 40,
        "title": "Fine-tune by unfreezing",
        "definition": "After the frozen-backbone phase converges, set base.trainable = True and re-compile with a much smaller learning rate. The pretrained features now adapt to your domain in small steps — too large a rate would overwrite them. This second phase is what delivers the biggest accuracy gains in transfer learning.",
        "example": "base.trainable = True\nmodel.compile(optimizer=tf.keras.optimizers.Adam(1e-5))   # tiny lr, not 1e-3",
        "usecase": "The second phase of transfer learning — adapting ImageNet features to your specific data instead of accepting them as fixed.",
        "category": "tensorflow"
    },
    {
        "id": 41,
        "title": "Handling dataset imbalance",
        "definition": "class_weight tells the loss how much each class's errors matter: rare classes get higher weights, so the model cannot win by ignoring them. The loss sums weighted terms per class, effectively balancing a skewed dataset without resampling and without touching a single row.",
        "example": "class_weight = {0: 1.0, 1: 20.0}\nmodel.fit(x, y, class_weight=class_weight)",
        "usecase": "Fraud detection, defect screening and medical data where the positive class is rare — weight it into every loss instead of sampling it away.",
        "category": "tensorflow"
    },
    {
        "id": 42,
        "title": "LSTMs handle context",
        "definition": "LSTM layers carry a hidden state across time steps, remembering relevant context from the whole past as each token is processed. return_sequences=True surfaces every step's output, letting a pooling layer summarize the sequence before the final Dense head decides.",
        "example": "tf.keras.Sequential([\n    layers.Embedding(10000, 64),\n    layers.LSTM(128, return_sequences=True),\n    layers.GlobalAveragePooling1D(),\n    layers.Dense(1, activation=\"sigmoid\"),\n])",
        "usecase": "Text sentiment, log anomaly detection and time-series regression — tasks where the answer hides in earlier context.",
        "category": "tensorflow"
    },
    {
        "id": 43,
        "title": "Loss functions at a glance",
        "definition": "The loss must match the label type: MSE for continuous values, CategoricalCrossentropy for one-hot classes, SparseCategoricalCrossentropy for integer classes, BinaryCrossentropy for two classes, Hinge for margin-style objectives. Every Keras loss is also a layer you can call directly.",
        "example": "model.compile(\n    loss=tf.keras.losses.MeanSquaredError(),   # regression\n    optimizer=\"adam\",\n)",
        "usecase": "Regression predicts numbers, classification predicts labels — mismatching the loss to the label format quietly sabotages training.",
        "category": "tensorflow"
    },
    {
        "id": 44,
        "title": "Layer reuse in functional graphs",
        "definition": "Calling the same layer object on two different inputs reuses its weights — one shared transformation applied to both branches. That is weight tying for free: both inputs embed into the identical space, which is exactly what Siamese-style comparison networks rely on.",
        "example": "shared = layers.Dense(64, activation=\"relu\")\na = shared(input_a)\nb = shared(input_b)   # same weights applied twice",
        "usecase": "Siamese networks and contrastive learning, comparing two inputs through one shared embedding space.",
        "category": "tensorflow"
    },
    {
        "id": 45,
        "title": "Time series windowing",
        "definition": "A sliding window turns raw timestamps into supervised pairs: each window of N past steps becomes X and the next step becomes y. The loop is a few lines, and with windows in place any regression model can forecast any series — the essence of supervised time-series ML.",
        "example": "X, y = [], []\nfor i in range(len(data) - 24):\n    X.append(data[i:i+24])    # past 24 steps\n    y.append(data[i+24])      # next step\nX, y = np.array(X), np.array(y)",
        "usecase": "Forecasting temperature, sales or power load from the previous N steps — windowing is the bridge from series to supervised data.",
        "category": "tensorflow"
    },
    {
        "id": 46,
        "title": "Debug with eager execution",
        "definition": "TensorFlow runs eagerly by default — operations execute immediately, so breakpoints, print() and the Python debugger behave exactly as they do in plain code. Intermediate tensors are inspectable mid-graph, which makes debugging loss and gradient issues a straightforward Python session.",
        "example": "tf.debugging.assert_all_finite(x, \"NaN in input!\")",
        "usecase": "Debugging gradients and losses by inspecting intermediate tensors in plain Python — no graph compilation mystery.",
        "category": "tensorflow"
    },
    {
        "id": 47,
        "title": "ModelCheckpoint strategies",
        "definition": "ModelCheckpoint saves weights automatically — save_best_only=True with a monitored metric keeps only the strongest epoch, and mode='max' or 'min' says which direction is better. A bad final epoch then costs nothing: the checkpoint preserves the best model the run ever produced.",
        "example": "cp = tf.keras.callbacks.ModelCheckpoint(\n    \"best.keras\", monitor=\"val_accuracy\",\n    mode=\"max\", save_best_only=True,\n)",
        "usecase": "Long runs that teeter on the validation curve — you always keep the best snapshot, never the last wandering epoch.",
        "category": "tensorflow"
    },
    {
        "id": 48,
        "title": "Custom layers with build + call",
        "definition": "Subclass layers.Layer: create weights in build(input_shape) once shapes are known, and define the forward math in call(). Anything Keras doesn't ship — attention blocks, exotic activations, custom regularizers — becomes a first-class layer that composes with everything else.",
        "example": "class MyLayer(layers.Layer):\n    def build(self, input_shape):\n        self.w = self.add_weight(shape=(input_shape[-1], 8))\n    def call(self, x):\n        return x @ self.w",
        "usecase": "From attention blocks to experimental activations — full control of weights and math, composed with standard Keras layers.",
        "category": "tensorflow"
    },
    {
        "id": 49,
        "title": "Per-epoch metrics history",
        "definition": "fit() returns a History object whose history dict holds a per-epoch list for every metric — training and validation, loss and accuracy alike. Plotting those lists tells the whole story: whether loss falls smoothly, whether the gap to validation widens, and when training starts to overfit.",
        "example": "history = model.fit(x, y, epochs=10, validation_split=0.2)\nprint(history.history[\"loss\"])        # [0.69, 0.31, ...]\nprint(history.history[\"val_loss\"])",
        "usecase": "Plotting loss and accuracy curves to judge convergence and overfitting at a glance — the default post-training review.",
        "category": "tensorflow"
    },
    {
        "id": 50,
        "title": "From model to production",
        "definition": "model.export() writes a SavedModel — a self-contained directory with the graph, weights and serving signature. TensorFlow Serving can host it behind a gRPC or REST endpoint at scale, and conversion tools can port it to TFLite for phones and edge devices.",
        "example": "model.export(\"saved_model\")   # self-contained serving directory",
        "usecase": "Serving trained models at scale with TensorFlow Serving, or shrinking them for mobile and edge hardware with TFLite.",
        "category": "tensorflow"
    }
]
