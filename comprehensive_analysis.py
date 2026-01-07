import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import json
import warnings
warnings.filterwarnings('ignore')

# Set style for better plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# City coordinates mapping
CITY_COORDINATES = {
    'Algeria': {
        'Algiers': (36.6997, 3.0576),
        'Batna': (35.556, 6.1741),
        'Oran': (35.6911, -0.6417),
        'Annaba': (36.9, 7.7667),
        'Blida': (36.4667, 2.8167),
        'Constantine': (36.365, 6.6147),
        'Biskra': (34.8504, 5.7281),
        'Djelfa': (34.6728, 3.263),
        'Sétif': (36.1911, 5.4137)
    },
    'Bahrain': {
        'Manama': (26.2279, 50.5857)
    },
    'Egypt': {
        'Cairo': (30.0626, 31.2497),
        'Alexandria': (31.2018, 29.9158)
    },
    'Iraq': {
        'Basra': (30.5085, 47.7804),
        'Baghdad': (33.3406, 44.4009)
    },
    'Jordan': {
        'Amman': (31.9552, 35.945),
        'Irbid': (32.556, 35.848)
    },
    'Kuwait': {
        'Kuwait (City)': (29.3759, 47.9774)
    },
    'Lebanon': {
        'Beirut': (33.8938, 35.5018),
        'Cheikh Taba': (34.5333, 36.0833)
    },
    'Libya': {
        'Tripoli': (32.8872, 13.1913),
        'Benghazi': (32.1167, 20.0667)
    },
    'Morocco': {
        'Fes': (34.0333, -5),
        'Casablanca': (33.5731, -7.5898),
        'Rabat': (34.0209, -6.8416),
        'Marrakech': (31.6295, -7.9811),
        'Tanger (Tangier)': (35.7796, -5.8339)
    },
    'Oman': {
        'Oman (Muscat)': (23.5841, 58.4078)
    },
    'Palestine': {
        'Nablus': (32.2211, 35.2544),
        'Hebron': (31.5294, 35.0938),
        'Ramallah': (31.8996, 35.2042),
        'Jerusalem': (31.769, 35.2163),
        'Qaza (Gaza City)': (31.5016, 34.4667)
    },
    'Qatar': {
        'Doha': (25.2854, 51.531)
    },
    'Saudi Arabia': {
        'Riyadh': (24.7136, 46.6753),
        'Jeddah': (21.4901, 39.1862),
        'Makkah (Mecca)': (21.4266, 39.8256)
    },
    'Somalia': {
        'Shabelle (Lower Shabelle region)': (1.7683, 44.39),
        'Mogadishu': (2.0371, 45.3438),
        'Daljir (Mogadishu area)': (2.0371, 45.3438)
    },
    'Sudan': {
        'El Obeid': (13.1842, 30.2167),
        'Omdurman': (15.6445, 32.4777),
        'Khartoum': (15.5007, 32.5599),
        'Wad Medani': (14.4012, 33.5199),
        'Port Sudan': (19.6175, 37.2164)
    },
    'Syria': {
        'Aleppo': (36.2012, 37.1612),
        'Damascus': (33.5104, 36.2783)
    },
    'Tunisia': {
        'Tunis': (36.819, 10.1658)
    },
    'UAE': {
        'Ajman': (25.4052, 55.5136),
        'Dubai': (25.2048, 55.2708),
        'Fujairah': (25.1288, 56.3265),
        'Abu Dhabi': (24.4539, 54.3773),
        'Sharjah': (25.3463, 55.4209)
    },
    'Yemen': {
        'Sana\'a': (15.3694, 44.191),
        'Aden': (12.7794, 45.0367),
        'Taiz': (13.5794, 44.0207),
        'Al-Hodeidah': (14.7978, 42.9545)
    }
}

def get_coordinates(country, city):
    """Get latitude and longitude for a city"""
    
    # City name mapping to handle mismatches
    city_mapping = {
        'alger': 'Algiers',
        'batna': 'Batna',
        'djelfa': 'Djelfa',
        'biskra': 'Biskra',
        'Tanger': 'Tanger (Tangier)',
        'Ajman': 'Ajman',
        'Jeddah': 'Jeddah',
        'Qaza': 'Qaza (Gaza City)',
        'amman': 'Amman',
        'kuwait': 'Kuwait (City)',
        'Muscat': 'Oman (Muscat)',
        'Abu Dhabi': 'Abu Dhabi',
        'sanaa': 'Sana\'a',
        'cheikh_taba': 'Cheikh Taba',
        'Riyadh': 'Riyadh',
        'unknown_city': None,
        'manama_nation-wide': 'Manama',
        'constantine': 'Constantine',
        'setif': 'Sétif',
        'tunis': 'Tunis',
        'taiz': 'Taiz',
        'beirut': 'Beirut',
        'hebron': 'Hebron',
        'Shabelle': 'Shabelle (Lower Shabelle region)',
        'manama': 'Manama',
        'bilda': 'Blida',
        'Somali': 'Mogadishu'
    }
    
    # Country name mapping
    country_mapping = {
        'United_Arab_Emirate': 'UAE',
        'Saudi_Arabia': 'Saudi Arabia'
    }
    
    # Apply mappings
    mapped_city = city_mapping.get(city, city)
    mapped_country = country_mapping.get(country, country)
    
    if mapped_city is None:
        return None, None
    
    try:
        lat, lon = CITY_COORDINATES[mapped_country][mapped_city]
        return lat, lon
    except KeyError:
        return None, None

def combine_annotations():
    """Combine all annotation CSV files from radio2 folder"""
    print("📁 Combining all annotation files...")
    
    # Get all CSV files from radio2 folder (parent directory)
    csv_files = glob.glob('../radio2/*.csv')
    
    if not csv_files:
        print("❌ No CSV files found in radio2 folder!")
        return None
    
    print(f"Found {len(csv_files)} CSV files:")
    for file in csv_files:
        print(f"  - {os.path.basename(file)}")
    
    # Read and combine all CSV files
    all_dfs = []
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file)
            print(f"Loaded {len(df)} rows from {os.path.basename(csv_file)}")
            all_dfs.append(df)
        except Exception as e:
            print(f"Error reading {csv_file}: {e}")
    
    if not all_dfs:
        print("❌ No valid CSV files could be read!")
        return None
    
    # Combine all dataframes
    combined_df = pd.concat(all_dfs, ignore_index=True)
    
    # Remove duplicates based on filename, country, city, and annotator
    print(f"\nBefore removing duplicates: {len(combined_df)} rows")
    combined_df = combined_df.drop_duplicates(subset=['Sound filename', 'Country', 'City', 'Annotator'], keep='last')
    print(f"After removing duplicates: {len(combined_df)} rows")
    
    # Add coordinates
    print("\n📍 Adding coordinates...")
    coordinates_added = 0
    missing_coordinates = 0
    
    for idx, row in combined_df.iterrows():
        country = row['Country']
        city = row['City']
        lat, lon = get_coordinates(country, city)
        
        if lat is not None and lon is not None:
            combined_df.at[idx, 'Latitude'] = lat
            combined_df.at[idx, 'Longitude'] = lon
            coordinates_added += 1
        else:
            combined_df.at[idx, 'Latitude'] = 0.0
            combined_df.at[idx, 'Longitude'] = 0.0
            missing_coordinates += 1
    
    print(f"✅ Coordinates added: {coordinates_added}")
    print(f"⚠️ Missing coordinates: {missing_coordinates}")
    
    return combined_df

def generate_analysis(combined_df):
    """Generate comprehensive analysis and visualizations"""
    print("\n📊 Generating comprehensive analysis...")
    
    # Create figures directory
    os.makedirs('figures', exist_ok=True)
    
    # 1. Overall Statistics
    print("\n1️⃣ Overall Statistics")
    total_annotations = len(combined_df)
    unique_files = combined_df['Sound filename'].nunique()
    unique_countries = combined_df['Country'].nunique()
    unique_cities = combined_df['City'].nunique()
    unique_annotators = combined_df['Annotator'].nunique()
    
    print(f"Total annotations: {total_annotations:,}")
    print(f"Unique files: {unique_files:,}")
    print(f"Unique countries: {unique_countries}")
    print(f"Unique cities: {unique_cities}")
    print(f"Unique annotators: {unique_annotators}")
    
    # 2. Annotator Analysis
    print("\n2️⃣ Annotator Analysis")
    annotator_stats = combined_df['Annotator'].value_counts()
    
    plt.figure(figsize=(12, 6))
    annotator_stats.plot(kind='bar', color='skyblue')
    plt.title('Annotations per Annotator', fontsize=16, fontweight='bold')
    plt.xlabel('Annotator', fontsize=12)
    plt.ylabel('Number of Annotations', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('figures/annotations_per_annotator.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Country Analysis
    print("\n3️⃣ Country Analysis")
    country_stats = combined_df['Country'].value_counts()
    
    plt.figure(figsize=(14, 8))
    country_stats.plot(kind='bar', color='lightcoral')
    plt.title('Annotations per Country', fontsize=16, fontweight='bold')
    plt.xlabel('Country', fontsize=12)
    plt.ylabel('Number of Annotations', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('figures/annotations_per_country.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 4. City Analysis (Top 20)
    print("\n4️⃣ City Analysis")
    city_stats = combined_df['City'].value_counts().head(20)
    
    plt.figure(figsize=(16, 10))
    city_stats.plot(kind='bar', color='lightgreen')
    plt.title('Top 20 Cities by Number of Annotations', fontsize=16, fontweight='bold')
    plt.xlabel('City', fontsize=12)
    plt.ylabel('Number of Annotations', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('figures/top_20_cities.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 5. Keep vs Skip Analysis
    print("\n5️⃣ Keep vs Skip Analysis")
    keep_skip_stats = combined_df['Keep or skip'].value_counts()
    
    plt.figure(figsize=(10, 8))
    plt.pie(keep_skip_stats.values, labels=keep_skip_stats.index, autopct='%1.1f%%', 
            colors=['lightgreen', 'lightcoral'], startangle=90)
    plt.title('Keep vs Skip Distribution', fontsize=16, fontweight='bold')
    plt.axis('equal')
    plt.savefig('figures/keep_vs_skip_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 6. Emotion Analysis
    print("\n6️⃣ Emotion Analysis")
    emotion_stats = combined_df['Emotion'].value_counts()
    
    plt.figure(figsize=(12, 8))
    emotion_stats.plot(kind='bar', color='gold')
    plt.title('Emotion Distribution', fontsize=16, fontweight='bold')
    plt.xlabel('Emotion', fontsize=12)
    plt.ylabel('Number of Annotations', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('figures/emotion_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 7. Type Analysis
    print("\n7️⃣ Type Analysis")
    type_stats = combined_df['Type'].value_counts()
    
    plt.figure(figsize=(12, 8))
    type_stats.plot(kind='bar', color='lightblue')
    plt.title('Audio Type Distribution', fontsize=16, fontweight='bold')
    plt.xlabel('Type', fontsize=12)
    plt.ylabel('Number of Annotations', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('figures/type_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 8. MSA/Dialect Analysis
    print("\n8️⃣ MSA/Dialect Analysis")
    msa_stats = combined_df['MSA or Dialect?'].value_counts()
    
    plt.figure(figsize=(10, 8))
    plt.pie(msa_stats.values, labels=msa_stats.index, autopct='%1.1f%%', 
            colors=['lightcoral', 'lightblue', 'lightgreen', 'gold'], startangle=90)
    plt.title('MSA/Dialect Distribution', fontsize=16, fontweight='bold')
    plt.axis('equal')
    plt.savefig('figures/msa_dialect_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 9. Confidence Analysis
    print("\n9️⃣ Confidence Analysis")
    confidence_stats = combined_df['Confidence'].value_counts()
    
    plt.figure(figsize=(10, 8))
    plt.pie(confidence_stats.values, labels=confidence_stats.index, autopct='%1.1f%%', 
            colors=['lightgreen', 'gold', 'lightcoral'], startangle=90)
    plt.title('Confidence Level Distribution', fontsize=16, fontweight='bold')
    plt.axis('equal')
    plt.savefig('figures/confidence_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 10. Duration Analysis
    print("\n🔟 Duration Analysis")
    plt.figure(figsize=(12, 6))
    plt.hist(combined_df['Duration (seconds)'], bins=30, color='skyblue', alpha=0.7)
    plt.title('Distribution of Audio Duration', fontsize=16, fontweight='bold')
    plt.xlabel('Duration (seconds)', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('figures/duration_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 11. Geographic Distribution (Keep entries only)
    print("\n1️⃣1️⃣ Geographic Distribution")
    keep_df = combined_df[combined_df['Keep or skip'] == 'Keep']
    
    plt.figure(figsize=(16, 10))
    plt.scatter(keep_df['Longitude'], keep_df['Latitude'], 
               c=keep_df['Country'].astype('category').cat.codes, 
               cmap='tab20', alpha=0.6, s=50)
    plt.title('Geographic Distribution of Kept Recordings', fontsize=16, fontweight='bold')
    plt.xlabel('Longitude', fontsize=12)
    plt.ylabel('Latitude', fontsize=12)
    plt.colorbar(label='Country')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('figures/geographic_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 12. Cross-tabulation Analysis
    print("\n1️⃣2️⃣ Cross-tabulation Analysis")
    
    # Emotion vs Type
    emotion_type_cross = pd.crosstab(combined_df['Emotion'], combined_df['Type'])
    plt.figure(figsize=(14, 8))
    sns.heatmap(emotion_type_cross, annot=True, fmt='d', cmap='YlOrRd')
    plt.title('Emotion vs Type Cross-tabulation', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('figures/emotion_type_crosstab.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 13. Annotator Agreement Analysis
    print("\n1️⃣3️⃣ Annotator Agreement Analysis")
    
    # Group by file and count unique annotators
    file_annotators = combined_df.groupby(['Sound filename', 'Country', 'City'])['Annotator'].nunique()
    annotator_counts = file_annotators.value_counts().sort_index()
    
    plt.figure(figsize=(10, 6))
    annotator_counts.plot(kind='bar', color='purple')
    plt.title('Distribution of Number of Annotators per File', fontsize=16, fontweight='bold')
    plt.xlabel('Number of Annotators', fontsize=12)
    plt.ylabel('Number of Files', fontsize=12)
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig('figures/annotator_agreement.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 14. Timeline Analysis
    print("\n1️⃣4️⃣ Timeline Analysis")
    combined_df['Timestamp'] = pd.to_datetime(combined_df['Timestamp'])
    combined_df['Date'] = combined_df['Timestamp'].dt.date
    
    daily_annotations = combined_df.groupby('Date').size()
    
    plt.figure(figsize=(16, 6))
    daily_annotations.plot(kind='line', color='blue', linewidth=2)
    plt.title('Daily Annotation Activity', fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Number of Annotations', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('figures/daily_activity.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("\n✅ All visualizations generated successfully!")

def save_summary_report(combined_df):
    """Save a comprehensive summary report"""
    print("\n📝 Generating summary report...")
    
    # Calculate statistics
    total_annotations = len(combined_df)
    unique_files = combined_df['Sound filename'].nunique()
    unique_countries = combined_df['Country'].nunique()
    unique_cities = combined_df['City'].nunique()
    unique_annotators = combined_df['Annotator'].nunique()
    
    keep_annotations = len(combined_df[combined_df['Keep or skip'] == 'Keep'])
    skip_annotations = len(combined_df[combined_df['Keep or skip'] == 'Skip'])
    
    # Create summary report
    report = f"""
# Radio Recordings Dataset Analysis Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overall Statistics
- Total Annotations: {total_annotations:,}
- Unique Audio Files: {unique_files:,}
- Unique Countries: {unique_countries}
- Unique Cities: {unique_cities}
- Unique Annotators: {unique_annotators}

## Keep vs Skip Analysis
- Keep Annotations: {keep_annotations:,} ({keep_annotations/total_annotations*100:.1f}%)
- Skip Annotations: {skip_annotations:,} ({skip_annotations/total_annotations*100:.1f}%)

## Top 10 Countries by Annotations
{combined_df['Country'].value_counts().head(10).to_string()}

## Top 10 Cities by Annotations
{combined_df['City'].value_counts().head(10).to_string()}

## Annotator Statistics
{combined_df['Annotator'].value_counts().to_string()}

## Emotion Distribution
{combined_df['Emotion'].value_counts().to_string()}

## Audio Type Distribution
{combined_df['Type'].value_counts().to_string()}

## MSA/Dialect Distribution
{combined_df['MSA or Dialect?'].value_counts().to_string()}

## Confidence Level Distribution
{combined_df['Confidence'].value_counts().to_string()}

## Duration Statistics
- Mean Duration: {combined_df['Duration (seconds)'].mean():.2f} seconds
- Median Duration: {combined_df['Duration (seconds)'].median():.2f} seconds
- Min Duration: {combined_df['Duration (seconds)'].min():.2f} seconds
- Max Duration: {combined_df['Duration (seconds)'].max():.2f} seconds

## Annotator Agreement
- Files with 1 annotator: {combined_df.groupby(['Sound filename', 'Country', 'City'])['Annotator'].nunique().value_counts().get(1, 0):,}
- Files with 2+ annotators: {combined_df.groupby(['Sound filename', 'Country', 'City'])['Annotator'].nunique().value_counts().get(2, 0):,}

## Geographic Coverage
- Countries with coordinates: {len(combined_df[combined_df['Latitude'] != 0.0]['Country'].unique())}
- Cities with coordinates: {len(combined_df[combined_df['Latitude'] != 0.0]['City'].unique())}
"""
    
    # Save report
    with open('summary_report.md', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("✅ Summary report saved to summary_report.md")

def main():
    print("🚀 Starting Comprehensive Dataset Analysis")
    print("=" * 50)
    
    # 1. Combine all annotations
    combined_df = combine_annotations()
    
    if combined_df is None:
        print("❌ Failed to combine annotations!")
        return
    
    # 2. Save combined file
    print("\n💾 Saving combined annotations...")
    combined_df.to_csv('combined_annotations_final.csv', index=False)
    print("✅ Combined annotations saved to combined_annotations_final.csv")
    
    # 2.5. Save filtered "Keep" only file
    print("\n💾 Saving filtered 'Keep' annotations...")
    keep_df = combined_df[combined_df['Keep or skip'] == 'Keep'].copy()
    keep_df.to_csv('filtered_keep_annotations.csv', index=False)
    print(f"✅ Filtered 'Keep' annotations saved to filtered_keep_annotations.csv ({len(keep_df)} rows)")
    
    # 3. Generate analysis and visualizations
    generate_analysis(combined_df)
    
    # 4. Save summary report
    save_summary_report(combined_df)
    
    print("\n🎉 Analysis Complete!")
    print("📁 Check the 'analysis' folder for:")
    print("   - combined_annotations_final.csv (combined data)")
    print("   - figures/ (all visualizations)")
    print("   - summary_report.md (comprehensive report)")

if __name__ == "__main__":
    main() 