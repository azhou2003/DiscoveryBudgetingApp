import matplotlib.pyplot as plt
import math

def plot_spending_summary(proc):
    """
    Plots total and category-wise weekly spending.
    `proc` is an instance of DiscoverActProc.
    """
    num_categories = len(proc.category_series)
    total_plots = num_categories + 1
    cols = 2
    rows = math.ceil(total_plots / cols)

    fig, axs = plt.subplots(rows, cols, figsize=(14, 5 * rows))
    axs = axs.flatten()

    # Total spending
    x_total = list(proc.weekly_spending.keys())
    y_total = list(proc.weekly_spending.values())
    axs[0].bar(x_total, y_total, width=6, color='blue', label='Weekly Spending')
    axs[0].axhline(y=proc.average_spending, color='red', linestyle='--', label='User Avg')
    if hasattr(proc, 'bls_weekly_avg'):
        axs[0].axhline(y=proc.bls_weekly_avg, color='green', linestyle=':', label='BLS Avg')
    axs[0].set_title("Total Weekly Spending")
    axs[0].set_xlabel("Week Start")
    axs[0].set_ylabel("Spending ($)")
    axs[0].legend()
    axs[0].tick_params(axis='x', rotation=45)

    # Per-category spending
    for idx, (category, weekly_data) in enumerate(proc.category_series.items(), start=1):
        x_vals = list(weekly_data.keys())
        y_vals = list(weekly_data.values())
        axs[idx].bar(x_vals, y_vals, width=6, label=category)
        avg = proc.average_spending_by_category.get(category, 0)
        axs[idx].axhline(y=avg, color='red', linestyle='--', label='User Avg')
        if proc.bls_comparator:
            bls_avg = proc.bls_comparator.get_bls_avg_for_user_category(category)
            if bls_avg:
                axs[idx].axhline(y=bls_avg / 52, color='green', linestyle=':', label='BLS Avg')
        axs[idx].set_title(f"Weekly Spending - {category}")
        axs[idx].set_xlabel("Week Start")
        axs[idx].set_ylabel("Spending ($)")
        axs[idx].legend()
        axs[idx].tick_params(axis='x', rotation=45)

    for ax in axs[total_plots:]:
        fig.delaxes(ax)

    fig.tight_layout()
    plt.show()
