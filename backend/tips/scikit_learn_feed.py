TIPS = [
    {
        "id": 1,
        "title": "Data straight from sklearn",
        "definition": "sklearn.datasets ships canonical, ready-to-load datasets — iris, digits, wine, breast cancer and more — with features, targets and metadata already separated. load_iris(as_frame=True) even returns a tidy pandas frame. It is real, curated data for prototyping and benchmarking without hunting for CSVs.",
        "example": "from sklearn.datasets import load_iris\niris = load_iris(as_frame=True)\ndf = iris.frame\ny = iris.target",
        "usecase": "Prototyping and benchmarks — established data with known good results, ideal for checking your pipeline before real data arrives.",
        "category": "scikit-learn"
    },
    {
        "id": 2,
        "title": "train_test_split is sacred",
        "definition": "train_test_split shuffles and carves the data into training and test parts, so the model fits on one slice and is judged on rows it never saw. The random_state argument makes that split reproducible. Never evaluate on the same rows you trained on — that number is fiction.",
        "example": "from sklearn.model_selection import train_test_split\nX_tr, X_te, y_tr, y_te = train_test_split(\n    X, y, test_size=0.2, random_state=42)",
        "usecase": "Every ML project — honest generalization numbers start with a clean split, and any score on training data is a lie.",
        "category": "scikit-learn"
    },
    {
        "id": 3,
        "title": "stratify keeps balance",
        "definition": "stratify=y tells train_test_split to preserve each class's proportion in both the training and test slices. On skewed data like fraud, a random split can easily leave the test set with zero rare-class rows, producing meaningless results — stratification prevents that before it happens.",
        "example": "X_tr, X_te, y_tr, y_te = train_test_split(\n    X, y, stratify=y, test_size=0.2)",
        "usecase": "99/1 fraud data: without stratification the test set might contain zero fraud rows — stratified splits keep rare classes represented.",
        "category": "scikit-learn"
    },
    {
        "id": 4,
        "title": "StandardScaler — the default preprocessor",
        "definition": "StandardScaler centers every feature at a mean of 0 with unit variance, so no single column dominates because of its units. Distance-based and regularized models compute similarity or penalties across features, and wildly different scales silently distort both — scaling is the prerequisite.",
        "example": "from sklearn.preprocessing import StandardScaler\nX_s = StandardScaler().fit_transform(X)",
        "usecase": "KNN, SVM, PCA and any model using distances or regularization expect scaled features — the default first step for tabular pipelines.",
        "category": "scikit-learn"
    },
    {
        "id": 5,
        "title": "MinMaxScaler for bounded ranges",
        "definition": "MinMaxScaler compresses every feature into a fixed interval, [0, 1] by default, using the column's observed minimum and maximum. Unlike normalization to unit variance, it preserves the exact shape of the distribution while guaranteeing a bounded output for every value.",
        "example": "from sklearn.preprocessing import MinMaxScaler\nX_s = MinMaxScaler().fit_transform(X)   # all values in [0, 1]",
        "usecase": "Neural nets and image pipelines that expect inputs in a fixed range — bounded inputs keep activation functions in their sane region.",
        "category": "scikit-learn"
    },
    {
        "id": 6,
        "title": "Pipelines: one object, no leakage",
        "definition": "Pipeline chains a preprocessing step with an estimator into one object whose fit() and predict() run both in sequence. Inside cross-validation, the scaler fits on the training fold only, so test folds never influence the transform — the clean fix for the classic data-leakage bug.",
        "example": "from sklearn.pipeline import Pipeline\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.svm import SVC\npipe = Pipeline([(\"scale\", StandardScaler()), (\"svm\", SVC())])",
        "usecase": "Scaler fits on train folds only, preventing the most common subtle leakage bug that inflates cross-validation scores.",
        "category": "scikit-learn"
    },
    {
        "id": 7,
        "title": "LinearRegression in one line",
        "definition": "LinearRegression fits y = w·x + b by ordinary least squares — minimizing summed squared error over the training rows — and learns a weight per feature plus a bias. Its .predict() then maps new rows to continuous values, and the coefficients double as interpretable directional effects.",
        "example": "from sklearn.linear_model import LinearRegression\nreg = LinearRegression().fit(X, y)\npreds = reg.predict(X_new)\nprint(reg.coef_)",
        "usecase": "Sales forecasts, price estimates and any continuous-target baseline — the fastest way to a working regression and a readable one.",
        "category": "scikit-learn"
    },
    {
        "id": 8,
        "title": "LogisticRegression for classification",
        "definition": "Despite the name it is a classifier: it models the log-odds of the positive class as a linear function, squashes them through sigmoid into a probability, and applies a threshold to decide the label. Predictions come out as interpretable probabilities with feature weight coefficients.",
        "example": "from sklearn.linear_model import LogisticRegression\nclf = LogisticRegression(max_iter=1000).fit(X, y)\nclf.predict_proba(X_new)",
        "usecase": "Spam, churn and click-through where you want calibrated probabilities and per-feature effects — not just a black-box label.",
        "category": "scikit-learn"
    },
    {
        "id": 9,
        "title": "Decision trees are readable",
        "definition": "Decision trees greedily split the data on single features, choosing the thresholds that best separate classes, and repeat until the depth cap. The result is a chain of if-else rules you can open and inspect — export_text prints the whole model as readable, auditable logic.",
        "example": "from sklearn.tree import DecisionTreeClassifier, export_text\nclf = DecisionTreeClassifier(max_depth=4).fit(X, y)\nprint(export_text(clf, feature_names=list(iris.feature_names)))",
        "usecase": "Credit rules and audits where stakeholders demand explainable decisions — a shallow tree is a model a human can actually read.",
        "category": "scikit-learn"
    },
    {
        "id": 10,
        "title": "Random forests beat single trees",
        "definition": "A random forest trains hundreds of slightly randomized trees — each on a bootstrapped sample with a random feature subset — then averages their votes. The averaging cancels most of an individual tree's variance, which is why forests are far more accurate and stable than any single tree.",
        "example": "from sklearn.ensemble import RandomForestClassifier\nclf = RandomForestClassifier(n_estimators=200, n_jobs=-1).fit(X, y)",
        "usecase": "A strong default classifier on tabular data — sparse tuning, solid accuracy, feature importances for free.",
        "category": "scikit-learn"
    },
    {
        "id": 11,
        "title": "Gradient boosting essentials",
        "definition": "Gradient boosting trains trees sequentially, each one fitted to the residual errors of the ensemble so far — later trees clean up what earlier trees got wrong. With a small learning_rate it is among the most accurate tabular algorithms, but it rewards tuning and punishes overfitting more than forests.",
        "example": "from sklearn.ensemble import GradientBoostingClassifier\nclf = GradientBoostingClassifier(\n    n_estimators=100, learning_rate=0.1).fit(X, y)",
        "usecase": "Kaggle-grade wins on structured data — powerful enough to dominate, careful enough to demand validation discipline.",
        "category": "scikit-learn"
    },
    {
        "id": 12,
        "title": "SVC for max-margin classification",
        "definition": "SVC finds the decision boundary that leaves the widest possible margin around it, regularized by the cost parameter C. The rbf kernel projects data into a higher-dimensional space, letting the linear-margin idea fit curved boundaries without explicitly computing the projection.",
        "example": "from sklearn.svm import SVC\nclf = SVC(kernel='rbf', C=1.0).fit(X, y)",
        "usecase": "Small and medium datasets where a clean, robust decision boundary beats complex ensembles — and where features are well scaled.",
        "category": "scikit-learn"
    },
    {
        "id": 13,
        "title": "KNN — no training at all",
        "definition": "KNeighborsClassifier stores the training set and, at prediction time, finds the k closest stored points to each query and takes a majority vote. There is no learned model in the usual sense — just distance. Simpler, but every prediction scans the data and inherits its scale sensitivity.",
        "example": "from sklearn.neighbors import KNeighborsClassifier\nclf = KNeighborsClassifier(n_neighbors=5).fit(X, y)",
        "usecase": "Recommendation engines, small datasets and instant baselines before heavier models — no training phase, instant updates.",
        "category": "scikit-learn"
    },
    {
        "id": 14,
        "title": "Naive Bayes for text",
        "definition": "MultinomialNB and GaussianNB apply Bayes' rule while assuming the features are independent — a simplification that is rarely true yet works surprisingly well. MultinomialNB's word-count model makes it a staple for text classification, training quickly even on very high-dimensional vocabularies.",
        "example": "from sklearn.naive_bayes import MultinomialNB\nclf = MultinomialNB().fit(X_train_tfidf, y_train)",
        "usecase": "Spam detection, document tagging and sentiment where word counts dominate — simple, fast and strong on text.",
        "category": "scikit-learn"
    },
    {
        "id": 15,
        "title": "accuracy_score in four chars",
        "definition": "accuracy_score returns the fraction of predictions that exactly match the true labels — the most basic quality read on a classifier. On balanced data it is informative; on skewed data a model predicting the majority class sails past 99% without learning anything.",
        "example": "from sklearn.metrics import accuracy_score\nacc = accuracy_score(y_true, y_pred)\nprint(acc)",
        "usecase": "Quick sanity checks and symmetric-class problems — pair it with precision and recall whenever one class is rare.",
        "category": "scikit-learn"
    },
    {
        "id": 16,
        "title": "classification_report summarizes everything",
        "definition": "classification_report prints one line per class with precision, recall, F1 score and support, then a macro and weighted average plus overall accuracy. It is the fastest way to see how the model treats each class — where it is precise, where it misses, and how rare classes fare.",
        "example": "from sklearn.metrics import classification_report\nprint(classification_report(y_true, y_pred))",
        "usecase": "The first thing you run after any classifier — a class-by-class breakdown that exposes exactly where the model fails.",
        "category": "scikit-learn"
    },
    {
        "id": 17,
        "title": "confusion_matrix, the failure map",
        "definition": "A confusion matrix lays errors out as a grid: rows are true labels, columns are predictions, and the diagonals are correct hits. Strong off-diagonal cells reveal systematic mixes — maybe '8' keeps being read as '3' — and ConfusionMatrixDisplay plots it for instant human inspection.",
        "example": "from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay\ncm = confusion_matrix(y_true, y_pred)\nConfusionMatrixDisplay(cm).plot()",
        "usecase": "Finding the systematic confusions behind a low score — which classes get mixed up and where more data will help.",
        "category": "scikit-learn"
    },
    {
        "id": 18,
        "title": "cross_val_score, trust the folds",
        "definition": "cross_val_score trains and evaluates a model k times on different train/test folds, returning one score per fold. Averaging those estimates gives a far more honest picture of generalization than a single split — small datasets can swing wildly depending on which rows land in the test slice.",
        "example": "from sklearn.model_selection import cross_val_score\nscores = cross_val_score(clf, X, y, cv=5, scoring='accuracy')\nprint(scores.mean(), scores.std())",
        "usecase": "Model selection on small data — a single holdout split is too noisy, and CV turns one guess into a stable estimate.",
        "category": "scikit-learn"
    },
    {
        "id": 19,
        "title": "GridSearchCV, tuning on rails",
        "definition": "GridSearchCV exhaustively trains the estimator on every combination in a hyperparameter grid, each evaluated by cross-validation, and keeps the best performer. Pipe parameters use double-underscore syntax (svc__C) so preprocessing knobs tune alongside model ones in one coordinated sweep.",
        "example": "from sklearn.model_selection import GridSearchCV\ngrid = {'C': [0.1, 1, 10], 'gamma': [0.01, 0.1]}\nsearch = GridSearchCV(SVC(), grid, cv=5).fit(X, y)\nprint(search.best_params_)",
        "usecase": "Finding the best hyperparameters when the space is small enough to exhaust — systematic, cross-validated and reproducible.",
        "category": "scikit-learn"
    },
    {
        "id": 20,
        "title": "RandomizedSearchCV for big spaces",
        "definition": "RandomizedSearchCV draws a fixed number of random hyperparameter combinations from your distributions instead of testing every one. When a grid would take days, sampling a few hundred well-chosen points finds a near-best model in a fraction of the compute — and covers the space more broadly.",
        "example": "from sklearn.model_selection import RandomizedSearchCV\nsearch = RandomizedSearchCV(clf, params, n_iter=50, cv=5)\nsearch.fit(X, y)",
        "usecase": "Huge parameter spaces where an exhaustive grid would run for days — random sampling gets most of the benefit at a fraction of the cost.",
        "category": "scikit-learn"
    },
    {
        "id": 21,
        "title": "feature_importances_ for trees",
        "definition": "Tree-based models track how much each feature reduces impurity across all their splits, and expose that as feature_importances_. Larger values mean the feature drives more of the model's decisions — an ordering that doubles as a feature-selection and explainability tool.",
        "example": "import numpy as np\nimp = clf.feature_importances_\norder = np.argsort(imp)[::-1]\nprint([feature_names[i] for i in order[:5]])",
        "usecase": "Feature selection, model explainability and deciding what data to collect more of — straight from the fitted forest.",
        "category": "scikit-learn"
    },
    {
        "id": 22,
        "title": "KMeans, clustering in one call",
        "definition": "KMeans partitions data into k clusters by iteratively assigning points to the nearest centroid and moving centroids to their members' mean until stable. The result splits the data into k groups whose internal distances are minimized — no labels required, pure structure discovery.",
        "example": "from sklearn.cluster import KMeans\nkmeans = KMeans(n_clusters=4, n_init=10, random_state=42).fit(X)\nlabels = kmeans.labels_",
        "usecase": "Customer segmentation, image compression and anomaly flags — find groups in unlabeled data, then label or act on them.",
        "category": "scikit-learn"
    },
    {
        "id": 23,
        "title": "PCA, dimensions without tears",
        "definition": "Principal component analysis finds the orthogonal directions that hold the most variance in your data and projects points onto the top few of them. Dimensionality collapses — hundreds of features into two or ten — while most of the signal survives, speeding models and enabling plots.",
        "example": "from sklearn.decomposition import PCA\nproj = PCA(n_components=2).fit_transform(X)   # to 2D for plotting\nprint(proj.shape)",
        "usecase": "Visualizing high-dimensional data in 2D and shrinking feature counts before distance-based or heavy downstream models.",
        "category": "scikit-learn"
    },
    {
        "id": 24,
        "title": "predict_proba, probability outputs",
        "definition": "Many classifiers expose predict_proba returning, per row, the estimated probability of each class instead of just the winning label. That continuous score enables ranking by risk, threshold tuning and informed decisions — a model ranked by true risk beats one judged on hard 0/1 guesses.",
        "example": "proba = clf.predict_proba(X)[:, 1]    # P(class=1) per row\norder = proba.argsort()[::-1]          # rank most likely first",
        "usecase": "Ranking by risk, threshold tuning and calibrated decisions — the probability is where the model's information actually lives.",
        "category": "scikit-learn"
    },
    {
        "id": 25,
        "title": "random_state, reproducibility for free",
        "definition": "Passing random_state pins the random draws of splits and algorithms, making the exact same numbers appear on every run. Models, folds and preprocessing become reproducible — the same code, the same seed, the same results, on any machine.",
        "example": "X_train, X_test, y_train, y_test = train_test_split(\n    X, y, test_size=0.2, random_state=42)",
        "usecase": "Replicating experiments and debugging — your teammate reproduces your exact numbers instead of chasing a moving target.",
        "category": "scikit-learn"
    },
    {
        "id": 26,
        "title": "SimpleImputer for missing values",
        "definition": "SimpleImputer replaces missing values with a fill strategy fitted on the training data — mean, median or most_frequent. It fits on X (train) and transforms X (test) the same way, so gaps in any later dataset get the exact same fill the model was trained to expect.",
        "example": "from sklearn.impute import SimpleImputer\nimputer = SimpleImputer(strategy='median').fit(X)\nX_clean = imputer.transform(X)",
        "usecase": "Real-world data is riddled with missing values — impute before you train so models never encounter NaN gaps.",
        "category": "scikit-learn"
    },
    {
        "id": 27,
        "title": "OneHotEncoder turns categories into columns",
        "definition": "OneHotEncoder converts each categorical value into its own binary 0/1 column, so city names or colors become numeric features without implying any false ordering. handle_unknown='ignore' keeps unseen categories at prediction time from crashing the model by mapping them to all-zero rows.",
        "example": "from sklearn.preprocessing import OneHotEncoder\nohe = OneHotEncoder(handle_unknown='ignore')\nX_cat = ohe.fit_transform(df[['city']])",
        "usecase": "Feeding text categories like city, color or country into models that only understand numbers — one column per distinct value.",
        "category": "scikit-learn"
    },
    {
        "id": 28,
        "title": "LabelEncoder only for targets",
        "definition": "LabelEncoder maps string labels to integers 0..n-1 — perfect for turning class names into the y a classifier expects. As an encoder for features it is usually a mistake: imposing 0,1,2 ordering on unordered categories teaches nonsense distances, which is what OneHotEncoder is for.",
        "example": "from sklearn.preprocessing import LabelEncoder\nle = LabelEncoder().fit(y)\ny_num = le.transform(y)\ny_back = le.inverse_transform(y_num)",
        "usecase": "Turning class names into integer labels before classification training — and decoding predicted integers back to names.",
        "category": "scikit-learn"
    },
    {
        "id": 29,
        "title": "ColumnTransformer for mixed data",
        "definition": "ColumnTransformer routes different column sets through different transformers inside one object: numeric columns to a scaler, categorical columns to an encoder, in a single fit/transform call. Mixed tables get each column type treated correctly while staying leakage-safe inside a pipeline.",
        "example": "from sklearn.compose import ColumnTransformer\nfrom sklearn.preprocessing import StandardScaler, OneHotEncoder\nct = ColumnTransformer([\n    ('num', StandardScaler(), ['age', 'income']),\n    ('cat', OneHotEncoder(), ['city']),\n])",
        "usecase": "Tables mixing numbers and categories — scale the numerics, encode the categories, and keep both steps one composable object.",
        "category": "scikit-learn"
    },
    {
        "id": 30,
        "title": "roc_auc_score, the ranking metric",
        "definition": "roc_auc_score measures how well a model ranks positives above negatives, ignoring thresholds entirely: 1.0 is perfect separation, 0.5 is random guessing. It evaluates the ordering the probabilities produce, not the labels a hard cutoff happens to output — ideal when you can act on rank.",
        "example": "from sklearn.metrics import roc_auc_score\nauc = roc_auc_score(y_true, clf.predict_proba(X)[:, 1])\nprint(auc)",
        "usecase": "Comparing classifiers where you care about ranking — fraud triage, click probability, risk scoring — rather than one threshold.",
        "category": "scikit-learn"
    },
    {
        "id": 31,
        "title": "joblib persists models",
        "definition": "joblib.dump writes a trained estimator to a single binary file, and joblib.load restores it into a working object. Everything the model needs — coefficients, trees, learned preprocessing parameters — comes back intact, so a model trained overnight serves predictions all day without retraining.",
        "example": "import joblib\njoblib.dump(clf, 'model.joblib')\nclf = joblib.load('model.joblib')\npreds = clf.predict(X_new)",
        "usecase": "Train once, serve forever — save the fitted model, then reload it inside an API or nightly batch job.",
        "category": "scikit-learn"
    },
    {
        "id": 32,
        "title": "DummyClassifier, the honest baseline",
        "definition": "DummyClassifier ignores features and always predicts the most frequent class (or another trivial strategy). Its score is the floor every real model must beat — if your AUC, precision or accuracy isn't above the dummy's, your features carry no signal at all.",
        "example": "from sklearn.dummy import DummyClassifier\nfrom sklearn.metrics import accuracy_score\ndummy = DummyClassifier(strategy='most_frequent').fit(X_train, y_train)\nacc = accuracy_score(y_test, dummy.predict(X_test))",
        "usecase": "Knowing if your model is actually learning or merely guessing the majority class — the baseline every result must beat.",
        "category": "scikit-learn"
    },
    {
        "id": 33,
        "title": "Ridge vs Lasso vs ElasticNet",
        "definition": "Ridge applies L2 regularization, shrinking all weights toward zero; Lasso applies L1, which drives some weights to exactly zero for sparse models; ElasticNet blends both. Each trades bias against variance differently, and the alpha parameter controls how hard the penalty bites.",
        "example": "from sklearn.linear_model import Ridge, Lasso, ElasticNet\nmodels = {\n    'ridge': Ridge(alpha=1.0),\n    'lasso': Lasso(alpha=0.01),\n    'enet': ElasticNet(alpha=0.01),\n}",
        "usecase": "Feature-dense regression — L1 and elastic net automatically pick a few informative columns, shrinking the rest to zero.",
        "category": "scikit-learn"
    },
    {
        "id": 34,
        "title": "SGDClassifier for huge datasets",
        "definition": "SGDClassifier trains a linear model with stochastic gradient descent, processing examples one at a time in mini-batches. Unlike batch solvers it never loads the whole dataset at once, so it can chew through millions of rows — and it stops when the loss converges across its max_iter passes.",
        "example": "from sklearn.linear_model import SGDClassifier\nclf = SGDClassifier(loss='log_loss', max_iter=1000).fit(X, y)",
        "usecase": "Clickstream and web-scale data that won't fit in memory — linear performance on millions of rows without loading them all.",
        "category": "scikit-learn"
    },
    {
        "id": 35,
        "title": "partial_fit for online learning",
        "definition": "partial_fit updates an already-fitted model incrementally with one new batch at a time — no retraining on the full history. Streams of events, sensor readings or user clicks keep the model current without memory growth or downtime, and the classes= argument tells the first call the full label set.",
        "example": "clf = SGDClassifier()\nfor batch_X, batch_y in data_stream:\n    clf.partial_fit(batch_X, batch_y, classes=[0, 1])",
        "usecase": "Models that must keep learning from a perpetual stream of new events — churn, fraud or trend shifts — without full retrains.",
        "category": "scikit-learn"
    },
    {
        "id": 36,
        "title": "PolynomialFeatures for curves",
        "definition": "PolynomialFeatures augments the feature matrix with powers and interaction terms — x², x³, x·z — so a linear model can fit curved relationships. Lines become parabolas, and feature interactions surface automatically; that flexibility trades directly against degrees of freedom and overfitting risk.",
        "example": "from sklearn.preprocessing import PolynomialFeatures\nfrom sklearn.linear_model import LinearRegression\npoly = PolynomialFeatures(degree=2, include_bias=False)\nX_p = poly.fit_transform(X)\nreg = LinearRegression().fit(X_p, y)",
        "usecase": "Trend lines with curvature and feature interactions — capturing non-linear shape without installing a gradient-boosted forest.",
        "category": "scikit-learn"
    },
    {
        "id": 37,
        "title": "CalibratedClassifierCV, honest probabilities",
        "definition": "CalibratedClassifierCV rescales a classifier's raw scores into well-calibrated probabilities: a 0.8 prediction actually comes true 80% of the time. Built on cross-validation folds to stay honest, it wraps estimators like SVC whose raw decisions are strong but whose probabilities are poorly scaled.",
        "example": "from sklearn.calibration import CalibratedClassifierCV\nclf = CalibratedClassifierCV(SVC(probability=False)).fit(X, y)\nproba = clf.predict_proba(X_new)",
        "usecase": "Models where the probability — not just the label — drives a decision, like risk gates that need trustworthy confidence values.",
        "category": "scikit-learn"
    },
    {
        "id": 38,
        "title": "permutation_importance removes bias",
        "definition": "permutation_importance shuffles one feature's values at a time, measures how much the model's score drops, and repeats to average out noise. It is model-agnostic and tells you which inputs genuinely matter to predictions — unlike tree feature_importances_, which can be biased toward high-cardinality columns.",
        "example": "from sklearn.inspection import permutation_importance\nimp = permutation_importance(clf, X_test, y_test, n_repeats=10)\nprint(imp.importances_mean)",
        "usecase": "Fair feature importance for any estimator — forest, SVM or logistic model alike — when you need trustworthy attribution.",
        "category": "scikit-learn"
    },
    {
        "id": 39,
        "title": "Learning curves diagnose fit",
        "definition": "learning_curve trains the model on increasing slices of the data and records train and validation scores at each size. Plotting those curves separates the two failure modes: a big train/validation gap says high variance (add data), while a low flat plateau says high bias (add model capacity).",
        "example": "from sklearn.model_selection import learning_curve\nsizes, train_scores, val_scores = learning_curve(\n    clf, X, y, cv=5, train_sizes=[0.2, 0.4, 0.6, 0.8, 1.0])",
        "usecase": "Deciding whether more data or a stronger model is the right next investment — one plot answers both directions.",
        "category": "scikit-learn"
    },
    {
        "id": 40,
        "title": "Pipelines + GridSearch, combined power",
        "definition": "Wrapping preprocessing and model in a Pipeline lets GridSearchCV tune both together, with the double-underscore syntax targeting each stage's parameters — svc__C and scaler__with_mean in the same sweep. Every cross-validation fold fits the transformer inside the fold, so tuning never leaks test knowledge.",
        "example": "from sklearn.pipeline import Pipeline\nfrom sklearn.svm import SVC\nfrom sklearn.model_selection import GridSearchCV\npipe = Pipeline([('scaler', StandardScaler()), ('svc', SVC())])\nsearch = GridSearchCV(pipe, {'svc__C': [0.1, 1, 10]}, cv=5)",
        "usecase": "Tuning preprocessing and model in one leakage-safe sweep — the professional workflow for every structured-data project.",
        "category": "scikit-learn"
    },
    {
        "id": 41,
        "title": "StandardScaler inside CV only",
        "definition": "The scaler must learn its mean and variance from training folds alone; fitting it on all data first leaks test information into every fold and inflates scores. Putting the scaler inside a pipeline or applyng the fit-then-transform pattern — fit on train, transform test — keeps the estimate honest.",
        "example": "from sklearn.pipeline import make_pipeline\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.linear_model import LogisticRegression\npipe = make_pipeline(StandardScaler(), LogisticRegression())\ncross_val_score(pipe, X, y, cv=5)",
        "usecase": "Getting honest cross-validation numbers instead of optimistically biased ones — the scaler never sees the test folds.",
        "category": "scikit-learn"
    },
    {
        "id": 42,
        "title": "LabelBinarizer for multi-label",
        "definition": "LabelBinarizer encodes a label column into one-hot rows: each class becomes its own binary column, with a 1 marking the class present. Its output matches what neural networks and multi-class losses consume, and the class count is derived automatically from the fitted data.",
        "example": "from sklearn.preprocessing import LabelBinarizer\nlb = LabelBinarizer()\nY = lb.fit_transform(y)   # n rows x k class columns\nprint(lb.classes_)",
        "usecase": "Mutually exclusive classes converted into binary vectors before feeding a categorical cross-entropy head.",
        "category": "scikit-learn"
    },
    {
        "id": 43,
        "title": "ROC curves are a picture",
        "definition": "roc_curve sweeps every possible classification threshold and plots the true-positive rate against the false-positive rate at each one; the area under that curve is the AUC. It shows the whole trade-off landscape — how catching more positives forces more false alarms — in a single view.",
        "example": "from sklearn.metrics import roc_curve\nfpr, tpr, thresholds = roc_curve(y_true, scores)\nimport matplotlib.pyplot as plt\nplt.plot(fpr, tpr)\nplt.xlabel('False positive rate')\nplt.ylabel('True positive rate')",
        "usecase": "Visualizing the balance between catching positives and absorbing false alarms — and seeing where your model beats the diagonal.",
        "category": "scikit-learn"
    },
    {
        "id": 44,
        "title": "Imbalance? Use class_weight",
        "definition": "class_weight='balanced' automatically upweights the rare class in inverse proportion to its frequency, so losing that class costs the loss proportionally more. The model stops winning by predicting the majority for everything — a one-argument fix for skewed targets.",
        "example": "from sklearn.linear_model import LogisticRegression\nclf = LogisticRegression(class_weight='balanced').fit(X, y)",
        "usecase": "Fraud, rare-disease or defect detection where positives are 1% of data — rebalance the loss without resampling a single row.",
        "category": "scikit-learn"
    },
    {
        "id": 45,
        "title": "fit_transform vs fit then transform",
        "definition": "fit_transform computes the transformer's parameters and applies it in one go, meant for training data. On test data you only transform — fit on train once, then reuse those exact parameters. Refitting the transformer on test rows quietly leaks test information into the model's scores.",
        "example": "scaler.fit(X_train)\nX_tr = scaler.transform(X_train)\nX_te = scaler.transform(X_test)   # never fit again on test",
        "usecase": "The single most common leakage bug in ML — transformers learn their parameters from training data and stay frozen for test.",
        "category": "scikit-learn"
    },
    {
        "id": 46,
        "title": "Random forests don't need scaling",
        "definition": "Trees split data on single feature thresholds, so monotonic transforms like scaling change nothing about their decisions — each split compares within one column. Forests are therefore happy on raw values, which removes entire preprocessing stages and suits them to messy, mixed-scale tabular data.",
        "example": "from sklearn.ensemble import RandomForestClassifier\nclf = RandomForestClassifier(n_estimators=300).fit(X, y)\n# raw units, unnormalized — perfectly fine",
        "usecase": "Fewer preprocessing steps — one reason forests shine on messy tabular data straight out of a spreadsheet.",
        "category": "scikit-learn"
    },
    {
        "id": 47,
        "title": "SMOTE for resampling",
        "definition": "imbalanced-learn's SMOTE synthesizes new minority-class samples from the existing ones — interpolating between neighbors — to balance the training distribution. Unlike duplication it adds variety, and logging, evaluation and validation must still use the untouched test set so scores stay honest.",
        "example": "from imblearn.over_sampling import SMOTE\nfrom sklearn.model_selection import train_test_split\nX_tr, X_te, y_tr, y_te = train_test_split(X, y, stratify=y, test_size=0.2)\nX_r, y_r = SMOTE().fit_resample(X_tr, y_tr)",
        "usecase": "Oversampling the rare class on the training split only — worth combining with class_weight when the class is very rare.",
        "category": "scikit-learn"
    },
    {
        "id": 48,
        "title": "train_test_split shuffle keeps order",
        "definition": "By default train_test_split shuffles before slicing — which destroys temporal order and lets future rows leak into the training past. For time-series data set shuffle=False so the split is a clean chronological cut; evaluating on the future needs the future to stay unseen.",
        "example": "X_tr, X_te, y_tr, y_te = train_test_split(\n    X, y, shuffle=False, test_size=0.2)",
        "usecase": "Time-series evaluation — shuffling would smear future observations through the training window and fake the forecast result.",
        "category": "scikit-learn"
    },
    {
        "id": 49,
        "title": "Cross-validation strategy for time",
        "definition": "TimeSeriesSplit creates folds chronologically: each training fold contains only past rows and each validation fold is strictly after it. That respects causality, revealing how a model truly performs on data it has never been allowed to see in the past — unlike random KFold shuffling.",
        "example": "from sklearn.model_selection import TimeSeriesSplit, cross_val_score\nscores = cross_val_score(clf, X, y, cv=TimeSeriesSplit(5))\nprint(scores)",
        "usecase": "Forecasting and backtesting — the only honest evaluation for sequential data where the past must never know the future.",
        "category": "scikit-learn"
    },
    {
        "id": 50,
        "title": "Precision/recall threshold trade-off",
        "definition": "Classification thresholds turn probabilities into labels, and moving it swings precision versus recall: raise it and only confident positives pass (high precision, low recall); lower it and you catch more (high recall, less precision). precision_recall_curve plots every operating point so you pick the right one.",
        "example": "from sklearn.metrics import precision_recall_curve\nprecisions, recalls, thresholds = precision_recall_curve(y_true, scores)\n# find threshold where precision >= 0.9:\nidx = next(i for i, p in enumerate(precisions) if p >= 0.9)",
        "usecase": "Choosing the operating point that matches the business — a stricter production gate versus catching every possible case.",
        "category": "scikit-learn"
    }
]
