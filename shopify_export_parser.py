import csv

def parse_shopify_export(path='data/Products.csv'):
    """
    Parse for products that need to be updated and extract the material tags for update
    """
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        product_data = [row for row in reader if row['Body HTML'] and "<strong>Material</strong>" in row['Body HTML'] and "Material" in row['Tags']]
        for row in product_data:
            row['target_tags'] = ', '.join([tag.split("_")[1] for tag in row['Tags'].split(',') if "Material" in tag])
        return [data for data in product_data if all([tag not in data['Body HTML'] and tag != 'null' for tag in data['target_tags'].split(', ')])]
            
        
def parse_for_non_actionable_data(path='data/Products.csv'):
    """
    Parse for non actionable data (data that cannot be updated) for reference
    """
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader if row['Handle'] == 'gift-card' or "Material" not in row['Tags'] or 'null' in row['Tags'] or not row['Body HTML'] or 'Material' not in row['Body HTML']]
        