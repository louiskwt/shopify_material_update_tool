from shopify_export_parser import parse_shopify_export, parse_for_non_actionable_data
import re, csv

def update_product_material_description(product_lst):
    for p in product_lst:
        p['Old Description'] = p['Body HTML']
        match = re.search(r'<strong>Material</strong>(.*?)<', p['Body HTML'])
        if match:
            p['Body HTML'] = p['Body HTML'][:match.end()-1] + p['target_tags'] + p['Body HTML'][match.end()-1:]
            keys_to_remove = ['target_tags', 'Handle', 'Status', 'Published', 'Published At', 'Tags']
        [p.pop(key) for key in keys_to_remove]
    return product_lst


def generate_updated_product_data_csv():
    product_lst = parse_shopify_export()
    updated_product_lst = update_product_material_description(product_lst)
    with open('shopify_material_update.csv', 'w') as file:
        write_op = csv.DictWriter(file, updated_product_lst[0].keys())
        write_op.writeheader()
        write_op.writerows(updated_product_lst)

def generate_non_actionble_product_csv():
    non_actionable_lst = parse_for_non_actionable_data()
    with open('non_actionable_product_list.csv', 'w') as file:
        write_op = csv.DictWriter(file, non_actionable_lst[0].keys())
        write_op.writeheader()
        write_op.writerows(non_actionable_lst)


generate_updated_product_data_csv()
generate_non_actionble_product_csv()        
