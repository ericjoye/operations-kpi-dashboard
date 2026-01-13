"""
Operations KPI Dashboard - Analytics Script
============================================
This script analyzes operations data and calculates key performance indicators (KPIs)
to help operations teams understand their performance and identify improvement areas.
"""

import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# ==========================================
# STEP 1: LOAD THE DATA
# ==========================================

def load_data(filename='operations_data.csv'):
    """
    Load operations data from CSV file.
    
    Args:
        filename (str): Path to the CSV file
    
    Returns:
        pd.DataFrame: Loaded data
    """
    print("📊 Loading operations data...")
    
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(filename)
    
    # Convert Date column to datetime format for easier manipulation
    df['Date'] = pd.to_datetime(df['Date'])
    
    print(f"✅ Loaded {len(df)} records from {df['Date'].min().date()} to {df['Date'].max().date()}")
    return df


# ==========================================
# STEP 2: CALCULATE KPIs
# ==========================================

def calculate_kpis(df):
    """
    Calculate key performance indicators for operations data.
    
    KPIs calculated:
    - Error Rate: Percentage of tasks that had errors
    - Productivity: Tasks completed per hour worked
    - Average Time per Task: How long each task takes on average
    - Rework Ratio: Percentage of tasks that required rework
    
    Args:
        df (pd.DataFrame): Operations data
    
    Returns:
        pd.DataFrame: Data with KPI columns added
    """
    print("\n🔧 Calculating KPIs...")
    
    # Create a copy to avoid modifying original data
    df_kpi = df.copy()
    
    # 1. ERROR RATE: (Errors Found / Tasks Completed) * 100
    # This tells us what percentage of our tasks had issues
    df_kpi['Error_Rate_%'] = (df_kpi['Errors_Found'] / df_kpi['Tasks_Completed'] * 100).round(2)
    
    # 2. PRODUCTIVITY: Tasks Completed / Time Spent
    # This shows how many tasks we complete per hour
    df_kpi['Productivity_Tasks_Per_Hour'] = (df_kpi['Tasks_Completed'] / df_kpi['Time_Spent_Hours']).round(2)
    
    # 3. AVERAGE TIME PER TASK: Time Spent / Tasks Completed
    # This indicates how long each task takes on average (in minutes)
    df_kpi['Avg_Time_Per_Task_Minutes'] = ((df_kpi['Time_Spent_Hours'] / df_kpi['Tasks_Completed']) * 60).round(2)
    
    # 4. REWORK RATIO: (Rework Count / Tasks Completed) * 100
    # This shows what percentage of tasks needed to be redone
    df_kpi['Rework_Ratio_%'] = (df_kpi['Rework_Count'] / df_kpi['Tasks_Completed'] * 100).round(2)
    
    print("✅ KPIs calculated successfully")
    return df_kpi


# ==========================================
# STEP 3: GENERATE SUMMARY REPORT
# ==========================================

def generate_summary(df_kpi):
    """
    Generate an executive summary of operations performance.
    
    Args:
        df_kpi (pd.DataFrame): Data with calculated KPIs
    """
    print("\n" + "="*60)
    print("📈 OPERATIONS PERFORMANCE SUMMARY")
    print("="*60)
    
    # Calculate overall statistics
    total_tasks = df_kpi['Tasks_Completed'].sum()
    total_errors = df_kpi['Errors_Found'].sum()
    total_hours = df_kpi['Time_Spent_Hours'].sum()
    total_rework = df_kpi['Rework_Count'].sum()
    
    # Calculate average KPIs
    avg_error_rate = df_kpi['Error_Rate_%'].mean()
    avg_productivity = df_kpi['Productivity_Tasks_Per_Hour'].mean()
    avg_time_per_task = df_kpi['Avg_Time_Per_Task_Minutes'].mean()
    avg_rework_ratio = df_kpi['Rework_Ratio_%'].mean()
    
    # Display key metrics
    print(f"\n📅 Analysis Period: {df_kpi['Date'].min().date()} to {df_kpi['Date'].max().date()}")
    print(f"📊 Total Working Days: {len(df_kpi)}")
    
    print(f"\n🎯 OVERALL PERFORMANCE:")
    print(f"   • Total Tasks Completed: {total_tasks:,}")
    print(f"   • Total Hours Worked: {total_hours:,.1f}")
    print(f"   • Total Errors Found: {total_errors}")
    print(f"   • Total Rework Items: {total_rework}")
    
    print(f"\n📊 AVERAGE KPIs:")
    print(f"   • Error Rate: {avg_error_rate:.2f}%")
    print(f"   • Productivity: {avg_productivity:.2f} tasks/hour")
    print(f"   • Avg Time per Task: {avg_time_per_task:.2f} minutes")
    print(f"   • Rework Ratio: {avg_rework_ratio:.2f}%")
    
    # Performance insights
    print(f"\n💡 KEY INSIGHTS:")
    
    # Check error rate
    if avg_error_rate > 10:
        print(f"   ⚠️  High error rate detected ({avg_error_rate:.1f}%). Consider quality improvements.")
    else:
        print(f"   ✅ Error rate is within acceptable range ({avg_error_rate:.1f}%).")
    
    # Check productivity
    if avg_productivity >= 6:
        print(f"   ✅ Strong productivity ({avg_productivity:.2f} tasks/hour).")
    else:
        print(f"   ⚠️  Productivity could be improved ({avg_productivity:.2f} tasks/hour).")
    
    # Check rework ratio
    if avg_rework_ratio > 5:
        print(f"   ⚠️  High rework ratio ({avg_rework_ratio:.1f}%). Review processes for defects.")
    else:
        print(f"   ✅ Rework ratio is manageable ({avg_rework_ratio:.1f}%).")
    
    print("\n" + "="*60)


# ==========================================
# STEP 4: EXPORT RESULTS
# ==========================================

def export_results(df_kpi, output_filename='operations_kpi_results.csv'):
    """
    Export the data with calculated KPIs to a new CSV file.
    
    Args:
        df_kpi (pd.DataFrame): Data with KPIs
        output_filename (str): Name of output file
    """
    print(f"\n💾 Exporting results to {output_filename}...")
    
    # Save to CSV
    df_kpi.to_csv(output_filename, index=False)
    
    print(f"✅ Results exported successfully!")
    print(f"   Columns: {', '.join(df_kpi.columns.tolist())}")


# ==========================================
# STEP 5: CREATE VISUALIZATIONS
# ==========================================

def create_visualizations(df_kpi, output_filename='kpi_trends.png'):
    """
    Create trend line visualizations for all KPIs.
    
    Args:
        df_kpi (pd.DataFrame): Data with calculated KPIs
        output_filename (str): Name of output image file
    """
    print(f"\n📊 Creating KPI trend visualizations...")
    
    # Set up the plot style
    plt.style.use('seaborn-v0_8-darkgrid')
    
    # Create a figure with 4 subplots (2x2 grid)
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Operations KPI Trends', fontsize=16, fontweight='bold')
    
    # Plot 1: Error Rate Trend
    axes[0, 0].plot(df_kpi['Date'], df_kpi['Error_Rate_%'], 
                    marker='o', linewidth=2, markersize=4, color='#e74c3c')
    axes[0, 0].axhline(y=df_kpi['Error_Rate_%'].mean(), 
                       color='red', linestyle='--', linewidth=1, alpha=0.7, label='Average')
    axes[0, 0].set_title('Error Rate Trend', fontsize=12, fontweight='bold')
    axes[0, 0].set_ylabel('Error Rate (%)', fontsize=10)
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Plot 2: Productivity Trend
    axes[0, 1].plot(df_kpi['Date'], df_kpi['Productivity_Tasks_Per_Hour'], 
                    marker='o', linewidth=2, markersize=4, color='#3498db')
    axes[0, 1].axhline(y=df_kpi['Productivity_Tasks_Per_Hour'].mean(), 
                       color='blue', linestyle='--', linewidth=1, alpha=0.7, label='Average')
    axes[0, 1].set_title('Productivity Trend', fontsize=12, fontweight='bold')
    axes[0, 1].set_ylabel('Tasks per Hour', fontsize=10)
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # Plot 3: Average Time per Task Trend
    axes[1, 0].plot(df_kpi['Date'], df_kpi['Avg_Time_Per_Task_Minutes'], 
                    marker='o', linewidth=2, markersize=4, color='#2ecc71')
    axes[1, 0].axhline(y=df_kpi['Avg_Time_Per_Task_Minutes'].mean(), 
                       color='green', linestyle='--', linewidth=1, alpha=0.7, label='Average')
    axes[1, 0].set_title('Avg Time per Task Trend', fontsize=12, fontweight='bold')
    axes[1, 0].set_ylabel('Minutes per Task', fontsize=10)
    axes[1, 0].set_xlabel('Date', fontsize=10)
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    # Plot 4: Rework Ratio Trend
    axes[1, 1].plot(df_kpi['Date'], df_kpi['Rework_Ratio_%'], 
                    marker='o', linewidth=2, markersize=4, color='#f39c12')
    axes[1, 1].axhline(y=df_kpi['Rework_Ratio_%'].mean(), 
                       color='orange', linestyle='--', linewidth=1, alpha=0.7, label='Average')
    axes[1, 1].set_title('Rework Ratio Trend', fontsize=12, fontweight='bold')
    axes[1, 1].set_ylabel('Rework Ratio (%)', fontsize=10)
    axes[1, 1].set_xlabel('Date', fontsize=10)
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    # Format x-axis dates for all subplots
    for ax in axes.flat:
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
        ax.tick_params(axis='x', rotation=45)
    
    # Adjust layout to prevent overlap
    plt.tight_layout()
    
    # Save the figure
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    print(f"✅ Visualization saved as '{output_filename}'")
    
    # Close the plot to free memory
    plt.close()


# ==========================================
# MAIN EXECUTION
# ==========================================

def main():
    """
    Main function to run the entire analytics pipeline.
    """
    print("\n🚀 Starting Operations KPI Dashboard Analysis\n")
    
    try:
        # Step 1: Load data
        df = load_data('operations_data.csv')
        
        # Step 2: Calculate KPIs
        df_kpi = calculate_kpis(df)
        
        # Step 3: Generate and display summary
        generate_summary(df_kpi)
        
        # Step 4: Export results
        export_results(df_kpi, 'operations_kpi_results.csv')
        
        # Step 5: Create visualizations
        create_visualizations(df_kpi, 'kpi_trends.png')
        
        print("\n✨ Analysis complete!")
        print("   📄 Detailed results: 'operations_kpi_results.csv'")
        print("   📊 Visual trends: 'kpi_trends.png'\n")
        
    except FileNotFoundError:
        print("❌ Error: 'operations_data.csv' not found. Please ensure the file exists.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")


# Run the script
if __name__ == "__main__":
    main()
