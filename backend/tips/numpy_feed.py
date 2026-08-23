TIPS = [
    {
        "id": 1,
        "title": "np.array, the raw material",
        "definition": "np.array builds NumPy's core object: a fast, homogeneous, multi-dimensional array of numeric values stored in contiguous memory. It is the storage layer underneath pandas columns, images and every ML framework — wherever arrays of numbers need batch, compiled-speed math.",
        "example": "import numpy as np\narr = np.array([1, 2, 3, 4])\nprint(arr.dtype, arr.shape)   # int64 (4,)",
        "usecase": "The foundation of scientific computing in Python — every NumPy op, image tensor and model input ultimately lives in one.",
        "category": "numpy"
    },
    {
        "id": 2,
        "title": "dtype chooses the precision",
        "definition": "A NumPy array is typed: dtype decides whether values are float64, float32, int64, uint8 and so on — controlling both numeric precision and memory footprint. Halving precision on a 100-million-element array halves the RAM it needs while calculations still behave predictably.",
        "example": "arr = np.array([1, 2, 3], dtype=np.float32)\nprint(arr.itemsize)    # 4 bytes per element",
        "usecase": "Halving memory on huge arrays when float32 precision is enough, or pinning integer widths to match storage formats.",
        "category": "numpy"
    },
    {
        "id": 3,
        "title": "shape and reshape",
        "definition": "An array's shape is its dimensions, and reshape() reinterprets the same underlying data in a new layout as long as the total element count matches. Reshaping never moves or copies values — it just changes the index arithmetic, making it the free way to flatten, batch or reformat arrays.",
        "example": "arr = np.arange(12).reshape(3, 4)\nprint(arr.shape)          # (3, 4)\nprint(arr.reshape(12))    # back to flat",
        "usecase": "Flattening, padding or reformatting arrays to fit model input shapes — reshape does it without touching the data.",
        "category": "numpy"
    },
    {
        "id": 4,
        "title": "Indexing and slicing arrays",
        "definition": "NumPy indexing extends Python's list syntax to N dimensions: arr[i] picks an element or sub-array, arr[1:3] slices a range, and arr[:, 0] selects a whole column. Slice notation composes across axes, so any rectangular block of a matrix or volume is one expression.",
        "example": "m = np.arange(12).reshape(3, 4)\nprint(m[1])        # second row\nprint(m[:, 1])     # second column\nprint(m[0:2, 1:3]) # 2x2 block",
        "usecase": "Extracting rows, columns and sub-blocks from matrices and grids — the everyday entry into array data.",
        "category": "numpy"
    },
    {
        "id": 5,
        "title": "Boolean indexing, filters without loops",
        "definition": "Passing a boolean array of the same shape into the brackets keeps only the elements where the mask is True — the vectorized filter. Conditions combine with &, | and ~, so 'keep everything satisfying this rule' becomes one expression with no Python loop anywhere.",
        "example": "nums = np.array([1, 5, 9, 12])\nbig = nums[nums > 5]          # [9 12]\neven = nums[nums % 2 == 0]    # [12]",
        "usecase": "Filtering outliers, masking invalid data or selecting values that satisfy complex conditions in bulk.",
        "category": "numpy"
    },
    {
        "id": 6,
        "title": "Fancy indexing, arbitrary picks",
        "definition": "Indexing with an array of positions pulls specific elements in any order: nums[[3, 0, 2]] grabs elements at those positions. The index array can be built from computation, sampling or shuffling, so reordering a whole array according to a permutation is a single expression.",
        "example": "nums = np.array([10, 20, 30, 40])\npicked = nums[[3, 0, 2]]      # [40 10 30]\nshuffled = nums[np.random.permutation(len(nums))]",
        "usecase": "Random sampling, reordering rows and columns, or remapping arrays to an index pattern from elsewhere in the program.",
        "category": "numpy"
    },
    {
        "id": 7,
        "title": "Broadcasting, implicit expansion",
        "definition": "Broadcasting lets smaller arrays stretch to match larger ones for elementwise math: a (3,1) column plus a (1,4) row produces a (3,4) result without replicating data. Dimensions align from the right, size-1 dimensions expand, which keeps expressions like 'add a vector to every row' concise.",
        "example": "col = np.array([[1], [2], [3]])      # (3, 1)\nrow = np.array([10, 20, 30])          # (3,)\nprint(col + row)                      # (3, 3)",
        "usecase": "Adding a column vector to every row, normalizing rows by a vector, or combining grids — without any explicit copy.",
        "category": "numpy"
    },
    {
        "id": 8,
        "title": "arange and linspace, ranges on rails",
        "definition": "np.arange(start, stop, step) produces values stepped by a fixed increment like range(); np.linspace(start, stop, n) produces exactly n evenly spaced points between the endpoints, inclusive. arange is good for counts and steps, linspace for precise, evenly-spaced grids.",
        "example": "np.arange(0, 1, 0.25)   # [0.   0.25 0.5  0.75]\nnp.linspace(0, 1, 5)     # [0.   0.25 0.5  0.75 1. ]",
        "usecase": "Building coordinate grids, time axes and test signals — the two standard ways to create ordered sequences.",
        "category": "numpy"
    },
    {
        "id": 9,
        "title": "random, the trial maker",
        "definition": "np.random provides seeded randomness for arrays: rand and randn for uniform and normal draws, randint for integers, plus shuffle, choice and permutation. Seeding with seed(42) makes every draw reproducible — the foundation of simulations, initializations and benchmarks.",
        "example": "np.random.seed(42)\nuniform = np.random.rand(3, 3)\nnormal = np.random.randn(3)          # mean 0, std 1",
        "usecase": "Weight initialization, simulation, bootstrapping and train/test shuffles — reproducible randomness at C speed.",
        "category": "numpy"
    },
    {
        "id": 10,
        "title": "views vs copies, know the difference",
        "definition": "Slicing an array returns a view sharing the same memory; .copy() produces an independent duplicate. Changing a view can silently modify the original, and reshaping a non-contiguous view may force an implicit copy. Knowing which you hold prevents accidental aliasing bugs.",
        "example": "sub = arr[1:4]          # view shares memory\nsafe = arr[1:4].copy()  # independent\nafter = arr.reshape(...)  # view when possible",
        "usecase": "Avoiding accidental aliasing when reshaping or storing subsets — copy when you'll modify, view when you want speed.",
        "category": "numpy"
    },
    {
        "id": 11,
        "title": "np.newaxis, add a dimension",
        "definition": "np.newaxis (the same as None) inserts a length-1 axis at the position you place it, turning a 1D vector into a column: v[:, np.newaxis] becomes (n, 1). Adding that axis aligns shapes for broadcasting, dot products and matrix mathematics.",
        "example": "v = np.array([1, 2, 3])\ncol = v[:, np.newaxis]   # (3, 1)\nrow = v[np.newaxis, :]   # (1, 3)",
        "usecase": "Turning arrays into columns or rows so matrix products, broadcasting and stacking behave as intended.",
        "category": "numpy"
    },
    {
        "id": 12,
        "title": "axis, the direction of operations",
        "definition": "Reductions take an axis argument that says which dimension to collapse. axis=0 collapses rows, giving per-column results; axis=1 collapses columns, giving per-row results. Misreading the axis is a classic source of silently transposed numbers — always check it twice.",
        "example": "m = np.array([[1, 2], [3, 4]])\nprint(m.sum(axis=0))   # [4 6]  column sums\nprint(m.sum(axis=1))   # [3 7]  row sums",
        "usecase": "Column sums versus row sums, per-channel statistics and any reduction along the dimension you actually meant.",
        "category": "numpy"
    },
    {
        "id": 13,
        "title": "reduce with sum, mean, std, min…",
        "definition": "aggregations like np.sum, np.mean, np.std, np.min and np.max collapse an array into a scalar or a lower-dimension result, optionally along an axis. They run in compiled code, so statistics over millions of values — datasets, batches, image channels — come back in milliseconds.",
        "example": "np.mean(arr, axis=0)        # per-column means\nnp.std(arr.flatten())        # overall spread\ndist = np.max(arr, axis=1) - np.min(arr, axis=1)",
        "usecase": "Computing statistics over datasets, batches or image channels — the vectorized path to any summary number.",
        "category": "numpy"
    },
    {
        "id": 14,
        "title": "vectorization, speed without loops",
        "definition": "NumPy operations act on whole arrays in compiled C, so arr * 2 + 1 transforms every element simultaneously. Writing equivalent Python loops pays per-element interpreter overhead and runs orders of magnitude slower — vectorized expressions are how large data stays fast.",
        "example": "result = arr * 2 + 1        # every element at once\nmasked = np.where(arr > 0, arr, 0)",
        "usecase": "Transforming millions of values in milliseconds instead of seconds — the single most important NumPy habit.",
        "category": "numpy"
    },
    {
        "id": 15,
        "title": "np.where, vectorized if-else",
        "definition": "np.where(condition, a, b) evaluates the condition across the array and chooses a where it's True, b where it's False — a vectorized if/else. Wrap the same array twice to clamp or transform selectively, and you get masking, thresholding and conditional math without a loop.",
        "example": "arr = np.array([-3, 0, 4])\nnp.where(arr > 0, arr, -arr)     # abs\nnp.where(arr > 0, 'pos', 'non')  # labels",
        "usecase": "Conditional math, masking or replacing values — pushing branch logic into one fast array-wide expression.",
        "category": "numpy"
    },
    {
        "id": 16,
        "title": "argmax and argmin, where's the peak?",
        "definition": "np.argmax and np.argmin return the index of the largest or smallest value, overall or along an axis. Locating the position of an extreme — the winning class, the peak of a signal, the hottest cell — is a fingertip operation that pairs naturally with computing the value itself.",
        "example": "grads = np.array([0.1, 0.5, 0.9])\nbest = grads.argmax()          # 2\npeak_row = m.argmax(axis=1)    # per-row peaks",
        "usecase": "Peak detection, finding the winning class or the location of extremes — position and value in two quick calls.",
        "category": "numpy"
    },
    {
        "id": 17,
        "title": "sort, argsort, and order",
        "definition": "np.sort reorders the values themselves, while np.argsort returns the indices that would sort the array — letting you reorder any other array to match. Sorting a scores column and matching rows to it is a one-liner with argsort, and argpartition finds top-k without a full sort.",
        "example": "scores = np.array([70, 90, 50])\norder = scores.argsort()      # [2 0 1]\nsorted_scores = scores[order] # [50 70 90]",
        "usecase": "Ranking values, coupling a sort to other arrays, or loading the top-k positions from any scored list.",
        "category": "numpy"
    },
    {
        "id": 18,
        "title": "unique, every distinct value, counted",
        "definition": "np.unique returns the array's distinct values in sorted order, and return_counts=True pairs them with how often each occurs. It turns a noisy list into a clean category inventory plus histogram from one call — the fastest distinct-value check in NumPy.",
        "example": "vals, counts = np.unique(arr, return_counts=True)\ndict(zip(vals, counts))   # value -> frequency",
        "usecase": "Category inventories, quick histogram data or distinct-count checks — before deciding how to bucket or encode.",
        "category": "numpy"
    },
    {
        "id": 19,
        "title": "dot and @, real matrix algebra",
        "definition": "np.dot and its @ operator perform matrix multiplication — the defining operation of linear algebra. Given compatible shapes, an @ b contracts the matching inner dimension and applies outer ones, powering everything from linear regression to the weight matrices inside neural networks.",
        "example": "A = np.array([[1, 2], [3, 4]])\nB = np.array([[5, 6], [7, 8]])\nC = A @ B      # [[19 22] [43 50]]",
        "usecase": "Linear regression, coordinate transforms and the matrix math under every neural-net layer — written as one operation.",
        "category": "numpy"
    },
    {
        "id": 20,
        "title": "transpose, flip axes",
        "definition": "arr.T transposes an array, swapping rows and columns for 2D data and reversing the axis order for higher dimensions; np.transpose can reorder axes in any permutation. Transposing realigns shapes for matrix multiplication, image channel layouts and coordinate swaps.",
        "example": "m = np.arange(6).reshape(2, 3)\nprint(m.T.shape)      # (3, 2)\nimg = img.transpose(2, 0, 1)   # HWC -> CHW",
        "usecase": "Preparing shapes for dot products, rearranging image channels or swapping coordinate axes — a shape-only, no-copy view.",
        "category": "numpy"
    },
    {
        "id": 21,
        "title": "stack and concatenate, combine arrays",
        "definition": "NumPy combines arrays several ways: concatenate joins along an existing axis, hstack/vstack pack them side by side or top to bottom, and stack adds a brand-new axis to hold them. Assembling feature matrices, batches or panels is then a one-call operation rather than manual loops.",
        "example": "np.hstack([a, b])     # columns side by side\nnp.vstack([a, b])     # rows stacked vertically\nnp.stack([a, b])      # new axis in front",
        "usecase": "Assembling feature matrices, batches or panels from separate arrays — each joiner for the layout you need.",
        "category": "numpy"
    },
    {
        "id": 22,
        "title": "nan-aware functions",
        "definition": "np.nanmean, np.nansum, np.nanstd and friends compute statistics while skipping NaN values, rather than letting a single missing point poison the whole result. Sensor streams, surveys and imports full of gaps stay analyzable without a mandatory cleanup pass first.",
        "example": "import numpy as np\nnp.nanmean(np.array([1, 2, np.nan]))   # 1.5, NaN skipped",
        "usecase": "Sensor data or surveys with missing readings — compute means, sums and spreads despite the gaps.",
        "category": "numpy"
    },
    {
        "id": 23,
        "title": "clip bounds values",
        "definition": "np.clip clamps every element into a lower/upper range: anything below goes to the lower bound, anything above to the upper, everything else stays. It tames outliers and sanitizes inputs without deleting a single observation.",
        "example": "np.clip(np.array([-5, 50, 300]), 0, 100)  # [-5 -> 0] [-5, 50, 100]",
        "usecase": "Capping explosion values, winsorizing tails or clamping network inputs to a safe operating range.",
        "category": "numpy"
    },
    {
        "id": 24,
        "title": "meshgrid, coordinate grids instantly",
        "definition": "np.meshgrid takes 1D axis arrays and expands them into full 2D (or N-D) grids where every coordinate combination appears once. Evaluating a function over a plane — plotting surfaces, computing distances — becomes array math instead of a nested loop.",
        "example": "x = np.linspace(-1, 1, 5)\ny = np.linspace(-1, 1, 5)\nX, Y = np.meshgrid(x, y)\nZ = X ** 2 + Y ** 2      # value at every grid point",
        "usecase": "Plotting surfaces, computing distance fields or building any coordinate grid for numerical math.",
        "category": "numpy"
    },
    {
        "id": 25,
        "title": "loadtxt/savetxt, plain text I/O",
        "definition": "np.savetxt writes arrays as human-readable plain text (CSV-style) and np.loadtxt reads them back, with column/format controls. It is the simplest interchange format going — useful for spreadsheets, fixtures and debugging dumps where binary formats would be opaque.",
        "example": "np.savetxt('data.csv', arr, delimiter=',', fmt='%.4f')\ndata = np.loadtxt('data.csv', delimiter=',')",
        "usecase": "Exporting arrays for spreadsheets or other tooling, and loading numeric fixtures — no libraries required on the receiving end.",
        "category": "numpy"
    },
    {
        "id": 26,
        "title": "linalg for linear equations",
        "definition": "np.linalg concentrates the linear algebra: solve for linear systems, inv for inverses, eig/eigh for eigenproblems, det for determinants, lstsq for least squares. The same machinery powers regression fits, PCA and most engineering math — one import away.",
        "example": "A = np.array([[3, 1], [1, 2]])\nx = np.linalg.solve(A, np.array([9, 8]))   # solves A x = b\nw = np.linalg.lstsq(X, y, rcond=None)[0]  # least squares",
        "usecase": "Least-squares fitting, PCA, coordinate transforms and physics/engineering computations — the solver toolbox for linear systems.",
        "category": "numpy"
    },
    {
        "id": 27,
        "title": "apply_along_axis for custom ops",
        "definition": "np.apply_along_axis runs a Python function over every slice along one axis — each row or column handed to your function with its results collected. When no vectorized built-in expresses the logic, it's the structured way to do row-wise custom work.",
        "example": "span = np.apply_along_axis(\n    lambda row: np.max(row) - np.min(row), axis=1, arr=m)",
        "usecase": "Row-wise custom metrics and per-column transforms before vectorized ideas prove too convoluted to write.",
        "category": "numpy"
    },
    {
        "id": 28,
        "title": "einsum, the signature of tensor math",
        "definition": "np.einsum uses index-script notation ('ij,jk->ik') to declare what to multiply and sum, collapsing many separate ops — matmul, transpose, diagonal, trace — into one readable call. For complex tensor contractions in ML and physics it is both compact and fast.",
        "example": "np.einsum('ij,jk->ik', A, B)   # matrix multiply\nnp.einsum('ii->i', A)            # diagonal\nnp.einsum('ij->ji', A)           # transpose",
        "usecase": "Tensor contractions in ML and physics where products and sums over axes need to stay readable and run at C speed.",
        "category": "numpy"
    },
    {
        "id": 29,
        "title": "flatten vs ravel, view vs copy again",
        "definition": "ravel() returns a flattened view of the data when the layout allows, sharing memory; flatten() always produces an independent copy. Both linearize any array, but choosing knowledgeably — view for speed, copy for safety — avoids surprise aliasing when you mutate the result.",
        "example": "flat_view = m.ravel()     # shares memory when possible\nflat_copy = m.flatten()    # always a fresh copy",
        "usecase": "Linearizing any-dimensional arrays for output or interop — reach for flatten when you'll modify the result.",
        "category": "numpy"
    },
    {
        "id": 30,
        "title": "full, zeros, ones, eye in bulk",
        "definition": "Pre-filled arrays come from dedicated constructors: zeros and ones fill with 0 or 1, full fills with any constant, and eye produces identity matrices with 1s on the diagonal. Initializing weights, masks and placeholder buffers is one call with no loops.",
        "example": "np.zeros((3, 4))       # all zeros\nnp.ones((2, 3))        # all ones\nnp.eye(4)              # 4x4 identity\nnp.full(10, 7)         # all 7s",
        "usecase": "Initializing weight matrices, masks, basis vectors and scratch buffers — pre-built arrays at C speed.",
        "category": "numpy"
    },
    {
        "id": 31,
        "title": "arange with floats, careful",
        "definition": "Stepping floats with arange accumulates binary rounding error, so endpoints can come out uneven or slightly off — and the stop value is never guaranteed to be hit. linspace computes endpoints directly and splits the interval evenly, making it the reliable choice for floats.",
        "example": "np.arange(0, 1, 0.1)        # 0.29999... surprises possible\nnp.linspace(0, 1, 11)         # crisp endpoints, 10 exact steps",
        "usecase": "Time axes and coordinate steps where endpoint precision and even spacing genuinely matter.",
        "category": "numpy"
    },
    {
        "id": 32,
        "title": "masked arrays, ignore the bad bits",
        "definition": "np.ma arrays carry a parallel mask marking entries to exclude — operations like mean, sum and plot skip masked elements automatically. Sentinel values like -999 or corrupt readings get flagged instead of deleted, and statistics stay clean without dropping rows.",
        "example": "m = np.ma.array([1.0, -999, 3.0], mask=[False, True, False])\nprint(m.mean())   # 2.0, the -999 excluded",
        "usecase": "Data with sentinel or invalid values where you want statistics and plots to ignore the bad bits rather than the rows.",
        "category": "numpy"
    },
    {
        "id": 33,
        "title": "broadcasting rules in one glance",
        "definition": "Broadcasting aligns trailing dimensions, expands size-1 axes to match, and errors when non-1 dimensions disagree. Skimming the shapes right-to-left predicts whether an operation is legal and what shape it yields — one read that prevents a class of cryptic runtime errors.",
        "example": "np.ones((3, 1)) + np.ones((1, 4))   # (3, 4): both expand\n# (3,) + (4,) -> error: aligned, neither is 1",
        "usecase": "Preventing cryptic shape errors and writing concise elementwise math that behaves exactly as intended.",
        "category": "numpy"
    },
    {
        "id": 34,
        "title": "np.gradient for slopes",
        "definition": "np.gradient computes numerical derivatives with central differences — the local rate of change along each axis (excluding edge effects handled by one-sided differences). Velocity from position or growth from level data falls out without fitting anything.",
        "example": "x = np.linspace(0, 10, 100)\ny = x ** 2\ndy = np.gradient(y, x)     # ~2x, the exact slope field",
        "usecase": "Velocity from position series, growth rates from level data, and edge detection in image arrays.",
        "category": "numpy"
    },
    {
        "id": 35,
        "title": "pad for borders",
        "definition": "np.pad wraps an array with borders using a chosen mode — constant values, edge values replicated, or reflected data. Padding before convolutions and windowed operations removes boundary effects by extending data sensibly beyond its edge.",
        "example": "np.pad(arr, 1, mode='constant', constant_values=0)\nnp.pad(arr, 2, mode='edge')     # repeat edge values",
        "usecase": "Preparing convolutions, avoiding boundary artifacts and framing images — borders built in any style in one call.",
        "category": "numpy"
    },
    {
        "id": 36,
        "title": "concatenate, the flexible joiner",
        "definition": "np.concatenate ties arrays together along any chosen existing axis — the general form underneath hstack, vstack and dstack. Give it a list of arrays with matching shapes except along that axis, and they merge into one larger array.",
        "example": "np.concatenate([a, b], axis=0)   # stack rows\nnp.concatenate([a, b], axis=1)   # join columns",
        "usecase": "Appending batches, merging arrays of matching shape along a dimension — the workhorse joiner for most array assembly.",
        "category": "numpy"
    },
    {
        "id": 37,
        "title": "cumsum and cumprod, running totals",
        "definition": "np.cumsum and np.cumprod compute running totals: every output element is the sum (or product) of everything up to it. Prefix sums power ranges, running balances, cumulative hits and counting algorithms — all in one vectorized call.",
        "example": "np.cumsum(np.array([1, 2, 3]))     # [1 3 6]\nspend = np.cumsum(daily_spend)         # total over time",
        "usecase": "Total spend over time, running hits, cumulative distributions and prefix computations over any series.",
        "category": "numpy"
    },
    {
        "id": 38,
        "title": "argpartition, top-k fast",
        "definition": "np.argpartition partially orders an array so the k smallest or largest elements land in the first or last k positions — with no full sort. For finding top-k on huge arrays it's dramatically cheaper than sorting everything, which makes it the go-to for retrieval-like problems.",
        "example": "top_idx = np.argpartition(scores, -5)[-5:]\nbest5 = scores[top_idx]",
        "usecase": "Top-k retrieval — recommendations, best matches, largest scores — on arrays too large to sort fully.",
        "category": "numpy"
    },
    {
        "id": 39,
        "title": "np.c_ and r_, build fast",
        "definition": "np.c_ and np.r_ are index-trick shorthands: np.c_ concatenates along columns and np.r_ along rows, accepting ranges and slices with an easy syntax. Building design matrices and assembling features in one readable line.",
        "example": "np.c_[np.ones(3), np.arange(3)]   # add a column of ones\nnp.r_[1:4, np.array([9])]            # [1 2 3 9]",
        "usecase": "Design matrices, appending bias terms and fast column assembly for linear models and experiments.",
        "category": "numpy"
    },
    {
        "id": 40,
        "title": "float precision, never assume",
        "definition": "Floating-point arithmetic accumulates tiny rounding errors, so exact == comparisons on computed values fail even for mathematically-equal results. np.isclose and np.allclose compare with tolerance — the correct way to test whether computed numbers match.",
        "example": "np.isclose(0.1 + 0.2, 0.3)   # True\nnp.allclose(a, b)               # elementwise, with tolerance",
        "usecase": "Comparing computed values where small rounding differences are inevitable — equality with the tolerance that reality demands.",
        "category": "numpy"
    },
    {
        "id": 41,
        "title": "empty arrays with shape",
        "definition": "np.empty allocates an array of a given shape and dtype but does not initialize its contents — the memory holds whatever was there before. It is faster than zeros when you will overwrite every element anyway, which makes it the right tool for reusable buffers and accumulation loops.",
        "example": "buf = np.empty((100, 100), dtype=float)\nfor i in range(100):\n    buf[i] = compute_row(i)   # fully overwritten each time",
        "usecase": "Pre-allocating buffers your loop fills completely — faster allocation, no wasted zeroing.",
        "category": "numpy"
    },
    {
        "id": 42,
        "title": "squeeze drops size-1 axes",
        "definition": "np.squeeze removes every dimension whose length is 1, collapsing singleton axes without moving any data — or a specific axis when given as an argument. Reductions, aggregations and model outputs routinely leave (1, n) or (n, 1) shapes, and squeeze restores the clean form.",
        "example": "img_single = np.squeeze(img)      # (1, 224, 224) -> (224, 224)\nvec = np.squeeze(probs, axis=0)   # just the batch axis",
        "usecase": "Cleaning up shapes after reductions, aggregations or model outputs — dropping axes that carry no information.",
        "category": "numpy"
    },
    {
        "id": 43,
        "title": "repeat and tile, copy patterns",
        "definition": "np.repeat duplicates each element a given number of times, while np.tile replicates the entire array as a single block. Repeat gives [1,1,1,2,2,2]; tile gives [1,2,1,2,1,2] — different repetition patterns from the same input, each fitting a different kind of expansion.",
        "example": "np.repeat([1, 2], 3)   # [1 1 1 2 2 2]\nnp.tile([1, 2], 3)     # [1 2 1 2 1 2]",
        "usecase": "Balancing classes, building periodic signals or generating synthetic samples by repetition.",
        "category": "numpy"
    },
    {
        "id": 44,
        "title": "choose between arrays",
        "definition": "np.where(condition, a, b) selects element-by-element from a where the condition is True and b where it is False — full-array vectorized branching. Both a and b can be scalars or arrays, so thresholds and flags become one expression with no Python loop.",
        "example": "status = np.where(scores > 80, 'pass', 'fail')\nreplacement = np.where(np.isnan(data), median, data)",
        "usecase": "Thresholds, flag collars and vectorized if/else — decide per element in bulk, not per row.",
        "category": "numpy"
    },
    {
        "id": 45,
        "title": "rates of change with diff",
        "definition": "np.diff computes the difference between each pair of successive elements, shortening the array by the step count. Combined with division by the original values it yields per-step rates — returns, velocities, deltas — the raw material of derivative-like signals.",
        "example": "returns = np.diff(prices) / prices[:-1]   # per-step percent change\nvel = np.diff(positions) / np.diff(times)",
        "usecase": "Signal derivatives, financial returns, velocity from positions — successive-change math in one call.",
        "category": "numpy"
    },
    {
        "id": 46,
        "title": "argpartition for fast top-k",
        "definition": "np.argpartition partially sorts an array in linear time so the k smallest elements land in the first k positions (or largest, using negative indices from the end) — without a full sort. Finding top-k indices on arrays of millions is dramatically cheaper than sorting everything.",
        "example": "idx = np.argpartition(scores, -5)[-5:]   # indices of top 5\nworst = np.argpartition(errors, 10)[:10]   # bottom 10",
        "usecase": "Top-k recommendations, nearest-neighbor shortlists and outlier search on arrays too big to sort fully.",
        "category": "numpy"
    },
    {
        "id": 47,
        "title": "flatten vs ravel, same view",
        "definition": "arr.ravel() returns a flattened view of the data when the memory layout allows, sharing the original's values; arr.flatten() always builds an independent copy. The choice is speed versus safety — modifying a ravel can silently change the source array.",
        "example": "flat_view = arr.ravel()     # shares memory when possible\nflat_copy = arr.flatten()    # always independent",
        "usecase": "Iterating a 2D array linearly — ravel for read-only, flatten when you'll mutate without touching the original.",
        "category": "numpy"
    },
    {
        "id": 48,
        "title": "trig, log, and special functions",
        "definition": "NumPy ships a full vectorized math toolbox beyond Python's math module: sin/cos/tan, exp/log/log2/log10, plus special functions like erf, gamma and Bessel — all operating elementwise across whole arrays. Physics, statistics and signal work run at C speed, not Python-loop speed.",
        "example": "angles = np.linspace(0, 2 * np.pi, 1000)\nys = np.sin(angles)                     # whole curve at once\nerrs = np.erf(np.linspace(-2, 2, 10))",
        "usecase": "Physics, statistics and signal processing where pure-Python math over millions of points would crawl.",
        "category": "numpy"
    },
    {
        "id": 49,
        "title": "structured arrays, mixed dtypes",
        "definition": "Structured arrays store tuples of columns with different data types — one array whose fields can be numbers, short strings or dates, like a mini CSV in memory. Field access by name keeps heterogeneous tabular workloads on NumPy's fast, compact storage.",
        "example": "recs = np.array([('A', 1), ('B', 2)],\n                 dtype=[('name', 'U1'), ('val', 'i4')])\nprint(recs['name'])    # ['A' 'B']",
        "usecase": "Tabular workloads that need NumPy speed with heterogeneous columns — a lightweight alternative to dragging in a DataFrame.",
        "category": "numpy"
    },
    {
        "id": 50,
        "title": "checking for NaN poisoning",
        "definition": "np.isnan flags NaN slots in one fast pass, and np.isclose compares values with floating-point tolerance instead of brittle equality. Sanitizing data before statistics or fitting — replacing or dropping NaN positions — is the guard that stops silent errors from propagating.",
        "example": "bad = np.isnan(data)\ndata[bad] = np.nanmedian(data)   # replace, don't crash\nnp.isclose(a, b)                  # tolerance-aware compare",
        "usecase": "Sanitizing data before stats or model fitting so NaN or rounding issues never quietly corrupt results.",
        "category": "numpy"
    }
]
