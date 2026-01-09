# Conocimientos Técnicos Difíciles: Data Analytics

## Objetivo
Temas complejos del día a día de análisis de datos que un arquitecto debe dominar para apoyar efectivamente a analistas de datos.

---

## CATEGORÍA 1: SQL Avanzado

### 1.1 Window Functions y Analytics
**Dificultad:** ⭐⭐⭐⭐⭐

```sql
-- 1. Running totals y cumulative sums
SELECT
    date,
    revenue,
    SUM(revenue) OVER (ORDER BY date) AS cumulative_revenue,
    AVG(revenue) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS moving_avg_7days
FROM daily_sales;

-- 2. Ranking (diferencias importantes!)
SELECT
    product_name,
    category,
    sales,
    -- ROW_NUMBER: unique ranks (1,2,3,4,5...)
    ROW_NUMBER() OVER (PARTITION BY category ORDER BY sales DESC) AS row_num,

    -- RANK: gaps for ties (1,2,2,4,5...)
    RANK() OVER (PARTITION BY category ORDER BY sales DESC) AS rank,

    -- DENSE_RANK: no gaps (1,2,2,3,4...)
    DENSE_RANK() OVER (PARTITION BY category ORDER BY sales DESC) AS dense_rank,

    -- NTILE: divide en N grupos
    NTILE(4) OVER (ORDER BY sales DESC) AS quartile
FROM products;

-- 3. LAG y LEAD (comparar con filas anteriores/siguientes)
SELECT
    date,
    revenue,
    -- Revenue del día anterior
    LAG(revenue, 1) OVER (ORDER BY date) AS prev_day_revenue,

    -- Growth vs día anterior
    revenue - LAG(revenue, 1) OVER (ORDER BY date) AS day_over_day_growth,

    -- Porcentaje de crecimiento
    ROUND(
        100.0 * (revenue - LAG(revenue, 1) OVER (ORDER BY date)) /
        NULLIF(LAG(revenue, 1) OVER (ORDER BY date), 0),
        2
    ) AS pct_change,

    -- Revenue del día siguiente (forecast validation)
    LEAD(revenue, 1) OVER (ORDER BY date) AS next_day_revenue
FROM daily_sales;

-- 4. FIRST_VALUE y LAST_VALUE
SELECT
    employee_id,
    department,
    salary,
    hire_date,

    -- Primer empleado contratado en departamento
    FIRST_VALUE(employee_id) OVER (
        PARTITION BY department
        ORDER BY hire_date
    ) AS first_hire,

    -- Último empleado contratado
    LAST_VALUE(employee_id) OVER (
        PARTITION BY department
        ORDER BY hire_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS last_hire,

    -- Salario más alto en departamento
    MAX(salary) OVER (PARTITION BY department) AS max_dept_salary
FROM employees;

-- 5. Cohort Analysis
WITH user_cohorts AS (
    SELECT
        user_id,
        DATE_TRUNC('month', MIN(order_date)) AS cohort_month
    FROM orders
    GROUP BY user_id
),
cohort_activity AS (
    SELECT
        c.cohort_month,
        DATE_TRUNC('month', o.order_date) AS activity_month,
        COUNT(DISTINCT o.user_id) AS active_users
    FROM user_cohorts c
    JOIN orders o ON c.user_id = o.user_id
    GROUP BY c.cohort_month, DATE_TRUNC('month', o.order_date)
)
SELECT
    cohort_month,
    activity_month,
    active_users,
    -- Months since cohort start
    EXTRACT(YEAR FROM age(activity_month, cohort_month)) * 12 +
    EXTRACT(MONTH FROM age(activity_month, cohort_month)) AS month_number,

    -- Retention rate
    100.0 * active_users / FIRST_VALUE(active_users) OVER (
        PARTITION BY cohort_month
        ORDER BY activity_month
    ) AS retention_rate
FROM cohort_activity
ORDER BY cohort_month, activity_month;

-- 6. Percentiles y Distribution Analysis
SELECT
    product_category,

    -- Quartiles
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY price) AS p25,
    PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY price) AS median,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY price) AS p75,

    -- Outlier detection (IQR method)
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY price) +
    1.5 * (
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY price) -
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY price)
    ) AS outlier_threshold
FROM products
GROUP BY product_category;

-- 7. Time Series Gaps y Missing Dates
WITH date_series AS (
    SELECT generate_series(
        '2024-01-01'::date,
        '2024-12-31'::date,
        '1 day'::interval
    )::date AS date
)
SELECT
    ds.date,
    COALESCE(s.revenue, 0) AS revenue,
    -- Fill forward (última observación)
    LAST_VALUE(s.revenue) IGNORE NULLS OVER (
        ORDER BY ds.date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS revenue_filled
FROM date_series ds
LEFT JOIN sales s ON ds.date = s.date
ORDER BY ds.date;
```

---

### 1.2 CTEs y Recursive Queries
**Dificultad:** ⭐⭐⭐⭐⭐

```sql
-- 1. Hierarchical Data (org chart, categories)
WITH RECURSIVE org_hierarchy AS (
    -- Base case: CEO
    SELECT
        employee_id,
        name,
        manager_id,
        1 AS level,
        name::TEXT AS path,
        ARRAY[employee_id] AS path_ids
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- Recursive case: subordinates
    SELECT
        e.employee_id,
        e.name,
        e.manager_id,
        oh.level + 1,
        oh.path || ' > ' || e.name,
        oh.path_ids || e.employee_id
    FROM employees e
    JOIN org_hierarchy oh ON e.manager_id = oh.employee_id
)
SELECT
    employee_id,
    name,
    level,
    path,
    -- Count direct reports
    (
        SELECT COUNT(*)
        FROM org_hierarchy oh2
        WHERE oh2.manager_id = oh1.employee_id
    ) AS direct_reports,

    -- Count total reports (recursive)
    (
        SELECT COUNT(*)
        FROM org_hierarchy oh3
        WHERE oh1.employee_id = ANY(oh3.path_ids[1:array_length(oh3.path_ids, 1)-1])
    ) AS total_reports
FROM org_hierarchy oh1
ORDER BY path;

-- 2. Graph Traversal (social network, product recommendations)
WITH RECURSIVE friend_network AS (
    -- Starting user
    SELECT
        user_id,
        friend_id,
        1 AS degree,
        ARRAY[user_id] AS path
    FROM friendships
    WHERE user_id = 123

    UNION

    -- Friends of friends (up to 3 degrees)
    SELECT
        f.user_id,
        f.friend_id,
        fn.degree + 1,
        fn.path || f.user_id
    FROM friendships f
    JOIN friend_network fn ON f.user_id = fn.friend_id
    WHERE
        fn.degree < 3
        AND NOT (f.user_id = ANY(fn.path))  -- Avoid cycles
)
SELECT
    friend_id,
    MIN(degree) AS min_degree,
    COUNT(*) AS connection_count
FROM friend_network
GROUP BY friend_id
ORDER BY min_degree, connection_count DESC;

-- 3. Time Series Aggregation (complejo)
WITH RECURSIVE time_buckets AS (
    SELECT
        '2024-01-01 00:00:00'::TIMESTAMP AS bucket_start,
        '2024-01-01 01:00:00'::TIMESTAMP AS bucket_end

    UNION ALL

    SELECT
        bucket_end,
        bucket_end + INTERVAL '1 hour'
    FROM time_buckets
    WHERE bucket_end < '2024-12-31 23:00:00'::TIMESTAMP
)
SELECT
    tb.bucket_start,
    COUNT(e.id) AS event_count,
    AVG(e.value) AS avg_value,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY e.value) AS p95_value
FROM time_buckets tb
LEFT JOIN events e ON
    e.timestamp >= tb.bucket_start AND
    e.timestamp < tb.bucket_end
GROUP BY tb.bucket_start
ORDER BY tb.bucket_start;

-- 4. Pivoting Data (dynamic columns)
SELECT
    date,
    SUM(CASE WHEN category = 'Electronics' THEN sales ELSE 0 END) AS electronics,
    SUM(CASE WHEN category = 'Clothing' THEN sales ELSE 0 END) AS clothing,
    SUM(CASE WHEN category = 'Food' THEN sales ELSE 0 END) AS food,
    SUM(CASE WHEN category = 'Books' THEN sales ELSE 0 END) AS books
FROM daily_sales
GROUP BY date
ORDER BY date;

-- 5. Running Calculations (complex business logic)
WITH
order_details AS (
    SELECT
        order_id,
        customer_id,
        order_date,
        total_amount,
        ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) AS order_number,
        SUM(total_amount) OVER (
            PARTITION BY customer_id
            ORDER BY order_date
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS lifetime_value,
        AVG(total_amount) OVER (
            PARTITION BY customer_id
            ORDER BY order_date
            ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
        ) AS avg_last_4_orders
    FROM orders
),
customer_segments AS (
    SELECT
        customer_id,
        MAX(lifetime_value) AS total_ltv,
        MAX(order_number) AS total_orders,
        CASE
            WHEN MAX(lifetime_value) > 10000 THEN 'VIP'
            WHEN MAX(lifetime_value) > 5000 THEN 'Premium'
            WHEN MAX(lifetime_value) > 1000 THEN 'Regular'
            ELSE 'New'
        END AS segment
    FROM order_details
    GROUP BY customer_id
)
SELECT
    od.*,
    cs.segment,
    cs.total_ltv,
    -- Churn prediction signal
    CASE
        WHEN CURRENT_DATE - MAX(od.order_date) OVER (PARTITION BY od.customer_id) > 90
        THEN 'At Risk'
        ELSE 'Active'
    END AS churn_risk
FROM order_details od
JOIN customer_segments cs ON od.customer_id = cs.customer_id;
```

---

## CATEGORÍA 2: Data Visualization Best Practices

### 2.1 Python Visualization Libraries
**Dificultad:** ⭐⭐⭐⭐

```python
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# 1. Matplotlib avanzado con subplots
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# Plot 1: Time series con múltiples líneas
axes[0, 0].plot(dates, revenue, label='Revenue', linewidth=2)
axes[0, 0].plot(dates, costs, label='Costs', linewidth=2)
axes[0, 0].fill_between(dates, revenue, costs, alpha=0.3)
axes[0, 0].set_title('Revenue vs Costs', fontsize=14, fontweight='bold')
axes[0, 0].set_xlabel('Date')
axes[0, 0].set_ylabel('Amount ($)')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# Plot 2: Distribution con histogram y KDE
axes[0, 1].hist(data, bins=50, alpha=0.7, density=True, label='Histogram')
axes[0, 1].plot(x_smooth, kde_values, 'r-', linewidth=2, label='KDE')
axes[0, 1].axvline(data.mean(), color='green', linestyle='--', label=f'Mean: {data.mean():.2f}')
axes[0, 1].axvline(data.median(), color='orange', linestyle='--', label=f'Median: {data.median():.2f}')
axes[0, 1].set_title('Distribution Analysis')
axes[0, 1].legend()

# Plot 3: Box plot comparativo
axes[1, 0].boxplot([group1, group2, group3], labels=['A', 'B', 'C'])
axes[1, 0].set_title('Group Comparison')
axes[1, 0].set_ylabel('Value')

# Plot 4: Scatter plot con regression
axes[1, 1].scatter(x, y, alpha=0.5)
axes[1, 1].plot(x, regression_line, 'r-', linewidth=2, label=f'R² = {r2:.3f}')
axes[1, 1].set_title('Correlation Analysis')
axes[1, 1].legend()

plt.tight_layout()
plt.savefig('analysis.png', dpi=300, bbox_inches='tight')
plt.show()

# 2. Seaborn statistical plots
# Correlation heatmap
plt.figure(figsize=(12, 10))
correlation_matrix = df.corr()
mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
sns.heatmap(
    correlation_matrix,
    mask=mask,
    annot=True,
    fmt='.2f',
    cmap='coolwarm',
    center=0,
    square=True,
    linewidths=1,
    cbar_kws={"shrink": 0.8}
)
plt.title('Feature Correlation Matrix', fontsize=16, fontweight='bold')
plt.tight_layout()

# Pair plot para explorar relaciones
sns.pairplot(
    df,
    hue='category',
    diag_kind='kde',
    plot_kws={'alpha': 0.6},
    corner=True
)

# Violin plot con swarm
plt.figure(figsize=(12, 6))
sns.violinplot(data=df, x='category', y='value', inner=None)
sns.swarmplot(data=df, x='category', y='value', color='white', alpha=0.5, size=2)
plt.title('Distribution by Category')

# 3. Plotly interactive dashboards
fig = go.Figure()

# Multiple traces
fig.add_trace(go.Scatter(
    x=dates,
    y=revenue,
    name='Revenue',
    mode='lines+markers',
    line=dict(color='green', width=2),
    hovertemplate='Date: %{x}<br>Revenue: $%{y:,.0f}<extra></extra>'
))

fig.add_trace(go.Scatter(
    x=dates,
    y=forecast,
    name='Forecast',
    mode='lines',
    line=dict(color='blue', width=2, dash='dash')
))

# Confidence interval
fig.add_trace(go.Scatter(
    x=dates + dates[::-1],
    y=upper_bound + lower_bound[::-1],
    fill='toself',
    fillcolor='rgba(0,100,250,0.2)',
    line=dict(color='rgba(255,255,255,0)'),
    name='95% CI',
    showlegend=True
))

fig.update_layout(
    title='Revenue Forecast',
    xaxis_title='Date',
    yaxis_title='Revenue ($)',
    hovermode='x unified',
    template='plotly_white',
    height=600
)

fig.show()

# 4. Plotly Express para quick analysis
# Animated scatter
fig = px.scatter(
    df,
    x='metric1',
    y='metric2',
    animation_frame='year',
    animation_group='country',
    size='population',
    color='continent',
    hover_name='country',
    log_x=True,
    size_max=60,
    range_x=[100, 100000],
    range_y=[25, 90]
)

fig.update_layout(title='Country Metrics Over Time')
fig.show()

# Sunburst chart (hierarchical data)
fig = px.sunburst(
    df,
    path=['region', 'country', 'city'],
    values='sales',
    color='growth_rate',
    color_continuous_scale='RdYlGn',
    hover_data=['population']
)
fig.show()

# 5. Dashboard con múltiples gráficos
from plotly.subplots import make_subplots

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=('Revenue Trend', 'Category Distribution',
                    'Regional Performance', 'Cohort Retention'),
    specs=[
        [{'type': 'scatter'}, {'type': 'pie'}],
        [{'type': 'bar'}, {'type': 'heatmap'}]
    ]
)

# Revenue trend
fig.add_trace(
    go.Scatter(x=dates, y=revenue, name='Revenue'),
    row=1, col=1
)

# Category pie
fig.add_trace(
    go.Pie(labels=categories, values=sales, name='Sales'),
    row=1, col=2
)

# Regional bar
fig.add_trace(
    go.Bar(x=regions, y=performance, name='Performance'),
    row=2, col=1
)

# Cohort heatmap
fig.add_trace(
    go.Heatmap(
        z=cohort_data,
        x=months,
        y=cohorts,
        colorscale='Viridis'
    ),
    row=2, col=2
)

fig.update_layout(height=800, showlegend=True, title_text="Business Dashboard")
fig.show()
```

---

## CATEGORÍA 3: Data Processing at Scale

### 3.1 Pandas Performance Optimization
**Dificultad:** ⭐⭐⭐⭐

```python
import pandas as pd
import numpy as np

# 1. Efficient data loading
# ❌ Malo: Load todo en memoria
df = pd.read_csv('huge_file.csv')

# ✅ Bueno: Load en chunks
chunks = []
for chunk in pd.read_csv('huge_file.csv', chunksize=100000):
    # Procesar chunk
    chunk_processed = process(chunk)
    chunks.append(chunk_processed)

df = pd.concat(chunks, ignore_index=True)

# ✅ Mejor: Load solo columnas necesarias con tipos optimizados
df = pd.read_csv(
    'huge_file.csv',
    usecols=['col1', 'col2', 'col3'],
    dtype={
        'col1': 'int32',         # En vez de int64
        'col2': 'category',      # Para strings repetidos
        'col3': 'float32'        # En vez de float64
    },
    parse_dates=['date_column']
)

# 2. Vectorization vs loops
# ❌ Muy lento: Loop
for idx in range(len(df)):
    df.loc[idx, 'total'] = df.loc[idx, 'price'] * df.loc[idx, 'quantity']

# ✅ Rápido: Vectorizado
df['total'] = df['price'] * df['quantity']

# 3. Apply vs vectorization
# ❌ Lento: apply
df['category'] = df['value'].apply(lambda x: 'High' if x > 100 else 'Low')

# ✅ Rápido: np.where
df['category'] = np.where(df['value'] > 100, 'High', 'Low')

# Multiple conditions
df['category'] = np.select(
    [
        df['value'] > 1000,
        df['value'] > 100,
        df['value'] > 10
    ],
    ['VIP', 'Premium', 'Regular'],
    default='Basic'
)

# 4. Groupby optimization
# ❌ Lento: múltiples groupby
avg_price = df.groupby('category')['price'].mean()
max_price = df.groupby('category')['price'].max()
count = df.groupby('category').size()

# ✅ Rápido: single groupby con agg
result = df.groupby('category')['price'].agg(['mean', 'max', 'size'])

# Multiple columns y functions
result = df.groupby('category').agg({
    'price': ['mean', 'median', 'std'],
    'quantity': ['sum', 'mean'],
    'customer_id': 'nunique'
})

# 5. Merge optimization
# ❌ Lento: merge sin índices
result = df1.merge(df2, on='customer_id')

# ✅ Rápido: set index antes
df1_indexed = df1.set_index('customer_id')
df2_indexed = df2.set_index('customer_id')
result = df1_indexed.join(df2_indexed)

# 6. Memory optimization
# Antes
print(df.memory_usage(deep=True).sum() / 1024**2, 'MB')

# Convertir tipos
def optimize_dtypes(df):
    for col in df.columns:
        col_type = df[col].dtype

        if col_type != 'object':
            c_min = df[col].min()
            c_max = df[col].max()

            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)

            elif str(col_type)[:5] == 'float':
                if c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)

        else:
            # String to category si pocos valores únicos
            if df[col].nunique() / len(df) < 0.5:
                df[col] = df[col].astype('category')

    return df

df_optimized = optimize_dtypes(df)

# Después
print(df_optimized.memory_usage(deep=True).sum() / 1024**2, 'MB')

# 7. Parallel processing con Dask
import dask.dataframe as dd

# Convertir a Dask DataFrame
ddf = dd.from_pandas(df, npartitions=4)

# Operaciones lazy (no ejecuta hasta compute())
result = ddf.groupby('category')['sales'].mean()

# Ejecutar en paralelo
result_computed = result.compute()

# Read large CSV con Dask
ddf = dd.read_csv('huge_file.csv', blocksize='64MB')

# Operaciones complejas
result = ddf[ddf['value'] > 100].groupby('category').agg({
    'sales': ['sum', 'mean'],
    'quantity': 'sum'
}).compute()
```

---

## CATEGORÍA 4: Statistical Analysis

### 4.1 A/B Testing y Hypothesis Testing
**Dificultad:** ⭐⭐⭐⭐⭐

```python
from scipy import stats
import numpy as np

# 1. T-Test (comparar dos grupos)
control_group = np.array([23, 25, 27, 29, 31, 24, 26, 28])
treatment_group = np.array([30, 32, 34, 35, 36, 33, 31, 37])

# Independent t-test
t_statistic, p_value = stats.ttest_ind(control_group, treatment_group)

print(f"T-statistic: {t_statistic:.4f}")
print(f"P-value: {p_value:.4f}")

if p_value < 0.05:
    print("Statistically significant difference!")
else:
    print("No significant difference")

# Effect size (Cohen's d)
def cohens_d(group1, group2):
    n1, n2 = len(group1), len(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    pooled_std = np.sqrt(((n1-1)*var1 + (n2-1)*var2) / (n1+n2-2))
    return (np.mean(group1) - np.mean(group2)) / pooled_std

effect_size = cohens_d(treatment_group, control_group)
print(f"Effect size (Cohen's d): {effect_size:.4f}")

# 2. Sample Size Calculation
from statsmodels.stats.power import ttest_power, tt_ind_solve_power

# ¿Cuántos usuarios necesito para detectar 10% de mejora?
effect_size = 0.1
alpha = 0.05  # Significance level
power = 0.8   # Desired power

required_sample_size = tt_ind_solve_power(
    effect_size=effect_size,
    alpha=alpha,
    power=power,
    alternative='two-sided'
)

print(f"Required sample size per group: {int(required_sample_size)}")

# 3. Chi-Square Test (categorical data)
# Conversion rates
control_conversions = 450
control_total = 10000
treatment_conversions = 520
treatment_total = 10000

# Contingency table
observed = np.array([
    [control_conversions, control_total - control_conversions],
    [treatment_conversions, treatment_total - treatment_conversions]
])

chi2, p_value, dof, expected = stats.chi2_contingency(observed)

print(f"Chi-square statistic: {chi2:.4f}")
print(f"P-value: {p_value:.4f}")

# 4. Bayesian A/B Test
def bayesian_ab_test(alpha_a, beta_a, alpha_b, beta_b, num_samples=10000):
    """
    Beta distribution parameters:
    alpha = successes + 1
    beta = failures + 1
    """
    # Sample from posteriors
    samples_a = np.random.beta(alpha_a, beta_a, num_samples)
    samples_b = np.random.beta(alpha_b, beta_b, num_samples)

    # Probability that B > A
    prob_b_better = np.mean(samples_b > samples_a)

    # Expected lift
    expected_lift = np.mean((samples_b - samples_a) / samples_a)

    return {
        'prob_b_better': prob_b_better,
        'expected_lift': expected_lift,
        'samples_a': samples_a,
        'samples_b': samples_b
    }

# Control: 450/10000 conversions
# Treatment: 520/10000 conversions
result = bayesian_ab_test(
    alpha_a=451,
    beta_a=9551,
    alpha_b=521,
    beta_b=9481
)

print(f"Probability that B is better: {result['prob_b_better']:.2%}")
print(f"Expected lift: {result['expected_lift']:.2%}")

# 5. Multiple Testing Correction (Bonferroni, FDR)
from statsmodels.stats.multitest import multipletests

# Múltiples p-values de diferentes tests
p_values = [0.01, 0.04, 0.03, 0.08, 0.02]

# Bonferroni correction
reject, pvals_corrected, _, _ = multipletests(
    p_values,
    alpha=0.05,
    method='bonferroni'
)

print("Bonferroni corrected p-values:", pvals_corrected)
print("Reject null:", reject)

# FDR (False Discovery Rate) - menos conservador
reject_fdr, pvals_fdr, _, _ = multipletests(
    p_values,
    alpha=0.05,
    method='fdr_bh'  # Benjamini-Hochberg
)

print("FDR corrected p-values:", pvals_fdr)
print("Reject null (FDR):", reject_fdr)

# 6. Sequential Testing (para early stopping)
def sequential_test(control_data, treatment_data, alpha=0.05):
    """
    Sequential probability ratio test
    """
    n_control = len(control_data)
    n_treatment = len(treatment_data)

    # Z-test for proportions
    p_control = np.mean(control_data)
    p_treatment = np.mean(treatment_data)
    p_pooled = (np.sum(control_data) + np.sum(treatment_data)) / (n_control + n_treatment)

    se = np.sqrt(p_pooled * (1 - p_pooled) * (1/n_control + 1/n_treatment))
    z = (p_treatment - p_control) / se

    # Adjusted alpha para sequential testing
    adjusted_alpha = alpha / np.log(n_control)

    p_value = 2 * (1 - stats.norm.cdf(abs(z)))

    return {
        'z_statistic': z,
        'p_value': p_value,
        'significant': p_value < adjusted_alpha,
        'control_rate': p_control,
        'treatment_rate': p_treatment
    }
```

---

## Resumen Prioridades Data Analysis

| Tema | Dificultad | Criticidad | Frecuencia | Prioridad |
|------|------------|------------|------------|-----------|
| SQL Window Functions | 5 | 5 | 5 | **CRÍTICA** |
| Pandas Optimization | 4 | 5 | 5 | **CRÍTICA** |
| Statistical Testing | 5 | 4 | 4 | **ALTA** |
| Complex CTEs | 5 | 4 | 4 | **ALTA** |
| Data Visualization | 4 | 4 | 5 | **ALTA** |
| A/B Testing | 5 | 5 | 3 | **ALTA** |
