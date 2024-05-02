from shopify_export_parser import parse_shopify_export, parse_for_non_actionable_data
import re, csv

def update_product_material_description(product_lst):
    for p in product_lst:
        p['Old Description'] = p['Body HTML']
        match = re.search(r'<p><strong>Material</strong></p>(.*?)<', p['Body HTML'])
        if match:
            p['Body HTML'] = p['Body HTML'][:match.end()-1] + '<p>' + p['target_tags'] + '</p>' + p['Body HTML'][match.end()-1:]
        keys_to_remove = ['target_tags', 'Handle', 'Status', 'Published', 'Published At', 'Tags']
        [p.pop(key) for key in keys_to_remove]
    return product_lst


def generate_updated_product_data_csv():
    product_lst = parse_shopify_export()
    updated_product_lst = update_product_material_description(product_lst)
    splited_product_lst = [updated_product_lst[0:len(updated_product_lst)//2], updated_product_lst[len(updated_product_lst)//2:]]

    for i in range(len(splited_product_lst)):
        with open(f'out/Round{i+1}_Products.csv', 'w') as file:
            write_op = csv.DictWriter(file, splited_product_lst[i][0].keys())
            write_op.writeheader()
            write_op.writerows(splited_product_lst[i])

def generate_non_actionble_product_csv():
    non_actionable_lst = parse_for_non_actionable_data()
    with open('non_actionable_product_list.csv', 'w') as file:
        write_op = csv.DictWriter(file, non_actionable_lst[0].keys())
        write_op.writeheader()
        write_op.writerows(non_actionable_lst)


generate_updated_product_data_csv()
generate_non_actionble_product_csv()        
